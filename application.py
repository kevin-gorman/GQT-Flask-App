from __future__ import print_function
import os
import sys
import boto3
import subprocess
import pandas as pd
from flask import Flask, render_template, request, url_for, Response, redirect
from werkzeug.utils import secure_filename
import json
from flask import send_from_directory
import csv
import copy

application = Flask(__name__)
BASE = '/Users/kevin/patient-visit-app'
UPLOAD_FOLDER = BASE + '/static/data/'
application.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

first = True

class Dataset:
  def __init__(self, name):
    self.name = name


@application.route("/")   
@application.route("/about")
def about():

    findFiles()
    return render_template("about.html", args=args)

# Searchs the 'data' directory to see what files are there, then add them to a list to be used for creating the dropdown menus
def findFiles():

    entries = os.listdir(UPLOAD_FOLDER)
    global files, fileNames, args
    fileNames = []
    files = []
    for en in entries:
        if (os.path.isdir(os.path.join(UPLOAD_FOLDER, en))):
            files.append(Dataset(en))
            fileNames.append(en)

    args = {}
    args["files"] = fileNames
    

findFiles()

# Upload data page
@application.route("/upload", methods=['GET', 'POST'])
def dataAdd():
    
    # Display upload page
    if request.method == 'GET':
        findFiles()
        args["error"] = "none"
        return render_template("data-add.html", args=args)
    
    # File uploaded
    if request.method == 'POST' and 'file' in request.files:
        files = request.files.getlist("file")
        demName = None
        for f in files:
            
            savedFile = f.read()
            header = savedFile[:64]

            # Event file
            if (header[:52] == b'GUID|EventCategory|StartTime|EndTime|EventAttributes'):
                events = copy.deepcopy(savedFile)
                demName = f.filename[:-4]
                args["error"] = "none"

            # Demographics file
            elif (header == b'GUID,Gender,Race,Ethnicity,Status,Religion,Age,State,FIPS,County'):
                dems = copy.deepcopy(savedFile)
                args["error"] = "none"
            
            # Neither
            else:
                args["error"] = "error"
                return render_template("data-add.html", args=args)

        #  Upload if both are present
        path = os.path.join(application.config['UPLOAD_FOLDER'], secure_filename(demName))
        if (not os.path.isdir(path)):
            os.mkdir(path)
        eventsFile = open(os.path.join(path, secure_filename("events.txt")), 'wb')
        eventsFile.write(events)
        eventsFile.close()
        demFile = open(os.path.join(path, secure_filename("demographics.txt")), 'wb')
        demFile.write(dems)
        demFile.close()
        args["newfile"] = path
    
        return render_template("data-uploaded.html", args=args)
    return render_template("data-add.html", args=args)



@application.route("/dashboard/<file>", methods=['GET', 'POST'])
def dashboard(file):

    # Run the data-ui eventflow app
    bashCommand = "cd static/"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    bashCommand = "npm run watch"
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    
    args["displaydash"] = 'data/' + file

    
    
    return render_template("dashboard.html", args=args)



              
if __name__ == "__main__":
    application.run(host="0.0.0.0", port=5000, debug='on')