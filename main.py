from flask import Flask, render_template, request
from nature import nature_miner
from science import science_miner
app = Flask("Journals")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/nature")   
def nature():
    return render_template("nature.html")

@app.route("/nature_results")   
def nature_results():
    KEYWORD = request.args.get("keyword")
    CYCLE = request.args.get("cycle")
    miner = nature_miner(KEYWORD, CYCLE)
    RESULTS = miner.start()
    return render_template("nature_results.html", keyword=KEYWORD, results=RESULTS)

@app.route("/science")   
def science():
    return render_template("science.html")

@app.route("/science_results")   
def science_results():
    KEYWORD = request.args.get("keyword")
    CYCLE = request.args.get("cycle")
    miner = science_miner(KEYWORD, CYCLE)
    RESULTS = miner.start()
    return render_template("science_results.html", keyword=KEYWORD, results=RESULTS)

app.run("0.0.0.0", port=8000)
