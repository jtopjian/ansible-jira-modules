#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.jira_common import JiraModuleBase
from ansible.module_utils.six.moves.urllib.parse import urlencode

__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = """
module: jira_list_notification_schemes_fact
version_added: "0.0.1"
short_description: list notification schemes in Jira
description:
  - List notification schemes in Jira

extends_documentation_fragment:
  - jira_modules_common

author: "Joe Topjian <joe@topjian.net>"
"""

RETURN = """
ansible_facts:
  description: facts to add to ansible_facts
  returned: always
  type: complex
  contains:
    jira_notification_schemes:
      type: list
      description:
        - Maps Jira notification schemes to a non-empty list of dicts with
          notification schemes information.
        - See
          https://docs.atlassian.com/software/jira/docs/api/REST/8.6.0/#api/2/notificationscheme-getNotificationSchemes
          for the schema.
      returned: When Jira notification schemes are detected.
"""

EXAMPLES = """
- name: List Notification Schemes
  jira_list_notification_schemes_fact:
"""

REST_ENDPOINT = "rest/api/2/notificationscheme"


class JiraListNotificationSchemes(JiraModuleBase):
    """Utility class to get list of Jira notification schemes as facts"""

    def __init__(self):
        self.module_args = dict()

        self.results = dict(
            ansible_facts=dict(
                jira_notification_schemes=[],
            ),
            changed=False,
        )

        super(JiraListNotificationSchemes, self).__init__(
            derived_arg_spec=self.module_args,
            facts_module=True,
            rest_endpoint=REST_ENDPOINT,
        )

    def exec_module(self, **kwargs):
        query = {
            'expand': 'all',
        }

        try:
            v = self.get(urlencode(query))
            if v is False:
                del(self.results['ansible_facts']['jira_notification_schemes'])
            else:
                self.results['ansible_facts']['jira_notification_schemes'] = v
        except Exception as e:
            self.fail(msg=e.message)


if __name__ == '__main__':
    JiraListNotificationSchemes()
