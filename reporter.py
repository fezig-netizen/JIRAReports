from jinja2 import Environment, FileSystemLoader, select_autoescape
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

from config import Config
from models import Epic, Issue

cfg = Config()
engine = create_engine(cfg.DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()
env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape(['xml', 'html']))

Statuses = [
    'Default',
    'Pending Clarifications', 'Backlog', 'Refined', 'To Do',
    'InProgress', 'Code Review', 'Testing (QA)', 'Demo To SME (Internal)',
    'Done']

colors = {
    'backlog': 'gray-700',
    'refined': 'gray-600',
    'to do': 'gray-400',
    'inprogress': 'blue-300',
    'testing (qa)': 'blue-700',
    'code review': 'blue-500',
    'demo to sme (internal)': 'green-300',
    'done': 'green-600',
    'pending clarifications': 'red-300',
    'default': 'yellow-400'
}

today = session.query(func.max(Epic.Date)).scalar()
epics = []
epicList = session.query(Epic).filter_by(Date=today).all()

for e in epicList:
    total = 0
    states = {}

    for s in Statuses:
        states[s.lower()] = 0

    for issue in e.Issues:
        if issue.Status.lower() in states:
            states[issue.Status.lower()] += 1
        else:
            states['default'] += 1

        total += 1

    statusSummary = []

    for title in Statuses:
        index = title.lower()

        if states[index] > 0:
            pct = 100 * states[index] / total
            color = colors[index]
            statusSummary.append({ 'percent': pct, 'color': color, 'total': states[index] })

    epics.append({'epic': e, 'statuses': statusSummary})

legend = []

for s in Statuses:
    legend.append({ 'label': s, 'color': colors[s.lower()] })

temp = env.get_template('basic.html')
html = temp.render(epics=epics, legend=legend)
print(html)
