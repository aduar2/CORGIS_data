from flask import Flask, request, Markup, render_template, flash, Markup
import os
import json

app = Flask(__name__)

@app.route("/tallestBuilt")
def home():
    return render_template('tallestBuilt.html', options = get_)

@app.route("/tallestBuilt")
def response():
    year = request.args['year']
    return render_template('tallestBuiltResponse.html', , )
    
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
        }
        else {
            if backUp > 0
            {
                if backUp + average < firstYear:
                    firstYear = backUp
                if backUp + average > lastyear:
                    lastYear = backUp
            }
        }
        return "contains data on buildings built from " + firstYear + " to " + lastYear
    
def find_average_completion():
    completionTime = []
    with open('skyscrapers.json') as skyscraper_data:
        skyscrapers = json.load(skyscraper_data)
    completed = 0
    started = 0
    count = 0
    for skyscraper in skyscrapers:
        completed = skyscraper["status"]["completed"]["year"]
        started = skyscraper["started"]["year"]
        if not started == 0 or not completed == 0:
            time = completed - started
        completionTime[count] = time
        count = count + 1
    for x in completionTime:
        return x
    
def get_year_options():
    years = []
    year = skyscraper["status"]["completed"]["year"]
    with open('skyscrapers.json') as skyscraper_data:
        skyscrapers = json.load(skyscraper_data)
    skyscraper
