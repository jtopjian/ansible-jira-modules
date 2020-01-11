#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.jira_common import JiraModuleBase
from ansible.module_utils.six.moves.urllib.parse import quote, urlencode

__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = """
module: jira_jql_fact
version_added: "0.0.1"
short_description: Run a JQL query in Jira
description:
  - Run a JQL query in Jira

extends_documentation_fragment:
  - jira_modules_common

options:
  jql:
    required: true
    description:
      - The JQL query to run

  fields:
    required: false
    description:
      - The list of fields to return.
      - By default, all fields are returned.

  max_results:
    required: false
    description:
      - The max number of users to include in the result.
    type: int
    default: 50

  validate_query:
    required: false
    description:
      - Whether to validate the given JQL query or not.
    type: bool

author: "Joe Topjian <joe@topjian.net>"
"""

RETURN = """
ansible_facts:
  description: facts to add to ansible_facts
  returned: always
  type: complex
  contains:
    jira_jql_results:
      type: dict
      description:
        - The results of the Jira JQL query.
        - See
          https://docs.atlassian.com/software/jira/docs/api/REST/8.6.0/#api/2/search-search
          for the schema.
      returned: When a Jira JQL query returned results.
"""

EXAMPLES = """
- name: Run a JQL query
  jira_jql_fact:
    jql: "project in (PRJ1)"
"""

REST_ENDPOINT = "rest/api/2/search"


class JiraJQLQuery(JiraModuleBase):
    """Utility class to run a JQL query in Jira"""

    def __init__(self):
        self.module_args = dict(
            jql=dict(
                required=True,
                _jira_field='jql'),

            fields=dict(
                type='list',
                _jira_field='fields'),

            max_results=dict(
                type="int",
                _jira_field='maxResults'),

            validate_query=dict(
                type="bool",
                _jira_field='validateQuery'),
        )

        self.results = dict(
            ansible_facts=dict(
                jira_jql_results=dict(),
            ),
            changed=False,
        )

        super(JiraJQLQuery, self).__init__(
            derived_arg_spec=self.module_args,
            facts_module=True,
            rest_endpoint=REST_ENDPOINT,
        )

    def exec_module(self, **kwargs):
        data = {}

        for (field, jira_field) in self.jira_fields():
            v = self.param(field)
            if v is not None:
                if field == "fields":
                    data[jira_field] = ",".join(v)
                else:
                    data[jira_field] = v

        try:
            jql = self.post(data)
            self.log("%s" % (jql))
            if jql is False:
                del(self.results['ansible_facts']['jira_jql_results'])
            else:
                self.results['ansible_facts']['jira_jql_results'] = jql
        except Exception as e:
            self.fail(msg=e.message)


if __name__ == '__main__':
    JiraJQLQuery()
