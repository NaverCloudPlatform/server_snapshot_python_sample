class BaseAuthInfo:

    ## NCP Access key
    access_key = ''
    ## NCP Access secret
    access_secret = ''

    req_path = ''

    url = 'https://ncloud.apigw.ntruss.com'

    def get_access_key(self):
        return self.access_key

    def get_access_secret(self):
        return self.access_secret

    def get_req_path(self):
        return self.req_path

    def get_url(self):
        return self.url

    def set_access_key(self, access_key):
        self.access_key = access_key

    def set_access_secret(self, access_secret):
        self.access_secret = access_secret

    def set_req_path(self, req_path):
        self.req_path = req_path

    def set_http_mehtod(self, http_method):
        self.http_method = http_method
