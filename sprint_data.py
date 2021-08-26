import datetime
import json
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import Config
from Lib.jira import jira
from models import Epic, Issue, Sprint

# --------- CONSTANTS ----------

# As of August 19, 2021, the main FCDRM board is numbered as "5".
FCDRM_BOARD_NUMBER = 5

# --------- Setup --------------

cfg = Config()
engine = create_engine(cfg.DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()
today = datetime.date.today()

epicCache = {}

def loadSprint(sprintId):
    json = conn.getSprintById(sprintId)
    s = session.query(Sprint).filter_by(JiraId=sprintId).first()

    if s is None:
        s = Sprint()
        s.JiraId = json['id']
        session.add(s)

    s.Name = json['name']
    session.commit()
    return s

# Try to fetch epics first from memory, then the database, then Jira.

def getEpic(jiraId):
    if jiraId not in epicCache.keys():
        epicCache[jiraId] = loadEpic(jiraId)
    
    return epicCache[jiraId]

def loadEpic(jiraId):
    e = session.query(Epic).filter_by(Key=jiraId, Date=today).first()

    if e is None:
        json = conn.getIssueById(jiraId)
        e = Epic()
        e.Key = jiraId
        e.Date = today
        session.add(e)
        e.Summary = json["fields"]["summary"]
        e.Status = json["fields"]["status"]["name"]
        session.commit()

    return e

def loadSprintIssues(sprint, data={}):
    json = conn.getIssuesBySprint(sprint.JiraId, data)

    for i in json['issues']:
        # If we already pulled data into the database today, start with that
        issue = session.query(Issue).filter_by(Key=i["key"], Date=today).first()

        # Not in the database?  Add to the database.
        if issue is None:
            issue = Issue()
            epicId = i['fields']['customfield_10014']

            if epicId is not None:
                epic = getEpic(epicId)
                issue.EpicId = epic.Id

            issue.Key = i["key"]
            issue.Date = today
            session.add(issue)

        # Update things that might have changed since the last time we refreshed the database.
        # We're only doing this because we have recent data from Jira.
        issue.IssueType = i["fields"]["issuetype"]["name"]
        issue.Status = i["fields"]["status"]["name"]
        issue.Summary = i["fields"]["summary"]

        if issue.IssueType == 'Bug':
            issue.Estimate = None
        else:
            issue.Estimate = i["fields"]["customfield_10026"]

        sprint.Issues.append(issue)
    
    session.commit()

# ------------------ Main Program ------------------

(email, token) = cfg.getAuthInfo()
conn = jira(email, token)

sprintIds = [43, 44]

for id in sprintIds:
    sprint = loadSprint(id)
    loadSprintIssues(sprint)
#loadSprints(conn.getSprintsByBoard(FCDRM_BOARD_NUMBER, { 'maxResults': '2' }))