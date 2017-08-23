eureka
=====
eureka is for python to connect to eureka, include heartbeat and get app info.

Example:
----------

    from eureka import DiscoveryClient

    app = 'eureka-test'

    eureka_urls = ['http://localhost:8761', ]

    instance = {
        'ipAddr': 'localhost',
        'port': 7777,
        'app': app,
        'instanceId': 'instanceId',
        'leaseInfo': {
            'durationInSecs': 10,
            'evictionDurationInSecs': 20,
        }
    }


    client = DiscoveryClient(eureka_urls, instance)

    # Registering service
    client.register()
    # Stopping service
    client.unregister()

    # Fetching app data
    app_data = client.app(app)



Support
----------

if you have any problem or suggest, please contact me with my email of 819070918@qq.com.
