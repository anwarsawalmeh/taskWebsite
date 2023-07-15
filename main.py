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
    id = db.Column(db.Integer, primary_key = True)
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
    return render_template("home.html")

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
       return render_template("viewIncomplete.html")

    return render_template("createAssignment.html")

@app.route("/viewCompletedAssignments")
def viewComplete():
    return render_template("viewCompleted.html", info = assignments.query.filter_by(status = True).all())

@app.route("/viewIncompleteAssignments", methods=["POST", "GET"])
def viewIncomplete():
    if request.method == "POST":
        ass = request.form["assignment_id"]
        button_name =  request.form["mark_complete"]

        assignment = assignments.query.filter_by(id=ass).first()
        assignment.status = True

        db.session.add(assignment)
        db.session.commit()
    return render_template("viewIncomplete.html", info = assignments.query.filter_by(status = False).all())

@app.route("/calanderView")
def viewCalander():
    events = []
    data = assignments.query.all()
    for d in data:
        color = ''
        eventTitle = d.name
        eventDate = d.deadline

        if d.status is True:
            color = '#008000'
        else:
            color = '#FF0000'
        
        events.append(
            {
                'name': eventTitle,
                'date':eventDate,
                'color':color,
            }
        )
    return render_template("calander.html", events = events)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
