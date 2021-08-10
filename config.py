import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    DATABASE_URI = 'sqlite:////{}'.format(os.path.join(basedir,
		'app_database', 'jira_reports.sqlite'))