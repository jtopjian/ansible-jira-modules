#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.jira_common import JiraModuleBase

__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = """
module: jira_get_role_fact
version_added: "0.0.1"
short_description: get a role in Jira
description:
  - Get a role in Jira

extends_documentation_fragment:
  - jira_modules_common

options:
  id:
    required: false
    description:
      - Query for a role by its ID.
      - This parameter is mutually exclusive with C(name).

  name:
    required: false
    description:
      - Query for a role by its name.
      - This parameter is mutually exclusive with C(id).

author: "Joe Topjian <joe@topjian.net>"
"""

RETURN = """
ansible_facts:
  description: facts to add to ansible_facts
  returned: always
  type: complex
  contains:
    jira_role:
      type: dict
      description:
        - A Jira role.
        - See
          https://docs.atlassian.com/software/jira/docs/api/REST/8.6.0/#api/2/role-getProjectRolesById
          for the schema.
      returned: When a Jira role was detected.
"""

EXAMPLES = """
- name: Get a role
  jira_get_role_fact:
    name: 'Administrators'
"""

REST_ENDPOINT = "rest/api/2/role"


class JiraGetRole(JiraModuleBase):
    """Utility class to get a Jira role as a fact"""

    def __init__(self):
        self.module_args = dict(
            id=dict(),
            name=dict(),
        )

        self.results = dict(
            ansible_facts=dict(
                jira_role=dict()
            ),
            changed=False,
        )

        super(JiraGetRole, self).__init__(
            derived_arg_spec=self.module_args,
            facts_module=True,
            mutually_exclusive=[['id', 'name']],
            required_one_of=[['id', 'name']],
            rest_endpoint=REST_ENDPOINT,
        )

    def find_id(self):
        self.rest_endpoint = REST_ENDPOINT
        roles = self.get()
        name = self.param('name')
        id = None
        for role in roles:
            if role["name"] == name:
                id = role["id"]
        return id

    def exec_module(self, **kwargs):
        id = self.param('id')
        if id is None:
            id = self.find_id()

        self.rest_endpoint = "%s/%s" % (self.rest_endpoint, id)

        try:
            v = self.get()
            if v is False:
                del(self.results['ansible_facts']['jira_role'])
            else:
                self.results['ansible_facts']['jira_role'] = v
        except Exception as e:
            self.fail(msg=e.message)


if __name__ == '__main__':
    JiraGetRole()
