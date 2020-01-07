#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.jira_common import JiraModuleBase
from ansible.module_utils.six.moves.urllib.parse import urlencode

__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = """
module: jira_user
version_added: "0.0.1"
short_description: manage a user in Jira
description:
  - Manage a user in Jira

extends_documentation_fragment:
  - jira_modules_common

options:
  username:
    required: true
    description:
      - The name of the user.
      - Cannot be updated.

  key:
    required: false
    description:
      - Reference a user via Jira key.
      - Cannot be updated.

  password:
    required: false
    description:
      - The password for the user.
      - Cannot be updated.

  email_address:
    required: false
    description:
      - The email address for the user.
      - Can be updated.

  display_name:
    required: false
    description:
      - The email address for the user.
      - Can be updated.

  active:
    required: false
    type: bool
    description:
      - Set the active status of the user.
      - Can be updated.
    default: true

  application_keys:
    required: false
    type: list
    description:
      - A list of applications the user has access to.
      - Can be updated.
    default: ['jira-core']


author: "Joe Topjian <joe@topjian.net>"
"""

RETURN = """
jira_user:
  type: dict
  description:
    - A Jira user.
    - See
      https://docs.atlassian.com/software/jira/docs/api/REST/8.6.0/#api/2/user-getUser
      for the schema.
  returned: When a Jira user was detected.
"""

EXAMPLES = """
- name: Ensure admin exists
  jira_user:
    username: 'admin'
    password: 'password'
    email_address: 'admin@example.com'
    display_name: 'Admin User'
    application_keys:
      - 'jira-core'
"""

REST_ENDPOINT = "rest/api/2/user"


class JiraUser(JiraModuleBase):
    """Utility class to manage a Jira user"""

    def __init__(self):
        self.module_args = dict(
            username=dict(required=True),
            key=dict(),
            password=dict(no_log=True),
            email_address=dict(),
            display_name=dict(),
            application_keys=dict(type='list', default=['jira-core']),
            active=dict(type='bool', default=True),
            state=dict(
                required=False,
                default='present',
                choices=['absent', 'present']),
        )

        self.results = dict(
            jira_user=dict(),
            changed=False,
        )

        super(JiraUser, self).__init__(
            derived_arg_spec=self.module_args,
            rest_endpoint=REST_ENDPOINT,
        )

    def exec_module(self, **kwargs):
        action = None
        is_install_mode = self.param('state') == 'present'

        query = {}
        update_dict = {}
        username = self.param('username')

        v = self.param('key')
        if v is not None:
            query['key'] = v
        else:
            if username is not None:
                query['username'] = username

        query['expand'] = 'groups,applicationRoles'
        query = urlencode(query)

        try:
            # Try to get the resource
            user = self.get(query)

            if not is_install_mode:
                if user is False:
                    return
                action = 'deleted'
            else:
                if user is False:
                    action = 'created'
                else:
                    self.results['jira_user'] = user

                    display_name = self.param('display_name')
                    _display_name = user['displayName']

                    if display_name != _display_name:
                        update_dict['displayName'] = display_name

                    email_address = self.param('email_address')
                    _email_address = user['emailAddress']
                    if email_address != _email_address:
                        update_dict['emailAddress'] = email_address

                    active = self.param('active')
                    _active = user['active']
                    if active != _active:
                        update_dict['active'] = active

                    application_keys = self.param('application_keys')
                    _application_roles = user['applicationRoles']
                    _application_keys = []
                    if 'items' in _application_roles:
                        for item in _application_roles['items']:
                            _application_keys.append(item['key'])

                    if set(application_keys) != set(_application_keys):
                        update_dict['application_keys'] = application_keys

                    if len(update_dict) > 0:
                        action = 'updated'

            self.results['jira_user_action'] = action
            self.results['jira_user'] = user
            if action is not None:
                self.results['changed'] = True

            if self.check_mode:
                return

            if action == 'created':
                data = {
                    'name': username,
                    'emailAddress': self.param('email_address'),
                    'displayName': self.param('display_name'),
                    'applicationKeys': self.param('application_keys'),
                }

                self.post(data)
                user = self.get(query)
                self.results['jira_user'] = user
                return

            if action == 'updated':
                self.put(update_dict, query=query)
                user = self.get(query)
                self.results['jira_user'] = user
                return

            if action == 'deleted':
                self.delete(query)
                return

        except Exception as e:
            self.fail(msg=e.message)


if __name__ == '__main__':
    JiraUser()
