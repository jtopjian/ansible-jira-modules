Ansible Jira Modules
=====================

Ansible modules for interacting with Jira.

Example Playbook
----------------

Example playbook

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

Variables / Arguments / Parameters
-----------------------------------------------

### Shared

Each module shares the following parameters:

* `jira_url`: The URL to the Jira server.
  Can also be set with JIRA_URL environment variable.

* `jira_username`: The username to authenticate with to Jira.
  Can also be set with JIRA_USERNAME environment variable.

* `jira_password`: The password to authenticate with to Jira.
  Can also be set with JIRA_PASSWORD environment variable.

* `timeout`: A timeout value, in seconds, on requests to the
  Jira API.

* `validate_certs`: Require valid SSL certificates. Set to false
  if you'd like to use self-signed certificates. Defaults to true.

### jira_get_group_fact

* `group_name`: The name of the group to get. Required.

* `include_inactive_users`: Whether to include inactive users of the group.
  Defaults to false.

* `max_results`: The max number of group members to include in the results.
  Defaults to 50.

### jira_get_project_fact

* `project_id`: The ID of the project to query.
  Mutually exclusive of `key`.

* `key`: The Jira key of the project to query.
  Mutually exclusive of `project_id`.

* `expand`: A list of fields to have expanded details of.
  Defaults to ['description', 'lead', 'url', 'projectKeys'].

### jira_get_user_fact

* `username`: The username to query.
  Mutually exclusive of `key`.

* `key`: The Jira key of the user to query.
  Mutually exclusive of `username`.

### jira_list_groups_fact

* `query`: A search string to match with a group name.

* `exclude`: A group to exclude from the results.

* `username`: Return groups where the user is a member.

### jira_list_projects_fact

* `expand`: A list of fields to have expanded details of.
  Defaults to ['description', 'lead', 'url', 'projectKeys'].

* `include_archived`: Whether to include archived projects.
  Defaults to false.

### jira_list_users_fact

* `username`: A search string to use for hte username.
  Defaults to "." which will return all users.

* `include_active`: Whether to include active users in the result.
  Defaults to true.

* `include_inactive`: Whether to include inactive users in the result.
  Defaults to false.

License
-------

Apache 2.0

Author Information
------------------

Joe Topjian <joe@topjian.net>
