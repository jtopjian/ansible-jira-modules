#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.jira_common import JiraModuleBase
from ansible.module_utils.six.moves.urllib.parse import urlencode

__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = """
module: jira_group
version_added: "0.0.1"
short_description: manage a group in Jira
description:
  - Manage a group in Jira

extends_documentation_fragment:
  - jira_modules_common

options:
  group_name:
    required: true
    description:
      - The name of the group.
      - Cannot be updated.

author: "Joe Topjian <joe@topjian.net>"
"""

RETURN = """
jira_group:
  type: dict
  description:
    - A Jira group.
    - See
      https://docs.atlassian.com/software/jira/docs/api/REST/8.6.0/#api/2/group-getUsersFromGroup
      for the schema.
  returned: When a Jira group was detected.
"""

EXAMPLES = """
- name: Ensure group exists
  jira_group:
    group_name: group_1
"""

REST_ENDPOINT_CREATE = "rest/api/2/group"
REST_ENDPOINT_DELETE = "rest/api/2/group"
REST_ENDPOINT_GET = "rest/api/2/group/member"


class JiraGroup(JiraModuleBase):
    """Utility class to manage a Jira group"""

    def __init__(self):
        self.module_args = dict(
            group_name=dict(required=True),
            state=dict(
                required=False,
                default='present',
                choices=['absent', 'present']),
        )

        self.results = dict(
            jira_group=dict(),
            changed=False,
        )

        super(JiraGroup, self).__init__(
            derived_arg_spec=self.module_args,
            rest_endpoint=REST_ENDPOINT_CREATE,
        )

    def exec_module(self, **kwargs):
        action = None
        is_install_mode = self.param('state') == 'present'

        query = {}
        group_name = self.param('group_name')

        v = self.param('group_name')
        if v is not None:
            query['groupname'] = v

        query = urlencode(query)

        try:
            self.rest_endpoint = REST_ENDPOINT_GET
            group = self.get(query)

            if not is_install_mode:
                if group is False:
                    return
                action = 'deleted'
            else:
                if group is False:
                    action = 'created'

            self.results['jira_group_action'] = action
            self.results['jira_group'] = group
            if action is not None:
                self.results['changed'] = True

            if self.check_mode:
                return

            if action == 'created':
                data = {
                    'name': group_name,
                }

                self.rest_endpoint = REST_ENDPOINT_CREATE
                self.post(data)

                self.rest_endpoint = REST_ENDPOINT_GET
                group = self.get(query)
                self.results['jira_group'] = group
                return

            if action == 'deleted':
                self.rest_endpoint = REST_ENDPOINT_DELETE
                self.delete(query)
                return

        except Exception as e:
            self.fail(msg=e.message)


if __name__ == '__main__':
    JiraGroup()
