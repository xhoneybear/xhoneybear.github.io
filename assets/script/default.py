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

def fetch_data(username):
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
                row <= html.TD(style="background-color: #888;")
            elif data[0][7*i+j - data[1][0]] != 0:
                shade = data[0][7*i+j - data[1][0]]*120/max(data[0])
                row <= html.TD(style=f"background-color: rgb({160 - shade}, {230 - shade}, {170 - shade}); opacity: 0.75;")
            else:
                row <= html.TD()
        table <= row
    return table

document["month"] <= datetime.date.today().strftime("%B")

table = make_table(fetch_data("xhoneybear"))

document["commit"] <= table