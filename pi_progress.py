import json
import os

from Lib.jira import jira

# dataPath = os.path.join(os.getcwd(), 'data', 'sqlite.db')
# print(dataPath)

# Provide an absolute path.  Otherwise, ../details.json will be used.
def getAuthInfo(filepath=None):
    if filepath is None:
        parent = os.path.abspath(os.path.join(os.getcwd(), '..'))
        filepath = os.path.join(parent, 'details.json')

    with open(filepath, 'r') as input:
        data = json.load(input)
        email = data['email']
        token = data['token']
        return(email, token)


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

def getEpicsByPI(piName):
    query = f'issuetype = Epic and fixVersion = "{ piName }"'
    print(query)
    json = conn.getJqlResults(query)
    print(json)

(email, token) = getAuthInfo()
conn = jira(email, token)

# TODO: Have this method return a list of epics with data suitable for use in reports and
# further queries.

getEpicsByPI('FPAC CDRM - PI 5')

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

