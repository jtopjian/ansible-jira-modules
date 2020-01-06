#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.jira_common import JiraModuleBase
from ansible.module_utils.six.moves.urllib.parse import urlencode

__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = """
module: jira_list_groups_fact
version_added: "0.0.1"
short_description: list groups in Jira
description:
  - List groups in Jira

extends_documentation_fragment:
  - jira_modules_common

options:
  query:
    required: false
    description:
      - A search string to match with a group name.

  exclude:
    required: false
    description:
      - A string to exclude matching groups.

  username:
    required: false
    description:
      - Return groups where username is a member.
    default: false

author: "Joe Topjian <joe@topjian.net>"
"""

RETURN = """
ansible_facts:
  description: facts to add to ansible_facts
  returned: always
  type: complex
  contains:
    jira_groups:
      type: list
      description:
        - Maps Jira groups to a non-empty list of dicts with
          group information.
        - See
          https://docs.atlassian.com/software/jira/docs/api/REST/8.6.0/#api/2/groups-findGroups
          for the schema.
      returned: When Jira groups are detected.
"""

EXAMPLES = """
- name: List Groups
  jira_list_groups_fact:
    jira_url: '{{ server }}'
    jira_username: '{{ user }}'
    jira_password: '{{ pass }}'
"""

REST_ENDPOINT = "rest/api/2/groups/picker"


class JiraListGroups(JiraModuleBase):
    """Utility class to get list of Jira groups as facts"""

    def __init__(self):
        self.module_args = dict(
            query=dict(required=False),
            exclude=dict(required=False),
            username=dict(required=False),
        )

        self.results = dict(
            ansible_facts=dict(
                jira_groups=[],
            ),
            changed=False,
        )

        super(JiraListGroups, self).__init__(
            derived_arg_spec=self.module_args,
            facts_module=True,
            rest_endpoint=REST_ENDPOINT,
        )

    def exec_module(self, **kwargs):
        query = {}

        q = self.module.params.get('query')
        if q:
            query["query"] = q

        exclude = self.module.params.get('exclude')
        if exclude:
            query["exclude"] = exclude

        username = self.module.params.get('username')
        if username:
            query["username"] = username

        try:
            groups = self.get(urlencode(query))
            self.results['ansible_facts']['jira_groups'] = groups['groups']
        except Exception as e:
            self.fail(msg=e.message)


if __name__ == '__main__':
    JiraListGroups()
