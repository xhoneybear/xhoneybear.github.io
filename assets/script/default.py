from browser import document, html
from urllib.error import HTTPError
import urllib.request
import datetime
import calendar
import math
import json

class Error_403(Exception):
    msg = "Could not connect to GitHub API (rate limit exceeded)"
    def __init__(self, message=msg):
        super().__init__(message)

def fetch_commits(username):
    date = datetime.date.today()
    month = str(date)[:7]
    days = calendar.monthrange(date.year, date.month)
    try:
        commits = json.loads(urllib.request.urlopen(f"https://api.github.com/search/commits?q=author:{username}&sort=author-date&order=desc&per_page=100").read())
    except HTTPError:
        document["commit"] <= html.TD(Error_403.msg, colspan=7, Class="error")
        raise Error_403
    count = min(100, commits["total_count"])
    table = [0] * days[1]

    for i in range(count):
        if commits["items"][i]["commit"]["author"]["date"][:7] != month:
            break
        table[int(commits["items"][i]["commit"]["author"]["date"][8:10]) - 1] += 1

    return (table, days)

def make_table(data):
    table = html.TBODY()
    rows = math.ceil((data[1][1] + data[1][0])/7)
    for i in range(rows):
        row = html.TR()
        for j in range(7):
            if 7*i+j < data[1][0] or 7*i+j - data[1][0] + 1 > data[1][1]:
                cell = html.TD(Class="inactive")
            elif data[0][7*i+j - data[1][0]] != 0:
                shade = data[0][7*i+j - data[1][0]]*120/max(data[0])
                cell = html.TD(style=f"background-color: rgb({160 - shade}, {230 - shade}, {170 - shade}); opacity: 0.75;")
                cell <= html.P(data[0][7*i+j - data[1][0]], Class="value", style=f"color: rgb({160 - shade}, {230 - shade}, {170 - shade});")
            else:
                cell = html.TD()
            row <= cell
        table <= row
    return table

document["month"] <= datetime.date.today().strftime("%B")

document["commit"] <= make_table(fetch_commits("xhoneybear"))

def fetch_repos(username):
    try:
        repos = json.loads(urllib.request.urlopen(f"https://api.github.com/users/{username}/repos").read())
    except HTTPError:
        document["project"] <= html.P(Error_403.msg, Class="error")
        raise Error_403
    names = [repo["name"] for repo in repos if repo["fork"] == False and username not in repo["name"]]
    descriptions = [repo["description"] for repo in repos if repo["fork"] == False and username not in repo["name"]]
    return (username, names, descriptions)

def make_tiles(data):
    tiles = html.DIV(Class="full")
    for i in range(len(data[1])):
        tile = html.A(Class="project", href=f"https://github.com/{data[0]}/{data[1][i]}", style=f"background-image: url(https://github.com/{data[0]}/{data[1][i]}/raw/main/preview.png)")
        content = html.DIV(Class="project")
        name = urllib.request.urlopen(f"https://raw.githubusercontent.com/{data[0]}/{data[1][i]}/main/README.md").read().split("\n")[0][2:]
        content <= html.H4(name)
        content <= html.P(data[2][i])
        tile <= content
        tiles <= tile
    return tiles

document["projects"] <= make_tiles(fetch_repos("xhoneybear"))