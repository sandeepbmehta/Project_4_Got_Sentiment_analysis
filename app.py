# import necessary libraries
from bs4 import BeautifulSoup
import requests
import pprint
import json
import pymongo
import pandas as pd
from sqlalchemy import func
import os
from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

# from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# create route that renders index.html template
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/obtainData")
def obtain_data():
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    # Define the 'classDB' database in Mongo
    db = client.projDB
    char_collection = db.char_img.find()
    # Insert a document into the 'hist' collection
    char_name_img_list = []
    for char in char_collection:
        char_dict = {}
        char_dict["name"] = char["name"]
        char_dict["img_url"] = char["img_url"]
        char_name_img_list.append(char_dict)
    
    file1 = "data/combined.csv"
    df1 = pd.read_csv(file1)
    df = df1[["char", "date", "polarity"]]
    # df["char"] = "Daenerys Targaryen"
    df2 = df.groupby(["char", "date"])["polarity"].mean()
    file_df = df2.reset_index()

    for character in char_name_img_list:
        # print (character["name"])
        char_data_df = file_df.loc[file_df["char"] == character["name"]]
        # print(char_data_df.size)
        if char_data_df.size > 0:
            character["date"] = [date for date in char_data_df["date"]]
            character["polarity"] = [polarity for polarity in char_data_df["polarity"]]

    return jsonify(char_name_img_list)

if __name__ == "__main__":
    app.run()
