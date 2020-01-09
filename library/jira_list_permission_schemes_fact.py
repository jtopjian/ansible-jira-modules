#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.jira_common import JiraModuleBase
from ansible.module_utils.six.moves.urllib.parse import urlencode

__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = """
module: jira_list_permission_schemes_fact
version_added: "0.0.1"
short_description: list permission schemes in Jira
description:
  - List permission schemes in Jira

extends_documentation_fragment:
  - jira_modules_common

author: "Joe Topjian <joe@topjian.net>"
"""

RETURN = """
ansible_facts:
  description: facts to add to ansible_facts
  returned: always
  type: complex
  contains:
    jira_permission_schemes:
      type: list
      description:
        - Maps Jira permission schemes to a non-empty list of dicts with
          permission schemes information.
        - See
          https://docs.atlassian.com/software/jira/docs/api/REST/8.6.0/#api/2/permissionscheme-getPermissionSchemes
          for the schema.
      returned: When Jira permission schemes are detected.
"""

EXAMPLES = """
- name: List Permission Schemes
  jira_list_permission_schemes_fact:
"""

REST_ENDPOINT = "rest/api/2/permissionscheme"


class JiraListPermissionSchemes(JiraModuleBase):
    """Utility class to get list of Jira permission schemes as facts"""

    def __init__(self):
        self.module_args = dict()

        self.results = dict(
            ansible_facts=dict(
                jira_permission_schemes=[],
            ),
            changed=False,
        )

        super(JiraListPermissionSchemes, self).__init__(
            derived_arg_spec=self.module_args,
            facts_module=True,
            rest_endpoint=REST_ENDPOINT,
        )

    def exec_module(self, **kwargs):
        query = {
            'expand': 'all',
        }

        try:
            v = self.get(urlencode(query))
            if v is False:
                del(self.results['ansible_facts']['jira_permission_schemes'])
            else:
                self.results['ansible_facts']['jira_permission_schemes'] = \
                    v['permissionSchemes']
        except Exception as e:
            self.fail(msg=e.message)


if __name__ == '__main__':
    JiraListPermissionSchemes()
