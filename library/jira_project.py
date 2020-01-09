#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.jira_common import JiraModuleBase
from ansible.module_utils.six.moves.urllib.parse import urlencode

__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = """
module: jira_project
version_added: "0.0.1"
short_description: manage a project in Jira
description:
  - Manage a project in Jira

extends_documentation_fragment:
  - jira_modules_common

options:
  name:
    required: true
    description:
      - The name of the project.
      - Cannot be updated.

  key:
    required: true
    description:
      - The Jira key for the project.
      - Cannot be updated.

  project_type_key:
    required: false
    description:
      - The Jira key for the project type.
      - Cannot be updated.
      - This paramter is mutally exclusive with C(project_template_key).

  project_template_key:
    required: false
    description:
      - The Jira key for the project template.
      - There is no way to poll Jira for templates via the API. The following
        are a reference.
      - software
      - com.pyxis.greenhopper.jira:gh-scrum-template
      - com.pyxis.greenhopper.jira:gh-kanban-template
      - com.pyxis.greenhopper.jira:basic-software-development-template
      - business
      - com.atlassian.jira-core-project-templates:jira-core-project-management
      - com.atlassian.jira-core-project-templates:jira-core-task-management
      - com.atlassian.jira-core-project-templates:jira-core-process-management
      - service Desk
      - com.atlassian.servicedesk:classic-service-desk-project
      - com.atlassian.servicedesk:itil-service-desk-project
      - Cannot be updated.
      - This paramter is mutally exclusive with C(project_type_key).

  description:
    required: false
    description:
      - A description of the project.
      - Can be updated.

  lead:
    required: true
    description:
      - A username of the project lead.
      - Can be updated.

  url:
    required: false
    description:
      - A URL for the project.
      - Can be updated.

  avatar_id:
    required: false
    description:
      - The ID of the avatar to use.
      - Can be updated.

  issue_security_scheme:
    required: false
    description:
      - The ID of the issue security scheme to use.
      - Can be updated.

  permission_scheme:
    required: false
    description:
      - The ID of the permission scheme to use.
      - Can be updated.

  notification_scheme:
    required: false
    description:
      - The ID of the notification scheme to use.
      - Can be updated.

  workflow_scheme_id:
    required: false
    description:
      - The ID of the workflow scheme to use.
      - Can be not updated.

  category_id:
    required: false
    description:
      - The ID of the category to use.
      - Can be updated.

author: "Joe Topjian <joe@topjian.net>"
"""

RETURN = """
jira_project:
  type: dict
  description:
    - A Jira project.
    - See
      https://docs.atlassian.com/software/jira/docs/api/REST/8.6.0/#api/2/project-getProject
      for the schema.
  returned: When a Jira project was detected.
"""

EXAMPLES = """
- name: Ensure project exists
  jira_project:
    name: project_1
"""

REST_ENDPOINT = "rest/api/2/project"


class JiraProject(JiraModuleBase):
    """Utility class to manage a Jira project"""

    def __init__(self):
        self.module_args = dict(
            name=dict(
                required=True,
                _jira_field='name',
                _jira_update=False),

            key=dict(
                required=True,
                _jira_field='key',
                _jira_update=False),

            project_type_key=dict(
                _jira_field='projectTypeKey',
                _jira_update=False),

            project_template_key=dict(
                _jira_field='projectTemplateKey',
                _jira_update=False),

            description=dict(
                _jira_field='description',
                _jira_update=True),

            lead=dict(
                required=True,
                _jira_field='lead',
                _jira_update=True),

            url=dict(
                _jira_field='url',
                _jira_update=True),

            avatar_id=dict(
                type='int',
                _jira_field='avatarId',
                _jira_update=True),

            issue_security_scheme=dict(
                type='int',
                _jira_field='issueSecurityScheme',
                _jira_update=True),

            permission_scheme=dict(
                type='int',
                _jira_field='permissionScheme',
                _jira_update=True),

            notification_scheme=dict(
                type='int',
                _jira_field='notificationScheme',
                _jira_update=True),

            workflow_scheme_id=dict(
                type='int',
                _jira_field='workflowSchemeId',
                _jira_update=False),

            category_id=dict(
                _jira_field='categoryId',
                _jira_update=True),

            state=dict(
                required=False,
                default='present',
                choices=['absent', 'present']),
        )

        self.results = dict(
            jira_project=dict(),
            changed=False,
        )

        super(JiraProject, self).__init__(
            derived_arg_spec=self.module_args,
            mutually_exclusive=[['project_type_key', 'project_template_key']],
            required_one_of=[['project_type_key', 'project_template_key']],
            rest_endpoint=REST_ENDPOINT,
        )

    def exec_module(self, **kwargs):
        action = None
        is_install_mode = self.param('state') == 'present'

        q = {
            'expand': ','.join(['description', 'lead', 'url', 'projectKeys'])
        }
        query = urlencode(q)

        update_dict = {}

        project_endpoint = "%s/%s" % (REST_ENDPOINT, self.param('key'))

        try:
            self.rest_endpoint = project_endpoint
            project = self.get(query)

            if not is_install_mode:
                if project is False:
                    return
                action = 'deleted'
            else:
                if project is False:
                    action = 'created'
                else:
                    # Detect updates
                    for (v, jira_field) in self.jira_update_fields():
                        if jira_field in project:
                            if jira_field == "lead":
                                lead = self.param(v)
                                _lead = project[jira_field]['name']
                                if lead != _lead:
                                    update_dict[jira_field] = lead
                                    update_dict['assigneeType'] = \
                                        'PROJECT_LEAD'
                                continue

                            if jira_field == "description":
                                desc = self.param(v)
                                _desc = project[jira_field]
                                if desc is None and _desc == "":
                                    continue
                                if desc != _desc:
                                    if _desc is None:
                                        update_dict[jira_field] = ""
                                    else:
                                        update_dict[jira_field] = self.param(v)
                                continue

                            if self.param(v) != project[jira_field]:
                                update_dict[jira_field] = self.param(v)

                        if v == "workflow_scheme_id":
                            if self.param(v) is None:
                                continue

                            self.rest_endpoint = "%s/%s/workflowscheme" % (
                                REST_ENDPOINT, self.param('key'))
                            workflow_scheme = self.get()
                            workflow_scheme_id = workflow_scheme['id']
                            if self.param(v) != workflow_scheme_id:
                                update_dict[jira_field] = self.param(v)

                        if v == "issue_security_scheme":
                            if self.param(v) is None:
                                continue
                            self.rest_endpoint = \
                                "%s/%s/issuesecuritylevelscheme" % (
                                    REST_ENDPOINT, self.param('key'))
                            iss = self.get()
                            iss_id = iss['id']
                            if self.param(v) != iss_id:
                                update_dict[jira_field] = self.param(v)

                        if v == "notification_scheme":
                            if self.param(v) is None:
                                continue
                            self.rest_endpoint = \
                                "%s/%s/notificationscheme" % (
                                    REST_ENDPOINT, self.param('key'))
                            ns = self.get()
                            ns_id = ns['id']
                            if self.param(v) != ns_id:
                                update_dict[jira_field] = self.param(v)

                        if v == "permission_scheme":
                            if self.param(v) is None:
                                continue
                            self.rest_endpoint = \
                                "%s/%s/permissionscheme" % (
                                    REST_ENDPOINT, self.param('key'))
                            ps = self.get()
                            ps_id = ps['id']
                            if self.param(v) != ps_id:
                                update_dict[jira_field] = self.param(v)

                    if len(update_dict) > 0:
                        action = 'updated'

            self.results['jira_project_action'] = action
            self.results['jira_project'] = project
            if action is not None:
                self.results['changed'] = True

            if self.check_mode:
                return

            if action == 'created':
                data = {}
                for (v, jira_field) in self.jira_fields():
                    if self.param(v):
                        data[jira_field] = self.param(v)
                data['assigneeType'] = 'PROJECT_LEAD'

                self.rest_endpoint = REST_ENDPOINT
                self.post(data)

                self.rest_endpoint = project_endpoint
                project = self.get(query)
                self.results['jira_project'] = project
                return

            if action == 'updated':
                self.rest_endpoint = project_endpoint
                project = self.put(update_dict)
                project = self.get(query)
                self.results['jira_project'] = project
                return

            if action == 'deleted':
                self.rest_endpoint = project_endpoint
                self.delete()
                return

        except Exception as e:
            self.fail(msg=e.message)


if __name__ == '__main__':
    JiraProject()
