from flask import Flask, redirect, request, url_for, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

allShows = []
week = ["", "", "", "", "", "", ""]
stats = {}
info = ""


def getStats(url):
    stats['url'] = url
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find_all('h1', class_="title-name h1_bold_none")
    stats['title'] = results[0].text.strip()
    results = soup.find_all('div', class_='spaceit')
    for res in results:
        if None in res:
            continue
        if "Broadcast:" in res.prettify():
            stats['date'] = date(res.prettify())
        elif "Episodes:" in res.prettify():
            stats['num-eps'] = eps(res)
    return stats

def getSchedule(newShow):
    week[newShow['date']] = week[newShow['date']] + '\n' + newShow['title']

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        url = request.form["link"]
        newShow = getStats(url)
        getSchedule(newShow)
        allShows.append(newShow)
        newShow = []
        return render_template("index.html", data=allShows, schedule=week)
    else:
        print('ur fat')
        return render_template("index.html", data=allShows, schedule=week)

def date(str):
    if "Monday" in str:
        return 0
    if "Tuesday" in str:
        return 1
    if "Wednesday" in str:
        return 2
    if "Thursday" in str:
        return 3
    if "Friday" in str:
        return 4
    if "Saturday" in str:
        return 5
    if "Sunday" in str:
        return 6

def eps(str):
    s = str.text.strip()
    if "Episodes:" in s:
        s = s[10:]
    return s

if __name__ == "__main__":
    app.run(debug=True)