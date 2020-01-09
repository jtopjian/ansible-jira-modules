#!/usr/bin/python
# -*- coding: utf-8 -*-

from ansible.module_utils.jira_common import JiraModuleBase

__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = """
module: jira_project_category
version_added: "0.0.1"
short_description: manage a project category in Jira
description:
  - Manage a project category in Jira

extends_documentation_fragment:
  - jira_modules_common

options:
  name:
    required: true
    description:
      - The name of the project category.
      - Cannot be updated.

  descriptioon:
    required: false
    description:
      - The description of the project category
      - Can be updated.

author: "Joe Topjian <joe@topjian.net>"
"""

RETURN = """
jira_project:
  type: dict
  description:
    - A Jira project.
    - See
      https://docs.atlassian.com/software/jira/docs/api/REST/8.6.0/#api/2/projectCategory-getProjectCategoryById
      for the schema.
  returned: When a Jira project category was detected.
"""

EXAMPLES = """
- name: Ensure project category exists
  jira_project_category:
    name: Internal Projects
    description: A category for internal projects
"""

REST_ENDPOINT = "rest/api/2/projectCategory"


class JiraProjectCategory(JiraModuleBase):
    """Utility class to manage a Jira project category"""

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
            jira_project_category=dict(),
            changed=False,
        )

        super(JiraProjectCategory, self).__init__(
            derived_arg_spec=self.module_args,
            rest_endpoint=REST_ENDPOINT,
        )

    def find_id(self):
        self.rest_endpoint = REST_ENDPOINT
        cats = self.get()
        name = self.param('name')

        id = None
        for cat in cats:
            if cat["name"] == name:
                id = cat["id"]

        return id

    def exec_module(self, **kwargs):
        action = None
        is_install_mode = self.param('state') == 'present'

        update_dict = {}

        try:
            id = self.find_id()
            if id is None:
                pcat = False
            else:
                self.rest_endpoint = "%s/%s" % (REST_ENDPOINT, id)
                pcat = self.get()

            if not is_install_mode:
                if pcat is False:
                    return
                action = 'deleted'
            else:
                if pcat is False:
                    action = 'created'
                else:
                    # Detect updates
                    for (v, jira_field) in self.jira_update_fields():
                        if jira_field in pcat:
                            if self.param(v) != pcat[jira_field]:
                                update_dict[jira_field] = self.param(v)

                    if len(update_dict) > 0:
                        action = 'updated'

            self.results['jira_project_category_action'] = action

            if pcat is False:
                del(self.results['jira_project_category'])
            else:
                self.results['jira_project_category'] = pcat

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
                pcat = self.post(data)
                self.results['jira_project_category'] = pcat
                return

            if action == 'updated':
                id = self.find_id()
                if id is None:
                    self.fail("Unable to find Jira project category %s" % (
                        self.param('name')))
                self.rest_endpoint = "%s/%s" % (REST_ENDPOINT, id)
                pcat = self.put(update_dict)
                pcat = self.get()
                self.results['jira_project_category'] = pcat
                return

            if action == 'deleted':
                id = self.find_id()
                if id is None:
                    self.fail("Unable to find Jira project category %s" % (
                        self.param('name')))
                self.rest_endpoint = "%s/%s" % (REST_ENDPOINT, id)
                self.delete()
                return

        except Exception as e:
            self.fail(msg=e.message)


if __name__ == '__main__':
    JiraProjectCategory()
