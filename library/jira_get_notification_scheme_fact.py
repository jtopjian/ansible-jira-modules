#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.jira_common import JiraModuleBase
from ansible.module_utils.six.moves.urllib.parse import quote, urlencode

__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = """
module: jira_get_notification_scheme_fact
version_added: "0.0.1"
short_description: list notification schemes in Jira
description:
  - Get a notification scheme in Jira

extends_documentation_fragment:
  - jira_modules_common

options:
  key:
    required: true
    description:
      - The Jira key of the notification scheme

author: "Joe Topjian <joe@topjian.net>"
"""

RETURN = """
ansible_facts:
  description: facts to add to ansible_facts
  returned: always
  type: complex
  contains:
    jira_notification_scheme:
      type: dict
      description:
        - A Jira notification scheme.
        - See
          https://docs.atlassian.com/software/jira/docs/api/REST/8.6.0/#api/2/notificationscheme-getNotificationScheme
          for the schema.
      returned: When a Jira notification scheme is detected.
"""

EXAMPLES = """
- name: Get a notification scheme
  jira_get_notification_scheme_fact:
    id: 10000
"""

REST_ENDPOINT = "rest/api/2/notificationscheme"


class JiraGetNotificationScheme(JiraModuleBase):
    """Utility class to get a Jira notification scheme fact"""

    def __init__(self):
        self.module_args = dict(
            id=dict(required=True),
        )

        self.results = dict(
            ansible_facts=dict(
                jira_notification_scheme="",
            ),
            changed=False,
        )

        super(JiraGetNotificationScheme, self).__init__(
            derived_arg_spec=self.module_args,
            facts_module=True,
            rest_endpoint=REST_ENDPOINT,
        )

    def exec_module(self, **kwargs):
        id = self.param('id')
        self.rest_endpoint = "%s/%s" % (self.rest_endpoint, quote(id))

        query = {
            'expand': 'all',
        }

        try:
            v = self.get(urlencode(query))
            if v is False:
                del(self.results['ansible_facts']['jira_notification_scheme'])
            else:
                self.results['ansible_facts']['jira_notification_scheme'] = v
        except Exception as e:
            self.fail(msg=e.message)


if __name__ == '__main__':
    JiraGetNotificationScheme()
