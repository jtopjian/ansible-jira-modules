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
            query=dict(required=False, _jira_field='query'),
            exclude=dict(required=False, _jira_field='exclude'),
            username=dict(required=False, _jira_field='username'),
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

        for (field, jira_field) in self.jira_fields():
            v = self.param(field)
            if v:
                query[jira_field] = v

        try:
            v = self.get(urlencode(query))
            if v is False:
                del(self.results['ansible_facts']['jira_groups'])
            else:
                self.results['ansible_facts']['jira_groups'] = v['groups']
        except Exception as e:
            self.fail(msg=e.message)


if __name__ == '__main__':
    JiraListGroups()
