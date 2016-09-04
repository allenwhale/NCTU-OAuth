#NCTU-OAuth

台灣國立交通大學推出 [NCTU OAuth]('https://id.nctu.edu.tw/')

你可以透過本套件在tornado開發中使用NCTU OAuth

根據[交通大學 OAuth 服務 - 開發者說明文件](https://id.nctu.edu.tw/docs/)進行對應的開發，以下是一個使用本套件的範例

```Python
import tornado
import tornado.web
import tornado.ioloop
import json
from oauth import NCTUOAuth2Mixin 

REDIRECT_URI = 'http://example.com:8080/auth/'
CLIENT_ID = ''
CLIENT_SECRET = ''

class OAuthHandler(tornado.web.RequestHandler, NCTUOAuth2Mixin):
    @tornado.gen.coroutine
    def get(self):
        code = self.get_argument('code', None)
        if code:
            access = yield self.get_authenticated_user(
                    redirect_uri=REDIRECT_URI,
                    code=code)
            self.set_secure_cookie('access', json.dumps(access))
            self.redirect('/')
        else:
            yield self.authorize_redirect(
                    redirect_uri=REDIRECT_URI,
                    client_id=self.settings[self._OAUTH_SETTINGS_KEY]['client_id'],
                    scope=['profile'],
                    response_type='code')

class IndexHandler(tornado.web.RequestHandler, NCTUOAuth2Mixin):
    @tornado.gen.coroutine
    def get(self):
        if self.get_secure_cookie('access'):
            access = json.loads(self.get_secure_cookie('access').decode())
            try:
                profile = yield self.oauth2_request(
                        self._OAUTH_PROFILE_URL,
                        access=access)
                self.finish(json.dumps(profile))
            except:
                self.redirect('/auth/')
        else:
            self.redirect('/auth/')


if __name__ == '__main__':
    app = tornado.web.Application([
        ('/', IndexHandler),
        ('/auth/', OAuthHandler),
    ], 
    debug=True,
    cookie_secret='secret!',
    NCTU_OAuth2={
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET})
    app.listen(8080)
    tornado.ioloop.IOLoop().instance().start()
```
