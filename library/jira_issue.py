#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.jira_common import JiraModuleBase

__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = """
module: jira_issue
version_added: "0.0.1"
short_description: manage a issue in Jira
description:
  - Manage a issue in Jira
  - This is a VERY simple representation of a Jira issue.
  - States and transitions are not supported yet.

extends_documentation_fragment:
  - jira_modules_common

options:
  key:
    required: false
    description:
      - The Jira key to use for referencing an existing issue.
      - Cannot be updated.

  summary:
    required: true
    description:
      - The summary/name of the issue

  issue_type:
    required: true
    description:
      - The issue type of the issue.

  project_key:
    required: true
    description:
      - The Jira key of the project.
      - Cannot be updated

  assignee:
    required: false
    description:
      - The Jira user assigned to the issue.

  reporter:
    required: false
    description:
      - The Jira user who reported the issue.

  description:
    required: false
    description:
      - The description/contents of the issue.

author: "Joe Topjian <joe@topjian.net>"
"""

RETURN = """
jira_issue:
  type: dict
  description:
    - A Jira issue.
    - See
      https://docs.atlassian.com/software/jira/docs/api/REST/8.6.0/#api/2/issue-getIssue
      for the schema.
  returned: When a Jira issue was detected.
"""

EXAMPLES = """
- name: Ensure issue exists
  jira_issue:
    summary: Test Issue
    issue_type: Task
    project_key: PRJ1
    description: This is an issue
"""

REST_ENDPOINT = "rest/api/2/issue"


class JiraProject(JiraModuleBase):
    """Utility class to manage a Jira issue"""

    def __init__(self):
        self.module_args = dict(
            assignee=dict(
                _jira_field='assignee',
                _jira_update=True),

            description=dict(
                _jira_field='description',
                _jira_update=True),

            issue_type=dict(
                _jira_field='issuetype',
                _jira_update=True),

            key=dict(
                required=False,
                _jira_field='key',
                _jira_update=False),

            project_key=dict(
                required=True,
                _jira_field='project',
                _jira_update=False),

            reporter=dict(
                _jira_field='reporter',
                _jira_update=True),

            summary=dict(
                required=True,
                _jira_field='summary',
                _jira_update=True),

            state=dict(
                required=False,
                default='present',
                choices=['absent', 'present']),
        )

        self.results = dict(
            jira_issue=dict(),
            changed=False,
        )

        super(JiraProject, self).__init__(
            derived_arg_spec=self.module_args,
            rest_endpoint=REST_ENDPOINT,
        )

    def exec_module(self, **kwargs):
        action = None
        is_install_mode = self.param('state') == 'present'

        create_dict = {
            'fields': dict(),
        }

        update_dict = {
            'fields': dict(),
        }

        issue_endpoint = "%s/%s" % (REST_ENDPOINT, self.param('key'))

        try:
            self.rest_endpoint = issue_endpoint
            if self.param('key') is not None:
                issue = self.get()
            else:
                issue = False

            if not is_install_mode:
                if issue is False:
                    return
                action = 'deleted'
            else:
                if issue is False:
                    action = 'created'

                    for (v, jira_field) in self.jira_fields():
                        if jira_field == 'assignee':
                            if self.param(v) is not None:
                                create_dict['fields'][jira_field] = {
                                    'name': self.param(v),
                                }

                        if jira_field == 'description':
                            if self.param(v) is not None:
                                create_dict['fields'][jira_field] = \
                                    self.param(v)

                        if jira_field == 'issuetype':
                            if self.param(v) is not None:
                                create_dict['fields'][jira_field] = {
                                    'name': self.param(v),
                                }

                        if jira_field == 'project':
                            if self.param(v) is not None:
                                create_dict['fields']['project'] = {
                                    'key': self.param(v),
                                }

                        if jira_field == 'reporter':
                            if self.param(v) is not None:
                                create_dict['fields'][jira_field] = {
                                    'name': self.param(v),
                                }

                        if jira_field == 'summary':
                            if self.param(v) is not None:
                                create_dict['fields']['summary'] = \
                                    self.param(v)

                else:
                    # Detect updates
                    for (v, jira_field) in self.jira_update_fields():
                        if jira_field in issue:
                            if jira_field == 'assignee':
                                asn = self.param(v)
                                _asn = issue[jira_field]['name']
                                if asn != _asn:
                                    update_dict['fields'][jira_field] = {
                                        'name': asn
                                    }
                                continue

                            if jira_field == "description":
                                desc = self.param(v)
                                _desc = issue[jira_field]
                                if desc is None and _desc == "":
                                    continue
                                if desc != _desc:
                                    if _desc is None:
                                        update_dict['fields'][jira_field] = ""
                                    else:
                                        update_dict['fields'][jira_field] = \
                                            self.param(v)
                                continue

                            if jira_field == 'issueType':
                                it = self.param(v)
                                _it = issue[jira_field]['name']
                                if it != _it:
                                    update_dict['fields'][jira_field] = {
                                        'name': it,
                                    }
                                continue

                            if jira_field == 'reporter':
                                asn = self.param(v)
                                _asn = issue[jira_field]['name']
                                if asn != _asn:
                                    update_dict['fields'][jira_field] = {
                                        'name': asn,
                                    }
                                continue

                            if self.param(v) != issue[jira_field]:
                                update_dict['fields'][jira_field] = \
                                    self.param(v)

                    if len(update_dict['fields']) > 0:
                        action = 'updated'

            self.results['jira_issue_action'] = action
            self.results['jira_issue'] = issue
            if action is not None:
                self.results['changed'] = True

            if self.check_mode:
                return

            if action == 'created':
                self.rest_endpoint = REST_ENDPOINT
                issue = self.post(create_dict)
                self.results['jira_issue'] = issue
                if 'key' in issue:
                    key = issue['key']
                    issue_endpoint = "%s/%s" % (REST_ENDPOINT, key)
                    self.rest_endpoint = issue_endpoint
                    issue = self.get()
                    self.results['jira_issue'] = issue

                return

            if action == 'updated':
                self.rest_endpoint = issue_endpoint
                issue = self.put(update_dict)
                issue = self.get()
                self.results['jira_issue'] = issue
                return

            if action == 'deleted':
                self.rest_endpoint = issue_endpoint
                self.delete()
                return

        except Exception as e:
            self.fail(msg=e.message)


if __name__ == '__main__':
    JiraProject()
