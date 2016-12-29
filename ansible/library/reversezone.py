#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2016, Christian Heimes <cheimes@redhat.com>

from ansible.module_utils.basic import *

DOCUMENTATION = """
---
module: reversezone
short_description: get reverse zone from an IP address
description:
     - get reverse zone from an IP address
version_added: "1.1"
options:
  ipaddress:
    description:
      - IP address
    required: true
    default:
    aliases: []
author: Christian Heimes
"""

EXAMPLES = """
# Get reverse zone
- reversezone: ipaddress={{ ansible_default_ipv4.address }}
  register: res
- debug: msg={{ res }}
"""


def get_reversezone(module, ipaddress):
    if ':' in ipaddress:
        raise ValueError('IPv6 not supported yet')
    parts = ipaddress.split('.')
    if len(parts) != 4:
        raise ValueError('Not an IPv4 address: %r' % ipaddress)
    parts = [int(p) for p in parts]
    return '{0[2]}.{0[1]}.{0[0]}.in-addr.arpa.'.format(parts)


def main():
    module = AnsibleModule(
        argument_spec=dict(
            ipaddress=dict(required=True),
        )
    )

    ipaddress = module.params['ipaddress']
    try:
        reversezone = get_reversezone(module, ipaddress)
    except Exception as e:
        module.fail_json(msg=str(e))
    else:
        module.exit_json(changed=True, reversezone=reversezone)


if __name__ == '__main__':
    main()
