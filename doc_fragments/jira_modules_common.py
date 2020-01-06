# -*- coding: utf-8 -*-

class ModuleDocFragment(object):
    # Common pulp documentation fragment
    DOCUMENTATION = r'''
options:
  jira_url:
    description:
      - The URL of the Jira service.
    required: true
    env:
      - JIRA_URL

  jira_username:
    description:
      - The username to connect to Jira with.
    required: true
    env:
      - JIRA_USERNAME

  jira_password:
    description:
      - The password to authenticate with
    required: true
    env:
      - JIRA_PASSWORD

  timeout:
    required: false
    description:
      - Set timeout, in seconds, on requests to Jira API.
    default: 10

  validate_certs:
    required: false
    description:
      - Require valid SSL certificates
        (set to `false` if you'd like to use self-signed certificates)
    default: true
    type: bool
'''
