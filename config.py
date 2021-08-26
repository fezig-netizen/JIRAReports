import json
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DATABASE_URI = 'sqlite:////{}'.format(os.path.join(basedir,
		'app_database', 'jira_reports.sqlite'))

    AUTH_FILE_PATH = None

    # Provide an absolute path.  Otherwise, ../details.json will be used.
    def getAuthInfo(self, filepath=None):
        if filepath is None:
          if self.AUTH_FILE_PATH is None:
            parent = os.path.abspath(os.path.join(os.getcwd(), '..'))
            filepath = os.path.join(parent, 'details.json')
          else:
            filepath = self.AUTH_FILE_PATH

        with open(filepath, 'r') as input:
            data = json.load(input)
            email = data['email']
            token = data['token']
            return(email, token)