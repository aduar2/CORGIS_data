from flask import Flask, request, Markup, render_template, flash, Markup
import os
import json

app = Flask(__name__)

@app.route("/")
def about():
    return render_template('about.html', average = find_average_completion())

@app.route("/tallestBuilt")
def tallHome():
    return render_template('tallestBuilt.html', options = get_year_options())

@app.route("/tallestBuiltResponse")
def tallResponse():
    year = request.args['year']
    return render_template('tallestBuiltResponse.html', options = get_year_options(), tallest = get_tallest(year))

@app.route("/graphHome")
def graphHome():
    return render_template('graphHome.html')

@app.route("/getGraph")
def graphResponse():
    graph = request.args['graph']
    if graph == "pieChart":
        percents = find_percents()
        con = percents[0]
        s = percents[1]
        com = percents[2]
        m = percents[3]
        sc = percents[4]
        return render_template('pieChart.html', concrete = con, steel = s, composite = com, masonry = m, steelConcrete = sc)
    if graph == "lineGraph":
        return render_template('lineGraph.html', points = get_line_data())


def find_average_completion():
    completionTime = []
    with open('skyscrapers.json') as skyscraper_data:
        skyscrapers = json.load(skyscraper_data)
    completed = 0
    started = 0
    average = 0
    for skyscraper in skyscrapers:
        completed = skyscraper["status"]["completed"]["year"]
        started = skyscraper["status"]["started"]["year"]
        if not started == 0 or not completed == 0:
            time = completed - started
            completionTime.append(time)
    for x in completionTime:
        average = average + x
        x = x + 1
    average = average / len(completionTime)
    return average
    
def get_year_options():
    years = []
    with open('skyscrapers.json') as skyscraper_data:
        skyscrapers = json.load(skyscraper_data)
    for skyscraper in skyscrapers:
        year = skyscraper["status"]["completed"]["year"]
        if year > 0:
            if years.count(str(year)) == 0:
                years.append(str(year))
    years.sort()
    options = ""
    for s in years:
        options = options + Markup("<option value=\"" + s + "\">" + s + "</option>")
    return options

def get_tallest(year):
    with open('skyscrapers.json') as skyscraper_data:
        skyscrapers = json.load(skyscraper_data)
    allBuilt = []
    allBuiltHeights = []
    cities = []
    for skyscraper in skyscrapers:
        if skyscraper["status"]["completed"]["year"] == int(year):
            allBuilt.append(skyscraper["name"])
            allBuiltHeights.append(skyscraper["statistics"]["height"])
            cities.append(skyscraper["location"]["city"])
    tallest = ""
    tallestHeight = 0
    city = ""
    count = 0
    for x in allBuiltHeights:
        if x > tallestHeight:
            tallestHeight = x
            tallest = allBuilt[count]
            city = cities[count]
        count = count + 1
    return "The tallest building constructed in " + year + " was " + tallest + " in " + city + " with a height of " + str(tallestHeight) + "m"

def find_percents():
    with open('skyscrapers.json') as skyscraper_data:
        skyscrapers = json.load(skyscraper_data) # do i need to do that every time or am i just being silly? lol
    con = 0
    s = 0
    m = 0
    com = 0
    sc = 0
    for x in skyscrapers:
        for skyscraper in skyscrapers:
            mat = skyscraper["material"]
            if mat == "concrete":
                con = con + 1
            if mat == "steel":
                s = s + 1
            if mat == "masonry":
                m = m + 1
            if mat == "steel/concrete":
                sc = sc + 1
            if mat == "composite":
                com = com + 1
    total = con + m + s + com + sc
    percentCon = con/total
    percentM = m/total
    percentS = s/total
    percentSC = sc/total
    percentCom = com/total
    
    percents = [percentCon * 100, percentS * 100, percentCom * 100, percentM * 100, percentSC * 100]
    return percents

def get_line_data():
    # find number of buildings each year
    with open('skyscrapers.json') as skyscraper_data:
        skyscrapers = json.load(skyscraper_data)
    years = []
    for skyscraper in skyscrapers:
        year = skyscraper["status"]["completed"]["year"]
        if year > 0:
            years.append(year)
    years.sort()
    dataPoints = []
    for year in years:
        if years.count(year) > 0:
            count = years.count(year)
            if dataPoints.count(year) == 0:                
                dataPoints.append("{x: new Date(" + str(year) + ", 0), y: " + str(count) + "}")
    return dataPoints

if __name__=="__main__":
    app.run(debug=False)
