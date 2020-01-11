#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.jira_common import JiraModuleBase

__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = """
module: jira_project_role_membership
version_added: "0.0.1"
short_description: manage a project role membership in Jira
description:
  - Manage a project role membership in Jira

extends_documentation_fragment:
  - jira_modules_common

options:
  project_key:
    required: false
    description:
      - The Jira key of the project.
      - Cannot be updated.
      - This parameter is mutually exclusive with C(project_id)

  project_id:
    required: false
    description:
      - The ID of the project.
      - Cannot be updated.
      - This parameter is mutually exclusive with C(project_key)

  role_name:
    required: false
    description:
      - The name of the Jira role
      - Cannot be updated.
      - This parameter is mutually exclusive with C(role_id)

  role_id:
    required: false
    description:
      - The ID of the Jira role
      - Cannot be updated.
      - This parameter is mutually exclusive with C(role_name)

  users:
    required: false
    description:
      - Users to belong to the role
      - Can be updated.

  groups:
    required: false
    description:
      - Groups to belong to the role
      - Can be updated.

author: "Joe Topjian <joe@topjian.net>"
"""

RETURN = """
jira_project_role_membership:
  type: dict
  description:
    - A Jira project role membership.
    - See
      https://docs.atlassian.com/software/jira/docs/api/REST/8.6.0/#api/2/project/{projectIdOrKey}/role-getProjectRole
      for the schema.
  returned: When a Jira project role membership was detected.
"""

EXAMPLES = """
- name: Ensure project role membership exists
  jira_project_role_membership:
    project_key: PRJ1
    role_name: Administrators
    users:
      - admin
"""

ROLE_REST_ENDPOINT = "rest/api/2/role"
REST_ENDPOINT = "rest/api/2/project/%s/role/%s"


class JiraProjectCategory(JiraModuleBase):
    """Utility class to manage a Jira project role membership"""

    def __init__(self):
        self.module_args = dict(
            project_name=dict(
                required=False,
                _jira_field='project_name',
                _jira_update=False),

            project_key=dict(
                required=False,
                _jira_field='project_key',
                _jira_update=False),

            role_name=dict(
                required=False,
                _jira_field='role_name',
                _jira_update=False),

            role_id=dict(
                required=False,
                _jira_field='role_id',
                _jira_update=False),

            users=dict(
                type='list',
                required=False,
                _jira_field='users',
                _jira_update=True),

            groups=dict(
                type='list',
                required=False,
                _jira_field='groups',
                _jira_update=True),

            state=dict(
                required=False,
                default='present',
                choices=['absent', 'present']),
        )

        self.results = dict(
            jira_project_role_membership=dict(),
            changed=False,
        )

        super(JiraProjectCategory, self).__init__(
            derived_arg_spec=self.module_args,
            rest_endpoint=REST_ENDPOINT,
            mutually_exclusive=[
                ['project_id', 'project_key'], ['role_id', 'role_name']],
            required_one_of=[
                ['project_id', 'project_key'], ['role_id', 'role_name']],
        )

    def find_role_id(self):
        self.rest_endpoint = ROLE_REST_ENDPOINT
        roles = self.get()
        name = self.param('role_name')

        id = None
        for role in roles:
            if role["name"] == name:
                id = role["id"]

        return id

    def get_users_and_groups(self):
        users = []
        groups = []
        actors = self.get()
        for actor in actors['actors']:
            if actor['type'] == 'atlassian-user-role-actor':
                users.append(actor['name'])
            if actor['type'] == 'atlassian-group-role-actor':
                groups.append(actor['name'])
        return (users, groups)

    def exec_module(self, **kwargs):
        action = None
        is_install_mode = self.param('state') == 'present'

        try:
            prj = self.param('project_key')
            if prj is None:
                prj = self.param('project_key')

            role_id = self.param('role_id')
            if role_id is None:
                role_id = self.find_role_id()
                if role_id is None:
                    self.fail("Unable to determine Jira role id: %s",
                              self.param('role_name'))

            self.rest_endpoint = REST_ENDPOINT % (prj, role_id)

            users = self.param('users')
            groups = self.param('groups')
            (_users, _groups) = self.get_users_and_groups()

            if not is_install_mode:
                action = 'deleted'

                if len(users) == 0 and len(_users) == 0 and \
                   len(groups) == 0 and len(_groups) == 0:
                    action = None
            else:
                if (set(users) != set(_users)) or \
                   (set(groups) != set(_groups)):
                    action = 'updated'

            self.results['jira_project_role_membership_action'] = action

            if len(users) == 0 and len(groups) == 0:
                del(self.results['jira_project_role_membership'])

            if action is not None:
                self.results['changed'] = True

            if self.check_mode:
                return

            if action == 'updated' or action == 'deleted':
                data = dict()
                key = 'categorisedActors'
                data[key] = dict()

                gKey = 'atlassian-group-role-actor'
                uKey = 'atlassian-user-role-actor'

                if action == 'deleted':
                    data[key][gKey] = []
                    data[key][uKey] = []

                if action == 'updated':
                    if len(groups) > 0:
                        data[key][gKey] = groups

                    if len(users) > 0:
                        data[key][uKey] = users

                self.put(data)

            (_users, _groups) = self.get_users_and_groups()
            if len(_users) == 0 and len(_groups) == 0:
                del(self.results['jira_project_role_membership'])
            else:
                v = {
                    'users': _users,
                    'groups': _groups,
                }

                self.results['jira_project_role_membership'] = v

        except Exception as e:
            self.fail(msg=e.message)


if __name__ == '__main__':
    JiraProjectCategory()
