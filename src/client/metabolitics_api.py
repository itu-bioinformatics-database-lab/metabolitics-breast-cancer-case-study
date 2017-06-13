import requests


class MetaboliticsApiClient:
    url = "http://metabolitics.biodb.sehir.edu.tr/api/%s"

    def login(self, email, password):
        req = requests.post(
            self.url % 'auth', json={'username': email,
                                     'password': password})
        req.raise_for_status()
        self.token_ = req.json()['access_token']

    def analyze(self, name, concentration_changes):
        req = requests.post(
            self.url % 'analysis/fva',
            json={
                'name': name,
                'concentration_changes': concentration_changes
            },
            headers=self.auth_header)
        req.raise_for_status()
        return req.json()['id']

    @property
    def auth_header(self):
        return {'Authorization': 'JWT %s' % self.token_}

    def get_analysis(self, id):
        return requests.get(
            self.url % 'analysis/detail/%d' % id,
            headers=self.auth_header).json()
