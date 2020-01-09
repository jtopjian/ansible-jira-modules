#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.jira_common import JiraModuleBase
from ansible.module_utils.six.moves.urllib.parse import urlencode

__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = """
module: jira_get_user_fact
version_added: "0.0.1"
short_description: get a user in Jira
description:
  - Get a user in Jira

extends_documentation_fragment:
  - jira_modules_common

options:
  username:
    required: false
    description:
      - Query for a user by their username.
      - This parameter is mutually exclusive with C(key).

  key:
    required: false
    description:
      - Query for a user by their Jira Key.
      - This parameter is mutually exclusive with C(username).

author: "Joe Topjian <joe@topjian.net>"
"""

RETURN = """
ansible_facts:
  description: facts to add to ansible_facts
  returned: always
  type: complex
  contains:
    jira_user:
      type: dict
      description:
        - A Jira user.
        - See
          https://docs.atlassian.com/software/jira/docs/api/REST/8.6.0/#api/2/user-getUser
          for the schema.
      returned: When a Jira user was detected.
"""

EXAMPLES = """
- name: Get a user
  jira_get_user_fact:
    jira_url: '{{ server }}'
    jira_username: '{{ user }}'
    jira_password: '{{ pass }}'
    username: 'admin'
"""

REST_ENDPOINT = "rest/api/2/user"


class JiraGetUser(JiraModuleBase):
    """Utility class to get a Jira user"""

    def __init__(self):
        self.module_args = dict(
            username=dict(_jira_field='username'),
            key=dict(_jira_field='key'),
        )

        self.results = dict(
            ansible_facts=dict(
                jira_user=dict()
            ),
            changed=False,
        )

        super(JiraGetUser, self).__init__(
            derived_arg_spec=self.module_args,
            facts_module=True,
            mutually_exclusive=[['username', 'key']],
            required_one_of=[['username', 'key']],
            rest_endpoint=REST_ENDPOINT,
        )

    def exec_module(self, **kwargs):
        query = {}
        for (field, jira_field) in self.jira_fields():
            v = self.param(field)
            if v is not None:
                query[jira_field] = v

        query['expand'] = ','.join(['groups', 'applicationRoles'])

        try:
            v = self.get(urlencode(query))
            if v is False:
                del(self.results['ansible_facts']['jira_user'])
            else:
                self.results['ansible_facts']['jira_user'] = v
        except Exception as e:
            self.fail(msg=e.message)


if __name__ == '__main__':
    JiraGetUser()
