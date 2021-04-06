from flask import Flask, request, Markup, render_template, flash, Markup
import os
import json

app = Flask(__name__)

@app.route("/")
def about():
    return render_template('about.html')

@app.route("/tallestBuilt")
def tallHome():
    return render_template('tallestBuilt.html', options = get_year_options())

@app.route("/tallestBuiltResponse")
def tallResponse():
    year = request.args['year']
    return render_template('tallestBuiltResponse.html', options = get_year_options(), response = get_tallest(year))
    
def find_years_range():
    firstYear = 2021
    lastYear = 0
    average = find_average_completion()
    with open('skyscrapers.json') as skyscraper_data:
        skyscrapers = json.load(skyscraper_data)
    for skyscraper in skyscrapers:
        year = skyscraper["status"]["completed"]["year"]
        backUp = skyscraper["started"]["year"]
        if year > 0:
            if year < firstYear:
                firstYear = year
            if year > lastYear:
                lastYear = year
        else:
            if backUp > 0:
                if backUp + average < firstYear:
                    firstYear = backUp + average
                if backUp + average > lastyear:
                    lastYear = backUp + average
        return "contains data on buildings built from " + firstYear + " to " + lastYear
    
def find_average_completion():
    completionTime = []
    with open('skyscrapers.json') as skyscraper_data:
        skyscrapers = json.load(skyscraper_data)
    completed = 0
    started = 0
    average = 0
    for skyscraper in skyscrapers:
        completed = skyscraper["status"]["completed"]["year"]
        started = skyscraper["started"]["year"]
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
            years.append(year)
    years.sort()
    options = 0
    for s in years:
        options = options + Markup("<option value=\"" + s + "\">" + s + "</option>")
    return options

def get_tallest(year):
    with open('skyscrapers.json') as skyscraper_data:
        skyscrapers = json.load(skyscraper_data)
    allBuilt = []
    allBuiltHeights = []
    for skyscraper in skyscrapers:
        if skyscraper["status"]["completed"]["year"] == year:
            allBuilt.append(skyscraper["name"])
            allBuiltHeights.append(skyscraper["statistics"]["height"])
    tallest = "none"
    tallestHeight = 0
    count = 0      
    for x in allBuiltHeights:
        if x > tallestHeight:
            tallestHeight = x
            tallest = allBuiltHeights[count]
        count = count + 1
    return tallest + " with a height of " + tallestHeight
