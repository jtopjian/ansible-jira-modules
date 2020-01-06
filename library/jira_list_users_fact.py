#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.jira_common import JiraModuleBase
from ansible.module_utils.six.moves.urllib.parse import urlencode

__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = """
module: jira_list_users_fact
version_added: "0.0.1"
short_description: list users in JIRA
description:
  - List users in JIRA

extends_documentation_fragment:
  - jira_modules_common

options:
  username:
    required: false
    description:
      - A search string to use for the username. By default,
        a "." is used to search for all users.
    default: .

  include_active:
    required: false
    description:
      - Include active users. Defaults to true.
    default: true
    type: bool

  include_inactive:
    required: false
    description:
      - Include inactive users. Defaults to false.
    default: false
    type: bool

author: "Joe Topjian <joe@topjian.net>"
"""

RETURN = """
ansible_facts:
  description: facts to add to ansible_facts
  returned: always
  type: complex
  contains:
    jira_users:
      type: list
      description:
        - Maps Jira users to a non-empty list of dicts with
          user information.
        - See
          https://docs.atlassian.com/software/jira/docs/api/REST/8.6.0/#api/2/user-findUsers
          for the schema.
      returned: When Jira users are detected.
"""

EXAMPLES = """
- name: List Users
  jira_list_users_fact:
    jira_url: '{{ server }}'
    jira_username: '{{ user }}'
    jira_password: '{{ pass }}'
"""

REST_ENDPOINT = "rest/api/2/user/search"


class JiraListUsers(JiraModuleBase):
    """Utility class to get list of Jira users as facts"""

    def __init__(self):
        self.module_args = dict(
            username=dict(required=False, default='.'),
            include_active=dict(required=False, type='bool', default=True),
            include_inactive=dict(required=False, type='bool', default=False),
        )

        self.results = dict(
            ansible_facts=dict(
                jira_users=[],
            ),
            changed=False,
        )

        super(JiraListUsers, self).__init__(
            derived_arg_spec=self.module_args,
            facts_module=True,
            rest_endpoint=REST_ENDPOINT,
        )

    def exec_module(self, **kwargs):
        query = {}
        v = self.module.params.get('username')
        if v is not None:
            query['username'] = v

        v = self.module.params.get('include_active')
        if v is not None:
            query['includeActive'] = v

        v = self.module.params.get('include_inactive')
        if v is not None:
            query['includeInactive'] = v

        try:
            users = self.get(urlencode(query))
            self.results['ansible_facts']['jira_users'] = users
        except Exception as e:
            self.fail(msg=e.message)


if __name__ == '__main__':
    JiraListUsers()
