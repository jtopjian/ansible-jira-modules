#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.jira_common import JiraModuleBase
from ansible.module_utils.six.moves.urllib.parse import urlencode

__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = """
module: jira_workflow_scheme
version_added: "0.0.1"
short_description: manage a workflow scheme in Jira
description:
  - Manage a workflow scheme in Jira

extends_documentation_fragment:
  - jira_modules_common

options:
  name:
    required: true
    description:
      - The name of the workflow scheme.

  description:
    required: false
    description:
      - The description of the workflow scheme

  id:
    required: false
    type: int
    description:
      - An integer ID for the workflow scheme.
      - An existing workflow scheme can only be updated
        and deleted by an ID. Therefore, the workflow
        scheme ID needs to be recorded / hard-coded
        at some point in its lifecycle.
      - Cannot be updated.

  default_workflow:
    required: false
    description:
      - The ID of the workflow to use as the default workflow.

  issue_type_mappings:
    required: false
    type: dict
    description:
      - Issue mappings for the workflow scheme.

author: "Joe Topjian <joe@topjian.net>"
"""

RETURN = """
jira_workflow_scheme:
  type: dict
  description:
    - A Jira workflow scheme.
    - See
      https://docs.atlassian.com/software/jira/docs/api/REST/8.6.0/#api/2/workflowscheme-getById
      for the schema.
  returned: When a Jira workflow scheme was detected.
"""

EXAMPLES = """
- name: Ensure workflow scheme exists
  jira_workflow_scheme:
    name: workflow_scheme_1
"""

REST_ENDPOINT = "rest/api/2/workflowscheme"


class JiraProject(JiraModuleBase):
    """Utility class to manage a Jira workflow scheme"""

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

            id=dict(
                type='int',
                _jira_field='id',
                _jira_update=False),

            default_workflow=dict(
                _jira_field='defaultWorkflow',
                _jira_update=True),

            issue_type_mappings=dict(
                type='dict',
                _jira_field='issueTypeMappings',
                _jira_update=True),

            state=dict(
                required=False,
                default='present',
                choices=['absent', 'present']),
        )

        self.results = dict(
            jira_workflow_scheme=dict(),
            changed=False,
        )

        super(JiraProject, self).__init__(
            derived_arg_spec=self.module_args,
            rest_endpoint=REST_ENDPOINT,
        )

    def exec_module(self, **kwargs):
        action = None
        is_install_mode = self.param('state') == 'present'

        #update_dict = {}

        workflow_scheme_endpoint = "%s/%s" % (REST_ENDPOINT, self.param('id'))

        try:
            self.rest_endpoint = workflow_scheme_endpoint
            workflow_scheme = self.get()

            if not is_install_mode:
                if workflow_scheme is False:
                    return
                action = 'deleted'
            else:
                if workflow_scheme is False:
                    action = 'created'
                #else:
                #    # Detect updates
                #    for (v, jira_field) in self.jira_update_fields():
                #        if self.param(v) != workflow_scheme[jira_field]:
                #            update_dict[jira_field] = self.param(v)
                #
                #    if len(update_dict) > 0:
                #        action = 'updated'

            self.results['jira_workflow_scheme_action'] = action

            if workflow_scheme is False:
                del(self.results['jira_workflow_scheme'])
            else:
                self.results['jira_workflow_scheme'] = workflow_scheme

            if action is not None:
                self.results['changed'] = True

            if self.check_mode:
                return

            if action == 'created':
                data = {}
                for (v, jira_field) in self.jira_fields():
                    if v == "id":
                        continue
                    if self.param(v):
                        data[jira_field] = self.param(v)

                self.rest_endpoint = REST_ENDPOINT
                workflow_scheme = self.post(data)
                self.results['jira_workflow_scheme'] = workflow_scheme
                return

            # Update isn't supported yet
            #if action == 'updated':
            #    self.rest_endpoint = workflow_scheme_endpoint
            #    workflow_scheme = self.put(urlencode(update_dict))
            #    self.results['jira_workflow_scheme'] = workflow_scheme
            #    return

            if action == 'deleted':
                self.rest_endpoint = workflow_scheme_endpoint
                self.delete()
                return

        except Exception as e:
            self.fail(msg=e.message)


if __name__ == '__main__':
    JiraProject()
