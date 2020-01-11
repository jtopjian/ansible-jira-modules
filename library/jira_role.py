#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.jira_common import JiraModuleBase

__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = """
module: jira_role
version_added: "0.0.1"
short_description: manage a role in Jira
description:
  - Manage a role in Jira

extends_documentation_fragment:
  - jira_modules_common

options:
  name:
    required: true
    description:
      - The name of the role.
      - Cannot be updated.

  description:
    required: false
    description:
      - The description of the role.
      - Can be updated.

author: "Joe Topjian <joe@topjian.net>"
"""

RETURN = """
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
- name: Ensure role exists
  jira_role:
    name: Some Role
    description: A role
"""

REST_ENDPOINT = "rest/api/2/role"


class JiraRole(JiraModuleBase):
    """Utility class to manage a Jira role"""

    def __init__(self):
        self.module_args = dict(
            name=dict(
                required=True,
                _jira_field='name',
                _jira_update=False),

            description=dict(
                required=False,
                _jira_field='description',
                _jira_update=True),

            state=dict(
                required=False,
                default='present',
                choices=['absent', 'present']),
        )

        self.results = dict(
            jira_role=dict(),
            changed=False,
        )

        super(JiraRole, self).__init__(
            derived_arg_spec=self.module_args,
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
        action = None
        is_install_mode = self.param('state') == 'present'

        update_dict = {}

        try:
            id = self.find_id()
            if id is None:
                role = False
            else:
                self.rest_endpoint = "%s/%s" % (REST_ENDPOINT, id)
                role = self.get()

            if not is_install_mode:
                if role is False:
                    return
                action = 'deleted'
            else:
                if role is False:
                    action = 'created'
                else:
                    # Detect updates
                    for (v, jira_field) in self.jira_update_fields():
                        if jira_field in role:
                            if self.param(v) != role[jira_field]:
                                update_dict[jira_field] = self.param(v)

                    if len(update_dict) > 0:
                        action = 'updated'

            self.results['jira_role_action'] = action

            if role is False:
                del(self.results['jira_role'])
            else:
                self.results['jira_role'] = role

            if action is not None:
                self.results['changed'] = True

            if self.check_mode:
                return

            if action == 'created':
                data = {}
                for (v, jira_field) in self.jira_fields():
                    if self.param(v):
                        data[jira_field] = self.param(v)

                self.rest_endpoint = REST_ENDPOINT
                role = self.post(data)
                self.results['jira_role'] = role
                return

            if action == 'updated':
                id = self.find_id()
                if id is None:
                    self.fail("Unable to find Jira role %s" % (
                        self.param('name')))
                self.rest_endpoint = "%s/%s" % (REST_ENDPOINT, id)
                role = self.post(update_dict)
                role = self.get()
                self.results['jira_role'] = role
                return

            if action == 'deleted':
                id = self.find_id()
                if id is None:
                    self.fail("Unable to find Jira role %s" % (
                        self.param('name')))
                self.rest_endpoint = "%s/%s" % (REST_ENDPOINT, id)
                self.delete()
                return

        except Exception as e:
            self.fail(msg=e.message)


if __name__ == '__main__':
    JiraRole()
