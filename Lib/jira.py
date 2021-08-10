import base64
import json
import requests

class jira:
    _base = 'https://brillient.atlassian.net/rest/'
    _rest_base = _base + 'api/3/'
    _agile_base = _base + 'agile/1.0/'

    def __init__(self, username, token=None):
        if token is None:
            self.token = username
        else:
            self.token = self._generateAuthToken(username, token)

    def _generateAuthToken(self, username, token):
        input = bytearray((':'.join([username, token])).encode())
        authToken = base64.b64encode(input).decode('utf-8')
        return authToken


    def restRequest(self, url, data=None):
        return self.request(self._rest_base + url, data)

    def agileRequest(self, url, data=None):
        return self.request(self._agile_base + url, data)

    # For now, the data value will be a dictionary for building the query string
    def request(self, url, data=None):
        headers = {'Authorization': 'Basic ' + self.token,
            'Content-Type': 'application/json'}

        # Build the query string, if needed
        if data is not None:
            qryString = []

            # TODO: HTML escape values
            for key, val in data.items():
                qryString.append(f'{key}={val}')

            url = url + '?' + '&'.join(qryString)

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return json.loads(response.content.decode('utf-8'))
        else:
            print('ERROR: ' + response.content.decode('utf-8'))

    def getIssueById(self, id):
        return self.restRequest(f'issue/{id}')
    
    def websafeQueryString(self, query):
        safeQuery = query.replace(' ', '+')
        return safeQuery

    def getJqlResults(self, query, data={}):
        data['jql'] = self.websafeQueryString(query)
        print(data['jql'])
        return self.restRequest('search', data)
