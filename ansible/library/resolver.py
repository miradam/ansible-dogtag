#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2013, Jan-Piet Mens <jpmens () gmail.com>
#
# This file is part of Ansible
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#
#

import re

from ansible.module_utils.basic import *

DOCUMENTATION = '''
---
module: resolver
short_description: Get information from the system's resolver
description:
     - Obtains nameserver addresses from C(/etc/resolv.conf)
version_added: "1.3"
options:
  resolvconf:
    description:
      - the file (in C(/etc/resolv.conf)-format) to parse
    required: false
    default: /etc/resolv.conf
    aliases: []
author: Jan-Piet Mens
'''

EXAMPLES = '''
# Get nameserver entries from /etc/resolv.conf and print first one
- resolver:
  register: res
- debug: msg={{ res.nameservers[0] }}
'''


# ===========================================
# Support methods

def get_nameservers(module, resolvconf=None):
    nameservers = []
    searchlist = None

    if resolvconf is None:
        resolvconf = '/etc/resolv.conf'

    r = open(resolvconf)
    line = r.readline()
    while line:
        try:
            s = re.search(r"^search\s+(.+)", line)
            if s is not None:
                searchlist = s.group(1).split()
        except:
            pass
        try:
            ip = re.search(r"^nameserver\s+([^\s]+)", line)
            if ip is not None:
                nameservers.append(ip.group(1))
        except:
            pass
        line = r.readline()

    r.close()
    return dict(nameservers=nameservers, searchlist=searchlist)


# ==============================================================
# main

def main():
    module = AnsibleModule(
        argument_spec=dict(
            resolvconf=dict(required=False),
        )
    )

    resolvconf = module.params['resolvconf']

    data = get_nameservers(module, resolvconf=resolvconf)

    # Mission complete
    module.exit_json(**data)


if __name__ == '__main__':
    main()
