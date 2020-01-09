#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.jira_common import JiraModuleBase
from ansible.module_utils.six.moves.urllib.parse import quote, urlencode

__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = """
module: jira_get_issue_type_fact
version_added: "0.0.1"
short_description: list issue types in Jira
description:
  - Get a issue type in Jira

extends_documentation_fragment:
  - jira_modules_common

options:
  issue_type_id:
    required: true
    description:
      - The ID of the Jira issue type

author: "Joe Topjian <joe@topjian.net>"
"""

RETURN = """
ansible_facts:
  description: facts to add to ansible_facts
  returned: always
  type: complex
  contains:
    jira_issue_type:
      type: dict
      description:
        - A Jira issue type.
        - See
          https://docs.atlassian.com/software/jira/docs/api/REST/8.6.0/#api/2/issuetype-getIssueType
          for the schema.
      returned: When a Jira issue type is detected.
"""

EXAMPLES = """
- name: Get a issue type
  jira_get_issue_type_fact:
    issue_type_id: 10000
"""

REST_ENDPOINT = "rest/api/2/issuetype"


class JiraGetIssueType(JiraModuleBase):
    """Utility class to get a Jira issue type fact"""

    def __init__(self):
        self.module_args = dict(
            issue_type_id=dict(required=True),
        )

        self.results = dict(
            ansible_facts=dict(
                jira_issue_type="",
            ),
            changed=False,
        )

        super(JiraGetIssueType, self).__init__(
            derived_arg_spec=self.module_args,
            facts_module=True,
            rest_endpoint=REST_ENDPOINT,
        )

    def exec_module(self, **kwargs):
        issue_type_id = self.param('issue_type_id')
        self.rest_endpoint = "%s/%s" % (
            self.rest_endpoint, quote(issue_type_id))

        query = {
            'expand': 'all',
        }

        try:
            v = self.get(urlencode(query))
            if v is False:
                del(self.results['ansible_facts']['jira_issue_type'])
            else:
                self.results['ansible_facts']['jira_issue_type'] = v
        except Exception as e:
            self.fail(msg=e.message)


if __name__ == '__main__':
    JiraGetIssueType()
