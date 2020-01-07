#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.jira_common import JiraModuleBase
from ansible.module_utils.six.moves.urllib.parse import urlencode

__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = """
module: jira_user_group_membership
version_added: "0.0.1"
short_description: manage a group in Jira
description:
  - Manage a group in Jira

extends_documentation_fragment:
  - jira_modules_common

options:
  username:
    required: true
    description:
      - The name of the user.
      - Cannot be updated.

  group_name:
    required: true
    description:
      - The name of the group.
      - Cannot be updated.

author: "Joe Topjian <joe@topjian.net>"
"""

RETURN = """
Does not return anything.
"""

EXAMPLES = """
- name: Ensure user is a member of group
  jira_user_group_membership:
    username: user_1
    group_name: group_1
"""

REST_ENDPOINT_CREATE = "rest/api/2/group/user"
REST_ENDPOINT_DELETE = "rest/api/2/group/user"
REST_ENDPOINT_GET = "rest/api/2/group/member"
REST_ENDPOINT_USER_GET = "rest/api/2/user"


class JiraUserGroupMembership(JiraModuleBase):
    """Utility class to manage a Jira user's membership in a group"""

    def __init__(self):
        self.module_args = dict(
            username=dict(required=True),
            group_name=dict(required=True),
            state=dict(
                required=False,
                default='present',
                choices=['absent', 'present']),
        )

        self.results = dict(
            jira_user_group_membership=dict(),
            changed=False,
        )

        super(JiraUserGroupMembership, self).__init__(
            derived_arg_spec=self.module_args,
            rest_endpoint=REST_ENDPOINT_GET,
        )

    def exec_module(self, **kwargs):
        action = None
        is_install_mode = self.param('state') == 'present'

        group_query = {}
        group_name = self.param('group_name')
        group_query['groupname'] = group_name

        user_query = {}
        username = self.param('username')
        user_query['username'] = username

        group_query = urlencode(group_query)
        user_query = urlencode(user_query)

        try:
            # NOTE: future issue if more than 50 users in a group.
            self.rest_endpoint = REST_ENDPOINT_GET
            group = self.get(group_query)
            if group is False:
                self.fail("Jira group %s does not exist" % (group_name))

            self.rest_endpoint = REST_ENDPOINT_USER_GET
            user = self.get(user_query)
            if user is False:
                self.fail("Jira user %s does not exist" % (username))

            user_exists = False
            if 'values' in group:
                for user in group['values']:
                    if user['name'] == username:
                        user_exists = True

            if not is_install_mode:
                if user_exists is False:
                    return
                action = 'deleted'
            else:
                if user_exists is False:
                    action = 'created'

            self.results['jira_user_group_membership_action'] = action
            if action is not None:
                self.results['changed'] = True

            if self.check_mode:
                return

            if action == 'created':
                data = {
                    'name': username,
                }

                self.rest_endpoint = REST_ENDPOINT_CREATE
                self.post(data, query=group_query)
                return

            if action == 'deleted':
                delete_query = {
                    'groupname': group_name,
                    'username': username,
                }
                self.rest_endpoint = REST_ENDPOINT_DELETE
                self.delete(urlencode(delete_query))
                return

        except Exception as e:
            self.fail(msg=e.message)


if __name__ == '__main__':
    JiraUserGroupMembership()
