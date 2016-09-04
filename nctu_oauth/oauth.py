import tornado.auth
import tornado.escape
import urllib.parse
import functools

class NCTUOAuth2Mixin(tornado.auth.OAuth2Mixin):
    _OAUTH_AUTHORIZE_URL = 'https://id.nctu.edu.tw/o/authorize/'
    _OAUTH_ACCESS_TOKEN_URL = 'https://id.nctu.edu.tw/o/token/'
    _OAUTH_PROFILE_URL = 'https://id.nctu.edu.tw/api/profile/'
    _OAUTH_SETTINGS_KEY = 'NCTU_OAuth2'
    @tornado.auth._auth_return_future
    def get_authenticated_user(self, redirect_uri, code, callback):
        http = self.get_auth_http_client()
        body = urllib.parse.urlencode({
            'redirect_uri': redirect_uri,
            'code': code,
            'client_id': self.settings[self._OAUTH_SETTINGS_KEY]['client_id'],
            'client_secret': self.settings[self._OAUTH_SETTINGS_KEY]['client_secret'],
            'grant_type': 'authorization_code'})
        http.fetch(self._OAUTH_ACCESS_TOKEN_URL,
                functools.partial(self._on_access_token, callback),
                method='POST',
                headers={'Content-Type': 'application/x-www-form-urlencoded'},
                body=body)

    def _on_access_token(self, future, response):
        if response.error:
            future.set_exception(tornado.auth.AuthError('NCTU OAuth error: %s' % str(response)))
            return
        future.set_result(tornado.escape.json_decode(response.body))
        
    @tornado.auth._auth_return_future
    def oauth2_request(self, url, callback, access=None):
        headers = {'Authorization': '%s %s' % (access['token_type'], access['access_token'])}
        callback = functools.partial(self._on_oauth2_request, callback)
        http = self.get_auth_http_client()
        http.fetch(
                url,
                method='GET',
                headers=headers,
                callback=callback)

    def _on_oauth2_request(self, future, response):
        if response.error:
            future.set_exception(tornado.auth.AuthError('Error response %s fetching %s' % (response.error, response.request.url)))
            return
        future.set_result(tornado.escape.json_decode(response.body))
