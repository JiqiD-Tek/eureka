# -*- coding: utf-8 -*-
# File   @ client.py
# Create @ 2017/8/10 14:23
# Author @ 819070918@qq.com

import time

import validator
import const


def get_timestamp():
    return int(time.time())


class EurekaClientError(Exception):
    pass


class EurekaInstanceDoesNotExistException(Exception):
    pass


class EurekaClient:

    def __init__(self, eureka_urls, instance_definition=None, verbose=False):
        """
        eureka_urls is the address to send requests to.
        instance_definition is description of service
            NOT conforming (as of 16.05.17) to schema available in
            https://github.com/Netflix/eureka/wiki/Eureka-REST-operations
        Basic operations:
        service side:
            client = EurekaClient(['localhost:8765', ], {'ipAddr': '127.0.0.1', 'port': 80, 'app': 'myapp'})
            client.register()
            client.heartbeat()
        client side:
            client = EurekaClient(['localhost:8765', ])
            try:
                client.query(app='myapp')
            except EurekaClientError:
                print('operation failed')
        """
        self.eureka_urls = eureka_urls
        if instance_definition is not None:
            if 'instanceId' not in instance_definition:
                instance_definition['instanceId'] = "{}:{}:{}".format(
                    instance_definition['ipAddr'],
                    instance_definition['app'],
                    instance_definition['port'])
            self.instance_definition = validator.validate_instance_definition(instance_definition)
            self.app_id = self.instance_definition['instance']['app']
            self.instance_id = self.instance_definition['instance']['instanceId']

        self.verbose = verbose
        if verbose:
            print("EurekaClient running with verbosity enabled")
            print("instance_definition: {}".format(self.instance_definition))

    def register(self):
        request_api = '/eureka/apps/' + self.app_id
        self._request('POST', request_api, 'registration', 204, payload=self.instance_definition)

    def deregister(self):
        self._request('DELETE', comment='deregistration')

    def heartbeat(self):
        request_api = self._instance_api() + '?status=UP&lastDirtyTimestamp=' + \
            str(get_timestamp())
        self._request('PUT', api=request_api, comment='heartbeat',
                      errors={404: EurekaInstanceDoesNotExistException})

    def query(self, app=None, instance=None):

        request_api = '/eureka/apps/'
        if app is not None:
            request_api += app
            if instance is not None:
                request_api += '/' + instance
        elif instance is not None:
            request_api = '/eureka/instances/' + instance
        request = self._request('GET', request_api, 'query')
        return request.json()

    def query_vip(self, vip):
        request_api = '/eureka/vips/' + vip
        request = self._request('GET', request_api, 'query vip')
        return request

    def query_svip(self, svip):
        request_api = '/eureka/svips/' + svip
        request = self._request('GET', request_api, 'query svip')
        return request

    def take_instance_out_of_service(self):
        request_api = self._instance_api() + '/status?value=OUT_OF_SERVICE'
        self._request('PUT', request_api, 'out of service')

    def put_instance_back_into_service(self):
        request_api = self._instance_api() + '/status?value=UP'
        self._request('PUT', request_api, 'up')

    def update_metadata(self, key, value):
        request_api = self._instance_api() + \
            '/metadata?{}={}'.format(key, value)
        self._request('PUT', request_api, 'update_metadata')

    def _instance_api(self):
        return '/eureka/apps/' + self.app_id + '/' + self.instance_id

    def _fail_code(self, code, request, comment, errors=None):
        if self.verbose:
            self._show_request(request, comment)
        if request.status_code != code:
            error = EurekaClientError
            if errors is not None and request.status_code in errors:
                error = errors[request.status_code]
            raise error({'request': request, 'comment': comment, 'status_code': request.status_code})

    def _show_request(self, request, comment):
        print("{}:".format(comment))
        print("Request code: {}".format(request.status_code))
        print("Request headers: {}".format(request.headers))
        print("Request response: {}".format(request.text))

    def _request(self, method, api=None, comment='operation', accepted_code=200, errors=None, payload=None):
        if api is None:
            api = self._instance_api()

        success = False
        last_e = None
        for eureka_url in self.eureka_urls:
            try:
                request = const.EUREKA_REQUESTS[method](
                    "{}{}".format(eureka_url, api), headers=const.EUREKA_HEADERS[method], json=payload)
                self._fail_code(accepted_code, request, comment, errors=errors)
                success = True
                return request

            except Exception as Ex:
                last_e = Ex

        if not success:
            raise last_e
