from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

station = pd.read_csv("data_small/stations.txt", skiprows=17)
station = station[["STAID", "STANAME                                 "]]
@app.route("/")
def home():
    return render_template("home.html", data=station.to_html())

@app.route("/api/v1/<station>/<date>")
def about(station, date):
    df = pd.read_csv("data_small/TG_STAID" + str(station).zfill(6) + ".txt", skiprows=20, parse_dates=["    DATE"])
    temperature = df.loc[df["    DATE"] == date]["   TG"].squeeze() /10
    return {"station": station,
            "date": date,
            "temperature": temperature}

@app.route("/api/v1/<station>")
def alldates(station):
    df = pd.read_csv("data_small/TG_STAID" + str(station).zfill(6) + ".txt", skiprows=20, parse_dates=["    DATE"])
    return df.to_dict(orient="records")

@app.route("/api/v1/yearly/<station>/<yr>")
def yearly(station, yr):
    df = pd.read_csv("data_small/TG_STAID" + str(station).zfill(6) + ".txt", skiprows=20)
    df["    DATE"] = df["    DATE"].astype(str)
    result = df[df["    DATE"].str.startswith(str(yr))].to_dict(orient="records")
    return result

app.run(debug=True)