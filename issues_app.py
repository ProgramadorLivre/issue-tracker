# -*- encoding: utf-8 -*-

from flask import Flask, render_template, jsonify, request, redirect
from tinydb import TinyDB, Query
from slugify import slugify

db = TinyDB('issues.db.json')

Issues = db.table("issues")
Projects = db.table("projects")
Milestones = db.table("milestones")
Filter = Query()

app = Flask(__name__)
app.debug = True


@app.route("/")
def index():
    projetos = Projects.all()
    return render_template("index.html", projetos=projetos)


@app.route("/add_project", methods=("POST",))
def addprojetc():
    data = request.form.get 

    newp = Projects.insert({"name": data("name"), "slug":slugify(data("name"))})
    newproject = Projects.get(eid=newp)
    newproject['eid'] = newproject.eid

    return jsonify({"status":"ok","message":"Project added", "object": newproject })


@app.route("/rm_project", methods=("POST",))
def del_project():
    data = request.form.get 
    
    pid = int(data("pid"))

    Projects.remove(eids=[pid])

    return jsonify({"status":"ok","message":"Project removed" })


@app.route("/add_milestone", methods=("POST",))
def addmilestone():
    print(request.form )
    return jsonify({"status":"ok","message":"Milestone added"})


@app.route("/add_issue", methods=("POST",))
def addissue():
    print(request.form )
    return jsonify({"status":"ok","message":"Issue added"})


@app.route("/<project_slug>/")
def listissues(project_slug):
    projeto = Projects.get(Filter.slug==project_slug)
    if not projeto:
        return redirect("/")
    projetos = Projects.all()
    milestones = Milestones.get(Filter.project_id==projeto.eid)
    issueslist = Issues.get(Filter.project_id==projeto.eid)

    #return jsonify({"status":"ok", "projeto": projeto, "issueslist": issueslist})
    return render_template("index.html", projetos = projetos, projeto = projeto, issueslist = issueslist)


if __name__ == '__main__':
    app.run("0.0.0.0", port=8000)
