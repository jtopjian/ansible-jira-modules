#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.jira_common import JiraModuleBase
from ansible.module_utils.six.moves.urllib.parse import urlencode

__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = """
module: jira_get_group_fact
version_added: "0.0.1"
short_description: get a group in Jira
description:
  - Get a group in Jira

extends_documentation_fragment:
  - jira_modules_common

options:
  group_name:
    required: true
    description:
      - Query for a group by its name.

  include_inactive_users:
    required: false
    description:
      - Include inactive users in the result
    type: bool
    default: false

  max_results:
    required: false
    description:
      - The max number of users to include in the result.
    type: int
    default: 50

author: "Joe Topjian <joe@topjian.net>"
"""

RETURN = """
ansible_facts:
  description: facts to add to ansible_facts
  returned: always
  type: complex
  contains:
    jira_group:
      type: dict
      description:
        - A Jira group.
        - See
          https://docs.atlassian.com/software/jira/docs/api/REST/8.6.0/#api/2/group-getUsersFromGroup
          for the schema.
      returned: When a Jira group was detected.
"""

EXAMPLES = """
- name: Get a group
  jira_get_group_fact:
    jira_url: '{{ server }}'
    jira_username: '{{ user }}'
    jira_password: '{{ pass }}'
    group_name: 'jira-administrators'
"""

REST_ENDPOINT = "rest/api/2/group/member"


class JiraGetGroup(JiraModuleBase):
    """Utility class to get a Jira group"""

    def __init__(self):
        self.module_args = dict(
            group_name=dict(required=True),
            include_inactive_users=dict(),
            max_results=dict(),
        )

        self.results = dict(
            ansible_facts=dict(
                jira_group={}
            ),
            changed=False,
        )

        super(JiraGetGroup, self).__init__(
            derived_arg_spec=self.module_args,
            facts_module=True,
            rest_endpoint=REST_ENDPOINT,
        )

    def exec_module(self, **kwargs):
        query = {}
        v = self.param('group_name')
        if v is not None:
            query['groupname'] = v

        v = self.param('include_inactive_users')
        if v is not None:
            query['includeInactiveUsers'] = v

        v = self.param('max_results')
        if v is not None:
            query['maxResults'] = v

        try:
            group = self.get(urlencode(query))
            group['name'] = self.param('group_name')
            self.results['ansible_facts']['jira_group'] = group
        except Exception as e:
            self.fail(msg=e.message)


if __name__ == '__main__':
    JiraGetGroup()
