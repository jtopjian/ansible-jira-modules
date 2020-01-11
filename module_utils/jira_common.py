#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import os

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_text
from ansible.module_utils.urls import fetch_url, basic_auth_header

__metaclass__ = type


JIRA_COMMON_ARGS = dict(
    jira_url=dict(type='str'),
    jira_username=dict(type='str'),
    jira_password=dict(type='str', no_log=True),
    timeout=dict(required=False, type='float', default=10),
    validate_certs=dict(required=False, type='bool', default=True),
)


class JiraModuleBase(object):
    def __init__(self, derived_arg_spec, rest_endpoint,
                 facts_module=False, mutually_exclusive=None,
                 required_one_of=None,
                 skip_exec=False, supports_check_mode=False):

        self.rest_endpoint = rest_endpoint

        merged_arg_spec = dict()
        merged_arg_spec.update(JIRA_COMMON_ARGS)

        if derived_arg_spec:
            merged_arg_spec.update(derived_arg_spec)

        self.module = AnsibleModule(
                argument_spec=merged_arg_spec,
                mutually_exclusive=mutually_exclusive,
                required_one_of=required_one_of,
                supports_check_mode=supports_check_mode)

        self.check_mode = self.module.check_mode
        self.facts_module = facts_module

        if not skip_exec:
            self.exec_module(**self.module.params)
            self.module.exit_json(**self.results)

    def exec_module(self, **kwargs):
        self.fail("Error: {0} failed to implement exec_module method.".format(
            self.__class__.__name__))

    def jira_fields(self):
        fields = []
        for field in self.module_args:
            field_args = self.module_args[field]
            if '_jira_field' in field_args:
                jira_field = field_args['_jira_field']
                fields.append([field, jira_field])
        return fields

    def jira_update_fields(self):
        fields = []
        for field in self.module_args:
            field_args = self.module_args[field]
            if '_jira_field' in field_args:
                jira_field = field_args['_jira_field']
                if field_args['_jira_update']:
                    fields.append([field, jira_field])
        return fields

    def get_connection_info(self):
        url = self.module.params.get('jira_url')
        if not url:
            if os.environ.get('JIRA_URL'):
                url = os.environ['JIRA_URL']

        if not url:
            self.fail(msg="jira_url not set")

        username = self.module.params.get('jira_username')
        if not username:
            if os.environ.get('JIRA_USERNAME'):
                username = os.environ['JIRA_USERNAME']

        if not username:
            self.fail(msg="jira_username not set")

        password = self.module.params.get('jira_password')
        if not password:
            if os.environ.get('JIRA_PASSWORD'):
                password = os.environ['JIRA_PASSWORD']

        if not password:
            self.fail(msg="jira_password not set")

        return (url, username, password)

    def fail(self, msg, **kwargs):
        self.module.fail_json(msg=msg, **kwargs)

    def debug(self, msg, pretty_print=False):
        if self.module._verbosity >= 3:
            if pretty_print:
                self.module.log(json.dumps(msg, indent=4, sort_keys=True))
            else:
                self.module.log(msg)

    def log(self, msg, pretty_print=False):
        if pretty_print:
            self.module.log(json.dumps(msg, indent=4, sort_keys=True))
        else:
            self.module.log(msg)

    def param(self, key):
        return self.module.params.get(key)

    def request(self, query=None, data=None, method='GET'):
        if data:
            data = json.dumps(data)

        (url, username, password) = self.get_connection_info()

        url = "%s%s" % (normalize_url(url), self.rest_endpoint)
        timeout = self.module.params['timeout']

        if query is not None:
            url = "%s?%s" % (url, query)

        self.debug(msg="Jira URL request: %s %s" % (method, url))

        auth = basic_auth_header(username, password)
        response, info = fetch_url(
            self.module, url, data=data, method=method, timeout=timeout,
            headers={'Content-Type': 'application/json',
                     'Authorization': auth})

        if info['status'] == 404:
            return False

        if response is not None:
            _body = response.read()
            self.debug(msg="Body result: %s" % (_body))
            if _body:
                body = json.loads(to_text(_body, errors='surrogate_or_strict'))
            else:
                body = {}

        if info['status'] not in (200, 201, 204):
            error_msgs = []

            if 'msg' in info:
                error_msgs.append(info['msg'])

            if 'body' in info:
                _body = json.loads(
                    to_text(info['body'],
                            errors='surrogate_or_strict'))

            if 'errorMessages' in _body:
                for e in _body['errorMessages']:
                    error_msgs.append(e)

            if 'errors' in _body:
                for e in _body['errors']:
                    error_msgs.append("%s: %s" % (e, _body['errors'][e]))

            if len(error_msgs) > 0:
                error_msg = "HTTP Error %s: [%s]" % (
                    info['status'], ', '.join(error_msgs))
            else:
                error_msg = "HTTP Error %s" % (info['status'])

            self.fail(msg=error_msg)

        return body

    def post(self, data, query=None):
        return self.request(
            query=query, data=data, method='POST')

    def put(self, data, query=None):
        return self.request(
            query=query, data=data, method='PUT')

    def get(self, query=None):
        return self.request(query=query)

    def delete(self, query=None):
        return self.request(query=query, method='DELETE')


def normalize_url(url):
    if not url.endswith('/'):
        url = url + '/'
    return url
