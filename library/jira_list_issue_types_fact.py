#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.jira_common import JiraModuleBase

__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = """
module: jira_list_issue_types_fact
version_added: "0.0.1"
short_description: list issue types in Jira
description:
  - List issue types in Jira

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
    jira_issue_types:
      type: list
      description:
        - Maps Jira issue types to a non-empty list of dicts with
          issue types information.
        - See
          https://docs.atlassian.com/software/jira/docs/api/REST/8.6.0/#api/2/issuetype-getIssueAllTypes
          for the schema.
      returned: When Jira issue types are detected.
"""

EXAMPLES = """
- name: List Issue Types
  jira_list_issue_types_fact:
"""

REST_ENDPOINT = "rest/api/2/issuetype"


class JiraListIssueTypes(JiraModuleBase):
    """Utility class to get list of Jira issue types as facts"""

    def __init__(self):
        self.module_args = dict()

        self.results = dict(
            ansible_facts=dict(
                jira_issue_types=[],
            ),
            changed=False,
        )

        super(JiraListIssueTypes, self).__init__(
            derived_arg_spec=self.module_args,
            facts_module=True,
            rest_endpoint=REST_ENDPOINT,
        )

    def exec_module(self, **kwargs):
        try:
            key = 'jira_issue_types'
            v = self.get()
            if v is False:
                del(self.results['ansible_facts'][key])
            else:
                self.results['ansible_facts'][key] = v
        except Exception as e:
            self.fail(msg=e.message)


if __name__ == '__main__':
    JiraListIssueTypes()
