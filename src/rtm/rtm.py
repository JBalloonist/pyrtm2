# Python library for Remember The Milk API

__author__ = 'Sridhar Ratnakumar <http://purl.org/NET/srid/>'
__all__ = (
    'API',
    'API_RESPONSE',
    'createRTM',
    'set_log_level',
)

import json
import logging
import warnings
from hashlib import md5
import requests

# rtm constant
from .consts import SERVICE_URL, AUTH_SERVICE_URL, API, API_RESPONSE

logging.basicConfig()
LOG = logging.getLogger(__name__)
LOG.setLevel(logging.INFO)


class RTMError(Exception): pass

class RTMAPIError(RTMError): pass

class AuthStateMachine:

    class NoData(RTMError): pass

    def __init__(self, states):
        self.states = states
        self.data = {}

    def dataReceived(self, state, datum):
        if state not in self.states:
            raise RTMError(f'Invalid state <{state}>')
        self.data[state] = datum

    def get(self, state):
        if state in self.data:
            return self.data[state]
        else:
            raise AuthStateMachine.NoData(f'No data for <{state}>')


class RTM:

    def __init__(self, apiKey, secret, token=None):
        self.apiKey = apiKey
        self.secret = secret
        self.authInfo = AuthStateMachine(['frob', 'token'])

        # this enables one to do 'rtm.tasks.getList()', for example
        for prefix, methods in API.items():
            setattr(self, prefix, RTMAPICategory(self, prefix, methods))

        if token:
            self.authInfo.dataReceived('token', token)

    def _sign(self, params):
        """Sign the parameters with MD5 hash"""
        pairs = ''.join(f'{k}{v}' for k, v in sortedItems(params))
        return md5((self.secret + pairs).encode('utf-8')).hexdigest()

    def get(self, **params):
        """Get the JSON response for the passed `params`."""
        params['api_key'] = self.apiKey
        params['format'] = 'json'
        # The api_sig MUST be calculated AFTER api_key and format are added
        params['api_sig'] = self._sign(params)
        
        response = requests.get(SERVICE_URL, params=params)
        response.raise_for_status()
        
        data = response.json()
        
        if 'rsp' in data:
            rsp = data['rsp']
            if rsp.get('stat') == 'fail':
                err = rsp.get('err', {})
                raise RTMAPIError(f"API Error {err.get('code')}: {err.get('msg')}")
            return rsp
            
        return data

    def getNewFrob(self):
        rsp = self.get(method='rtm.auth.getFrob')
        try:
            frob = rsp['frob']
            self.authInfo.dataReceived('frob', frob)
            return frob
        except KeyError:
            raise RTMAPIError("Failed to get new frob")

    def getAuthURL(self):
        try:
            frob = self.authInfo.get('frob')
        except AuthStateMachine.NoData:
            frob = self.getNewFrob()

        params = {
            'api_key': self.apiKey,
            'perms': 'delete',
            'frob': frob
        }
        params['api_sig'] = self._sign(params)
        
        req = requests.models.PreparedRequest()
        req.prepare_url(AUTH_SERVICE_URL, params)
        return req.url

    def getToken(self):
        frob = self.authInfo.get('frob')
        rsp = self.get(method='rtm.auth.getToken', frob=frob)
        try:
            token = rsp['auth']['token']
            self.authInfo.dataReceived('token', token)
            return token
        except KeyError:
            raise RTMAPIError("Failed to get token")

class RTMAPICategory:
    """See the `API` structure and `RTM.__init__`"""

    def __init__(self, rtm, prefix, methods):
        self.rtm = rtm
        self.prefix = prefix
        self.methods = methods

    def __getattr__(self, attr):
        if attr in self.methods:
            rargs, oargs = self.methods[attr]
            if self.prefix == 'tasksNotes':
                aname = f'rtm.tasks.notes.{attr}'
            else:
                aname = f'rtm.{self.prefix}.{attr}'
            return lambda **params: self.callMethod(
                aname, rargs, oargs, **params)
        else:
            raise AttributeError(f'No such attribute: {attr}')

    def callMethod(self, aname, rargs, oargs, **params):
        # Sanity checks
        for requiredArg in rargs:
            if requiredArg not in params:
                raise TypeError(f'Required parameter ({requiredArg}) missing')

        for param in params:
            if param not in list(rargs) + list(oargs):
                warnings.warn(f'Invalid parameter ({param})')

        try:
            token = self.rtm.authInfo.get('token')
        except AuthStateMachine.NoData:
            token = None
            
        if params.get('auth_token'):
            # auth.checkToken api needs auth_token parameter
            token = params.pop('auth_token')
            
        if token:
            return self.rtm.get(method=aname, auth_token=token, **params)
        else:
            return self.rtm.get(method=aname, **params)


# Utility functions

def sortedItems(dictionary):
    """ Return a list of (key, value) sorted based on keys
    >>> list(sortedItems({'a': 1, 1: 55, 'key': 7}))
    [(1, 55), ('a', 1), ('key', 7)]
    """
    yield from sorted(dictionary.items(), key=lambda item: str(item[0]))


def createRTM(apiKey, secret, token=None):
    rtm = RTM(apiKey, secret, token)

    if token is None:
        print('No token found')
        print(f'Give me access here: {rtm.getAuthURL()}')
        input('Press enter once you gave access')
        print(f'Note this token for future use: {rtm.getToken()}')

    return rtm

def set_log_level(level):
    '''Sets the log level of the logger used by the module.

    >>> import rtm
    >>> import logging
    >>> rtm.set_log_level(logging.INFO)
    '''
    LOG.setLevel(level)
