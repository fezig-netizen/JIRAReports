import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import Config
from Lib.jira import jira
from models import Epic, Issue

# --------- CONSTANTS ----------

# As of August 19, 2021, the main FCDRM board is numbered as "5".
FCDRM_BOARD_NUMBER = 5

# --------- Setup --------------

cfg = Config()
engine = create_engine(cfg.DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()
today = datetime.date.today()

def getIssueById(id):
    json = conn.getIssueById(id)
    print(json['key'])
    print(json['fields']['summary'])
    print(json['fields']['issuetype']['name'])
    print(json['fields']['status']['name'])
    print(json['fields']['timeoriginalestimate'])

    # sprints
    sprints = json['fields']['customfield_10020']

    if sprints is not None:
        for sp in sprints:
            print(sp['name'])
            print(sp['id'])
    
    # epic
    print('Epic: ' + json['fields']['customfield_10014'])

    print('\nSubtasks')
    subtask = json['fields']['subtasks']
    for s in subtask:
        print()
        print(s['key'])
        print(s['fields']['summary'])
        print(s['fields']['issuetype']['name'])
        print(s['fields']['status']['name'])

# Get the issues associated with an epic and store them in the database.
# Issues are associated with a daily instance of an epic.  The same Jira issue will have
# multiple rows -- one for each day it has been associated with an epic.

def loadIssuesByEpic(epic):
    query = f'"Epic Link" = { epic.Key } order by rank'
    json = conn.getJqlResults(query)

    for i in json['issues']:
        issue = session.query(Issue).filter_by(Key=i["key"], EpicId=epic.Id).first()

        if issue is None:
            issue = Issue()
            issue.EpicId = epic.Id
            issue.Key = i["key"]
            issue.Date = today
            session.add(issue)

        issue.IssueType = i["fields"]["issuetype"]["name"]
        issue.Status = i["fields"]["status"]["name"]
        issue.Summary = i["fields"]["summary"]

        if issue.IssueType == 'Bug':
            issue.Estimate = None
        else:
            issue.Estimate = i["fields"]["customfield_10026"]
    
    session.commit()

# Get the epics associated with a fix version and store them in the database.
# Epics have a date stamp.  If this is run twice in the same day, epics not seen before are added,
# while epics already seen today are updated.  If this is run on subsequent days, there will be a
# unique record for each epic on each day.  This allows us to have historical data, somewhat.

def loadEpicsByPI(piName):
    query = f'issuetype = Epic and fixVersion = "{ piName }"'
    json = conn.getJqlResults(query)

    for epic in json['issues']:
        loadEpic(epic)

    session.commit()

def loadEpicById(id):
    query = f'issuetype = Epic and key="{ id }"'
    json = conn.getJqlResults(query)
    loadEpic(json['issues'][0])
    session.commit()

def loadEpic(epic):
    e = session.query(Epic).filter_by(Key=epic["key"], Date=today).first()

    if e is None:
        e = Epic()
        e.Key = epic["key"]
        e.Date = today
        session.add(e)

    e.Summary = epic["fields"]["summary"]
    e.Status = epic["fields"]["status"]["name"]
    #e.FixVersion = epic["fields"][]


# ------------------ Main Program ------------------

(email, token) = cfg.getAuthInfo()
conn = jira(email, token)

loadEpicsByPI('FPAC CDRM - PI 5')
epics = session.query(Epic).filter_by(Date=today).all()

for e in epics:
    loadIssuesByEpic(e)



# ----------- EXAMPLES -------------------------------------

#getIssueById('FCDRM-1514')

#json = conn.agileRequest('board/5/backlog', { 'startAt': '350', 'maxResults': '50' })
#print(len(json['issues']))

# ------------------ OLDER EXAMPLES ------------------------

# epics = ['FCDRM-2046', 'FCDRM-2047', 'FCDRM-1266', 'FCDRM-1246', 'FCDRM-2114', 'FCDRM-2199', 'FCDRM-2137',
#         'FCDRM-1198', 'FCDRM-1349', 'FCDRM-1217', 'FCDRM-2271', 'FCDRM-2101', 'FCDRM-2119', 'FCDRM-2132', 
#         'FCDRM-2270', 'FCDRM-2145', 'FCDRM-2148', 'FCDRM-1175', 'FCDRM-2194', 'FCDRM-2273', 'FCDRM-2201',
#         'FCDRM-1397', 'FCDRM-1396', 'FCDRM-1392', 'FCDRM-1388', 'FCDRM-2283', 'FCDRM-2240', 'FCDRM-2109', 
#         'FCDRM-1269', 'FCDRM-2581']
# epics = ','.join(epics)
# query = f'issuetype=Epic AND key in({ epics })'
# print(query)
# json = conn.getJqlResults(query)
# print(json)

