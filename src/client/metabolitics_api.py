import requests


class MetaboliticsApiClient:
    url = "http://metabolitics.biodb.sehir.edu.tr/api/%s"

    def login(self, email, password):
        req = requests.post(
            self.url % 'auth', data={'name': name,
                                     'password': password}).json()
        req.raise_for_status()
        self.token_ = req.json()

    def analyze(self, name, concentration_changes):
        req = requests.post(
            self.url % 'analysis/fva',
            data={
                'name': name,
                'concentration_changes': concentration_changes
            }).json()
        req.raise_for_status()

    def get_analysis(self, id):
        return requests.get(self.url % 'analysis/detail/%d' % id).json()
