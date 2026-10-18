import os
import warnings
from configparser import RawConfigParser
from os.path import dirname, join as pathjoin, realpath
from unittest import mock

import pytest

import rtm.rtm as RTM

KEY_TXT = pathjoin(dirname(realpath(__file__)), 'apikey.txt')
KEY_TXT_FORMAT = """
The format are(ConfigParser readable):
[rtm]
apikey: xxx
secret: yyy
token: zzz
"""


class TestRTMOffline:
    """Tests that exercise the client without hitting the live API."""

    def setup_method(self):
        self.rtm = RTM.RTM('apikey', 'secret', token='token')

    def test_sign_is_deterministic(self):
        params = {'method': 'rtm.test.echo', 'api_key': 'apikey'}
        assert self.rtm._sign(params) == self.rtm._sign(dict(params))

    def test_get_auth_url_contains_frob(self):
        self.rtm.authInfo.dataReceived('frob', 'my-frob')
        url = self.rtm.getAuthURL()
        assert url.startswith(RTM.AUTH_SERVICE_URL)
        assert 'frob=my-frob' in url

    def test_unknown_method_raises_attribute_error(self):
        with pytest.raises(AttributeError):
            self.rtm.tasks.notAMethod()

    def test_missing_required_param_raises_type_error(self):
        with pytest.raises(TypeError):
            self.rtm.tasks.add()

    def test_api_arg_specs_are_tuples(self):
        for prefix, methods in RTM.API.items():
            for name, (rargs, oargs) in methods.items():
                assert isinstance(rargs, tuple), f'{prefix}.{name}'
                assert isinstance(oargs, tuple), f'{prefix}.{name}'

    def test_api_and_response_cover_same_methods(self):
        assert RTM.API.keys() == RTM.API_RESPONSE.keys()
        for prefix, methods in RTM.API.items():
            assert methods.keys() == RTM.API_RESPONSE[prefix].keys(), prefix

    @pytest.mark.parametrize('prefix, method, params', [
        ('push', 'getSubscriptions', {}),
        ('push', 'getTopics', {}),
        ('push', 'subscribe', {'timeline': '1', 'url': 'https://x.example',
                               'topics': 'task_created',
                               'push_format': 'json'}),
        ('push', 'unsubscribe', {'timeline': '1', 'subscription_id': '2'}),
        ('scripts', 'add', {'timeline': '1', 'name': 'n', 'code': 'c'}),
        ('scripts', 'delete', {'timeline': '1', 'script_id': '2'}),
        ('scripts', 'getList', {'name': 'n'}),
        ('scripts', 'run', {'timeline': '1', 'script_id': '2'}),
        ('scripts', 'setCode', {'timeline': '1', 'script_id': '2',
                                'code': 'c'}),
        ('scripts', 'setName', {'timeline': '1', 'script_id': '2',
                                'name': 'n'}),
        ('tags', 'getList', {}),
        ('tasks', 'setParentTask', {'timeline': '1', 'list_id': '2',
                                    'taskseries_id': '3', 'task_id': '4',
                                    'parent_task_id': '5'}),
        ('tasks', 'setStartDate', {'timeline': '1', 'list_id': '2',
                                   'taskseries_id': '3', 'task_id': '4',
                                   'start': 'tomorrow', 'parse': '1'}),
    ])
    def test_new_methods_call_rtm(self, monkeypatch, prefix, method, params):
        calls = self.mock_post(monkeypatch)
        with warnings.catch_warnings():
            warnings.simplefilter('error')
            getattr(getattr(self.rtm, prefix), method)(**params)
        assert calls[0]['data']['method'] == f'rtm.{prefix}.{method}'

    def test_set_default_list_accepts_timeline(self, monkeypatch):
        calls = self.mock_post(monkeypatch)
        with warnings.catch_warnings():
            warnings.simplefilter('error')
            self.rtm.lists.setDefaultList(timeline='1', list_id='2')
        assert calls[0]['data']['method'] == 'rtm.lists.setDefaultList'

    def test_requests_are_posted_with_v2(self, monkeypatch):
        calls = self.mock_post(monkeypatch)
        self.rtm.lists.getList()
        (call,) = calls
        assert call['url'] == RTM.SERVICE_URL
        assert call['data']['v'] == '2'
        assert call['data']['auth_token'] == 'token'

    def test_credentials_not_in_url(self, monkeypatch):
        calls = self.mock_post(monkeypatch)
        self.rtm.lists.getList()
        assert 'apikey' not in calls[0]['url']
        assert 'token' not in calls[0]['url']

    def test_as_list(self):
        assert RTM.as_list({'id': '1'}) == [{'id': '1'}]
        assert RTM.as_list([{'id': '1'}]) == [{'id': '1'}]
        assert RTM.as_list([]) == []
        assert RTM.as_list(None) == []

    @staticmethod
    def mock_post(monkeypatch):
        calls = []

        def fake_post(url, data=None, timeout=None):
            calls.append({'url': url, 'data': data})
            response = mock.Mock()
            response.json.return_value = {'rsp': {'stat': 'ok'}}
            return response

        monkeypatch.setattr(RTM.requests, 'post', fake_post)
        return calls


class TestRTM:
    """Tests that call the live Remember The Milk API.

    Requires an `apikey.txt` file next to this module, readable by
    `configparser.RawConfigParser`:

        [rtm]
        apikey: xxx
        secret: yyy
        token: zzz
    """

    message = {
        'skip': f'\n\nSet your API key "{KEY_TXT}" to run TestRTM for '
                f'authentication\n{KEY_TXT_FORMAT}',
        'cannot_read': f'\n\nCannot read "{KEY_TXT}"\n{KEY_TXT_FORMAT}',
        'no_item': 'rtm.%s.%s: Cannot get response item, '
                   'maybe there is no item\n',
    }

    def setup_method(self):
        if not os.access(KEY_TXT, os.R_OK):
            pytest.skip(self.message['skip'])
        self.read_key_txt()
        self.rtm = RTM.createRTM(self.apikey, self.secret, self.token)

    def read_key_txt(self):
        try:
            c = RawConfigParser()
            c.read(KEY_TXT)
            self.apikey = c.get('rtm', 'apikey')
            self.secret = c.get('rtm', 'secret')
            self.token = c.get('rtm', 'token')
        except Exception as err:
            pytest.skip(self.message['cannot_read'] + str(err))

    def assert_response(self, func_name, elem=None, **params):
        """Assert the stat/attr(only top) of response from api"""
        api, method = func_name.replace('test_', '').split('_')
        elem = elem or api
        rsp = getattr(getattr(self.rtm, api), method)(**params)
        assert rsp['stat'] == 'ok'

        rsp_attr = rsp.get(api)
        if not isinstance(rsp_attr, dict):
            pytest.skip(self.message['no_item'] % (api, method))
        attr = next(iter(RTM.API_RESPONSE[api][method][elem]))
        assert attr in rsp_attr

    def test_auth_checkToken(self):
        self.assert_response('test_auth_checkToken', auth_token=self.token)

    def test_contacts_getList(self):
        self.assert_response('test_contacts_getList')

    def test_groups_getList(self):
        self.assert_response('test_groups_getList')

    def test_lists_getList(self):
        self.assert_response('test_lists_getList')

    def test_locations_getList(self):
        self.assert_response('test_locations_getList')

    def test_settings_getList(self):
        self.assert_response('test_settings_getList')

    def test_tasks_getList(self):
        self.assert_response('test_tasks_getList')

    def test_timezones_getList(self):
        self.assert_response('test_timezones_getList')
