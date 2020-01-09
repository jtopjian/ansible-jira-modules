#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.jira_common import JiraModuleBase

__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = """
module: jira_list_issue_security_schemes_fact
version_added: "0.0.1"
short_description: list issue security schemes in Jira
description:
  - List issue security schemes in Jira

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
    jira_issue_security_schemes:
      type: list
      description:
        - Maps Jira issue security schemes to a non-empty list of dicts with
          issue security schemes information.
        - See
          https://docs.atlassian.com/software/jira/docs/api/REST/8.6.0/#api/2/issuesecurityschemes-getIssueSecuritySchemes
          for the schema.
      returned: When Jira issue security schemes are detected.
"""

EXAMPLES = """
- name: List Issue Security Schemes
  jira_list_issue_security_schemes_fact:
"""

REST_ENDPOINT = "rest/api/2/issuesecurityschemes"


class JiraListIssueSecuritySchemes(JiraModuleBase):
    """Utility class to get list of Jira issue security schemes as facts"""

    def __init__(self):
        self.module_args = dict()

        self.results = dict(
            ansible_facts=dict(
                jira_issue_security_schemes=[],
            ),
            changed=False,
        )

        super(JiraListIssueSecuritySchemes, self).__init__(
            derived_arg_spec=self.module_args,
            facts_module=True,
            rest_endpoint=REST_ENDPOINT,
        )

    def exec_module(self, **kwargs):
        try:
            key = 'jira_issue_security_schemes'
            v = self.get()
            if v is False:
                del(self.results['ansible_facts'][key])
            else:
                self.results['ansible_facts'][key] = v
        except Exception as e:
            self.fail(msg=e.message)


if __name__ == '__main__':
    JiraListIssueSecuritySchemes()
