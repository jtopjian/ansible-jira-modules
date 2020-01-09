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
        query = {
            'expand': ','.join(['description', 'lead', 'url', 'projectKeys'])
        }

        v = self.param('include_archived')
        if v is not None:
            query['includeArchived'] = v

        try:
            v = self.get(urlencode(query))
            if v is False:
                del(self.results['ansible_facts']['jira_projects'])
            else:
                self.results['ansible_facts']['jira_projects'] = v
        except Exception as e:
            self.fail(msg=e.message)


if __name__ == '__main__':
    JiraListProjects()
