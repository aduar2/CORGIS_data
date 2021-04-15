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
    page = graph + ".html"
    return render_template(page)
    
    
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
    for skyscraper in skyscrapers:
        if skyscraper["status"]["completed"]["year"] == int(year):
            allBuilt.append(skyscraper["name"])
            allBuiltHeights.append(skyscraper["statistics"]["height"])
    tallest = ""
    tallestHeight = 0
    count = 0      
    for x in allBuiltHeights:
        if x > tallestHeight:
            tallestHeight = x
            tallest = allBuiltHeights[count]
        count = count + 1
    return "The tallest building constructed that year was " + tallest + " with a height of " + str(tallestHeight)
    
if __name__=="__main__":
    app.run(debug=False)
