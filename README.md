Ansible Jira Modules
=====================

Ansible modules for interacting with Jira.

Example Playbook
----------------

Fact Examples

    - hosts: localhost
      roles:
        - jtopjian.jira
      tasks:
        - name: List all groups
          jira_list_groups_fact:

        - name: List all issue security schemes
          jira_list_issue_security_schemes_fact:

        - name: List all issue types
          jira_list_issue_types_fact:

        - name: List all notification schemes
          jira_list_notification_schemes_fact:

        - name: List all project categories
          jira_list_project_categories_fact:

        - name: List all projects
          jira_list_projects_fact:

        - name: List all project types
          jira_list_project_types_fact:

        - name: List all roles
          jira_list_roles_fact:

        - name: List all users
          jira_list_users_fact:

        - name: List all workflow schemes
          jira_list_workflow_schemes_fact:

        - name: List all project types
          jira_list_project_types_fact:

        - name: Get a group
          jira_get_user_fact:
            name: jira-administrators

        - name: Get an issue type
          jira_get_issue_type_fact:
            issue_type_id: 10000

        - name: Get a notification scheme
          jira_get_notification_scheme_fact:
            id: 10000

        - name: Get a permission scheme
          jira_get_permission_scheme_fact:
            id: 10000

        - name: Get a project
          jira_get_project_fact:
            key: PROJ

        - name: Get a project type
          jira_get_project_type_fact:
            key: business

        - name: Get a role
          jira_get_role_fact:
            name: Administrators

        - name: Get a user
          jira_get_user_fact:
            username: admin

        - name: Get a workflow scheme
          jira_get_workflow_scheme_fact:
            id: 10000

User Management Example

    - host: localhost
      roles:
        - jtopjian.jira
      tasks:
        - name: Manage a User
          jira_user:
            username: jdoe
            email_address: jdoe@example.com
            password: password
            display_name: John Doe

        - name: Delete a user
          jira_user:
            username: jdoe
            state: absent

Group Management Example

    - host: localhost
      roles:
        - jtopjian.jira
      tasks:
        - name: Manage a Group
          jira_group:
            name: group_1

        - name: Delete a Group
          jira_group:
            name: group_1
            state: absent


Group Membership Example

    - host: localhost
      roles:
        - jtopjian.jira
      tasks:
        - name: Ensure a user is in a group
          jira_user_group_membership:
            group_name: group_1
            username: jdoe

        - name: Ensure a user is not in a group
          jira_user_group_membership:
            group_name: group_1
            username: jdoe
            state: absent

Project Management Example

    - host: localhost
      roles:
        - jtopjian.jira
      tasks:
        - name: Ensure a project exists
          jira_project:
            name: Project 1
            key: PRJ1
            project_key_type: business
            lead: admin

        - name: Ensure a project does not exist
          jira_project:
            name: Project 1
            key: PRJ1
            project_key_type: business
            lead: admin
            state: absent

Project Category Management Example

    - host: localhost
      roles:
        - jtopjian.jira
      tasks:
        - name: Ensure a project category exists
          jira_project_category:
            name: Project Category 1
            description: A project category

        - name: Ensure a project category does not exist
          jira_project_category:
            name: Project Category 1
            state: absent

Documentation
-------------

See [docs](docs).

License
-------

Apache 2.0

Author Information
------------------

Joe Topjian <joe@topjian.net>
