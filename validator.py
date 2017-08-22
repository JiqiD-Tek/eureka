# -*- coding: utf-8 -*-
# File   @ validator.py
# Create @ 2017/8/10 14:24
# Author @ 819070918@qq.com

import configure


class EurekaValidationError(Exception):
    pass


def validate_instance_definition(instance_definition):
    for needed in configure.EUREKA_INSTANCE_DEFINITION['needed']:
        if needed not in instance_definition:
            raise EurekaValidationError("{} is necessary".format(needed))

    configure.EUREKA_INSTANCE_DEFINITION['needed-with-default'].update(instance_definition)
    instance_definition = configure.EUREKA_INSTANCE_DEFINITION['needed-with-default']

    for part in configure.EUREKA_INSTANCE_DEFINITION['transformations']:
        if part[0] in instance_definition and part[1](instance_definition[part[0]]):
            instance_definition[part[0]] = part[2](
                instance_definition[part[0]])

    return {'instance': instance_definition}
