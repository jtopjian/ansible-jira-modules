#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.jira_common import JiraModuleBase
from ansible.module_utils.six.moves.urllib.parse import urlencode

__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = """
module: jira_list_projects_fact
version_added: "0.0.1"
short_description: list projects in Jira
description:
  - List projects in Jira

extends_documentation_fragment:
  - jira_modules_common

options:
  expand:
    required: false
    description:
      - A list of fields to expand.
      - Defaults to ['description', 'lead', 'url' ,'projectKeys']

  include_archived:
    required: false
    description:
      - Include archived projects. Defaults to false.
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
    jira_projects:
      description:
      type: list
        - Maps Jira projects to a non-empty list of dicts with
          project information.
        - See
          https://docs.atlassian.com/software/jira/docs/api/REST/8.6.0/#api/2/project-getAllProjects
          for the schema.
      returned: When Jira projects are detected.
"""

EXAMPLES = """
- name: List Projects
  jira_list_projects_fact:
    jira_url: '{{ server }}'
    jira_username: '{{ user }}'
    jira_password: '{{ pass }}'
"""

REST_ENDPOINT = "rest/api/2/project"


class JiraListProjects(JiraModuleBase):
    """Utility class to get list of Jira projects as facts"""

    def __init__(self):
        self.module_args = dict(
            expand=dict(required=False, type='list',
                        default=['description', 'lead', 'url', 'projectKeys']),
            include_archived=dict(required=False, type='bool', default=False),
        )

        self.results = dict(
            ansible_facts=dict(
                jira_projects=[],
            ),
            changed=False,
        )

        super(JiraListProjects, self).__init__(
            derived_arg_spec=self.module_args,
            facts_module=True,
            rest_endpoint=REST_ENDPOINT,
        )

    def exec_module(self, **kwargs):
        query = {}
        v = self.module.params.get('expand')
        if v is not None:
            query['expand'] = ','.join(v)

        v = self.module.params.get('include_archived')
        if v is not None:
            query['includeArchived'] = v

        try:
            projects = self.get(urlencode(query))
            self.results['ansible_facts']['jira_projects'] = projects
        except Exception as e:
            self.fail(msg=e.message)


if __name__ == '__main__':
    JiraListProjects()
