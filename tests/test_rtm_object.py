import os
from configparser import RawConfigParser
from os.path import dirname, join as pathjoin, realpath

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
        self.assert_response('test_tasks_getList', 'lists')

    def test_timezones_getList(self):
        self.assert_response('test_timezones_getList')
