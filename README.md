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

        - name: List all projects
          jira_list_projects_fact:

        - name: List all users
          jira_list_users_fact:

        - name: Get a group
          jira_get_user_fact:
            group_name: jira-administrators

        - name: Get a project
          jira_get_project_fact:
            key: PROJ

        - name: Get a user
          jira_get_user_fact:
            username: admin

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
            group_name: group_1

        - name: Delete a Group
          jira_group:
            group_name: group_1
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


Documentation
-------------

See [docs](docs).

License
-------

Apache 2.0

Author Information
------------------

Joe Topjian <joe@topjian.net>
