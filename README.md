eureka
=====
eureka is for python to connect to eureka, include heartbeat and get app info.

Example:
----------

    app = 'eureka-test'
    eureka_urls = ['http://localhost:8761', ]
    heartbeat = 5.0
    instance = {
        'ipAddr': 'localhost',
        'port': 7777,
        'app': app,
        'instanceId': 'instanceId'
    }


    service_wrapper = SimpleEurekaServiceWrapper(eureka_urls, instance, heartbeat)

    # Registering service
    service_wrapper.run()
    # Stopping service
    service_wrapper.stop()

    client_wrapper = SimpleEurekaClientWrapper(eureka_urls)

    # Fetching app data
    app_data = client_wrapper.app(app)


Support
----------

if you have any problem or suggest, please contact me with my email of 819070918@qq.com.
