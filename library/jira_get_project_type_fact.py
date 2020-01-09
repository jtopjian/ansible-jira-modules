#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.jira_common import JiraModuleBase
from ansible.module_utils.six.moves.urllib.parse import quote

__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = """
module: jira_get_project_type_fact
version_added: "0.0.1"
short_description: list project types in Jira
description:
  - Get a project type in Jira

extends_documentation_fragment:
  - jira_modules_common

options:
  key:
    required: true
    description:
      - The Jira key of the project type

author: "Joe Topjian <joe@topjian.net>"
"""

RETURN = """
ansible_facts:
  description: facts to add to ansible_facts
  returned: always
  type: complex
  contains:
    jira_project_type:
      type: dict
      description:
        - A Jira project type.
        - See
          https://docs.atlassian.com/software/jira/docs/api/REST/8.6.0/#api/2/project/type-getProjectTypeByKey
          for the schema.
      returned: When a Jira project type is detected.
"""

EXAMPLES = """
- name: Get a project type
  jira_get_project_type_fact:
    key: business
"""

REST_ENDPOINT = "rest/api/2/project/type"


class JiraGetProjectType(JiraModuleBase):
    """Utility class to get a Jira project type fact"""

    def __init__(self):
        self.module_args = dict(
            key=dict(required=True),
        )

        self.results = dict(
            ansible_facts=dict(
                jira_project_types=[],
            ),
            changed=False,
        )

        super(JiraGetProjectType, self).__init__(
            derived_arg_spec=self.module_args,
            facts_module=True,
            rest_endpoint=REST_ENDPOINT,
        )

    def exec_module(self, **kwargs):
        key = self.param('key')
        self.rest_endpoint = "%s/%s" % (self.rest_endpoint, quote(key))

        try:
            v = self.get()
            if v is False:
                del(self.results['ansible_facts']['jira_project_type'])
            else:
                self.results['ansible_facts']['jira_project_type'] = v
        except Exception as e:
            self.fail(msg=e.message)


if __name__ == '__main__':
    JiraGetProjectType()
