from flask import Flask, redirect, url_for, render_template, request
import sqlalchemy  
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)


"""
Setting up the Database table 
"""
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class assignments(db.Model):
    _id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    deadline = db.Column(db.Date)
    module_code = db.Column(db.String(100))
    comments = db.Column(db.String(100))
    status = db.Column(db.Boolean)

    def __init__(self, name, deadline, module_code, comments, status):
        self.name = name
        self.deadline = deadline
        self.module_code = module_code
        self.comments = comments
        self.status = status



"""
Created all routes and methods for the different windows:

"""

@app.route("/")
def main():
    return render_template("base.html")

@app.route("/viewAll")
def viewAll():
    return render_template("viewAll.html", info = assignments.query.all())

@app.route("/createAssignment", methods = ["POST", "GET"])
def create():
    if request.method == "POST":
       locName = request.form["name"]
       locDead = request.form["deadline"]
       locCode = request.form["moduleC"]
       locComment = request.form["comments"]
       locStatus = False
       assignment = assignments(locName, datetime.strptime(locDead, "%Y-%m-%d"), locCode, locComment, locStatus)
       
       db.session.add(assignment)
       db.session.commit() 

    return render_template("createAssignment.html")

@app.route("/viewCompletedAssignments")
def viewComplete():
    return render_template("viewCompleted.html")

@app.route("/viewIncompleteAssignments")
def viewIncomplete():
    return render_template("viewIncomplete.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
