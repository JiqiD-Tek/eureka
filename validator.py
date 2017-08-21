# -*- coding: utf-8 -*-
# File   @ validator.py
# Create @ 2017/8/10 14:24
# Author @ 819070918@qq.com

import const


class PyEurekaValidationError(Exception):
    pass


class PyEurekaInternalValidationError(Exception):
    pass


def validate_instance_definition(instance_definition):
    for needed in const.EUREKA_INSTANCE_DEFINITION['needed']:
        if needed not in instance_definition:
            raise PyEurekaValidationError("{} is necessary".format(needed))

    for part in const.EUREKA_INSTANCE_DEFINITION['needed-with-default']:
        if part[0] not in instance_definition:
            if part[1] == const.EUREKA_DEFAULT_SAME_AS:
                instance_definition[part[0]] = instance_definition[part[2]]
            elif part[1] == const.EUREKA_DEFAULT_VALUE:
                instance_definition[part[0]] = part[2]
            else:
                raise PyEurekaInternalValidationError(
                    "on {} - unknown symbol {}".format(part[0], part[1]))

    for part in const.EUREKA_INSTANCE_DEFINITION['transformations']:
        if part[0] in instance_definition and part[1](instance_definition[part[0]]):
            instance_definition[part[0]] = part[2](
                instance_definition[part[0]])

    return {'instance': instance_definition}
