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


def valid_slug(obj, text):
    
    newslug = slugify(text)
    s = newslug

    ct = 0
    while True:
        have = obj.get(Filter.slug==newslug)
        if not have:
            return newslug
        else:
            ct+=1
            newslug = "%s-%d" % (s, ct)


@app.route("/")
def index():
    projetos = Projects.all()
    return render_template("index.html", projetos=projetos)


@app.route("/add_project", methods=("POST",))
def addprojetc():
    data = request.form.get 

    newp = Projects.insert({"name": data("name"), "slug":valid_slug(Projects,data("name"))})
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
    data = request.form.get

    newp = Milestones.insert({"name": data("name"), "project_id": int(data("pid")), "slug": valid_slug(Milestones,data("name"))})
    newmilestone = Milestones.get(eid=newp)
    newmilestone['eid'] = newmilestone.eid

    return jsonify({"status": "ok", "message":"Milestone added", "object": newmilestone })


@app.route("/rm_milestone", methods=("POST",))
def del_milestone():
    data = request.form.get 
    
    mid = int(data("mid"))

    Milestones.remove(eids=[mid])

    return jsonify({"status":"ok","message":"Milestone removed" })


@app.route("/<project_slug>/")
def listissues(project_slug):
    projeto = Projects.get(Filter.slug==project_slug)
    if not projeto:
        return redirect("/")
    projeto['eid'] = projeto.eid
    milestones = Milestones.search(Filter.project_id==projeto.eid)
    
    issueslist = [ complete_issue(issue) for issue in Issues.search(Filter.project_id==projeto.eid)]
    projetos = Projects.all()

    #return jsonify({"status":"ok", "projeto": projeto, "issueslist": issueslist})
    return render_template("index.html", projetos = projetos, milestones = milestones, projeto = projeto, issueslist = issueslist)


@app.route("/<project_slug>/<milestone_slug>/")
def listissuesmilestone(project_slug, milestone_slug):

    projeto = Projects.get(Filter.slug==project_slug)
    if not projeto:
        return redirect("/")
    projeto['eid'] = projeto.eid

    milestone = Milestones.get( (Filter.project_id==projeto.eid) & (Filter.slug==milestone_slug) )
    if not milestone:
        return redirect("listissues", project_slug=project_slug)
    milestone['eid'] = milestone.eid

    issueslist = [ complete_issue(issue) for issue in Issues.search( (Filter.project_id==projeto.eid) & (Filter.milestone_id==milestone.eid) )]

    projetos = Projects.all()
    milestones = Milestones.search( Filter.project_id==projeto.eid )

    #return jsonify({"status":"ok", "projeto": projeto, "issueslist": issueslist})
    return render_template("index.html", projetos = projetos, milestones = milestones, projeto = projeto, milestone = milestone, issueslist = issueslist)


def complete_issue(issue):
    
    if issue['project_id']:
        proj = Projects.get(eid=issue['project_id'])
        issue['project'] = proj
    
    if issue['milestone_id']:
        milestone = Milestones.get(eid=issue['milestone_id'])
        issue['milestone'] = milestone
    
    return issue


@app.route("/add_issue", methods=("POST",))
def add_issue():
    data = request.form.get

    name = data("name")
    pid = data("pid")
    mid = data("mid")
    status = data("status")
    tipo = data("tipo")
    prioridade = data("prioridade")

    newid = Issues.insert({
        "name": name,
        "project_id": int(pid),
        "milestone_id": int(mid),
        "status": status,
        "tipo": tipo,
        "prioridade": prioridade,
    })
    newissue = Issues.get(eid=newid)
    newissue['eid'] = newissue.eid

    return jsonify({"status":"ok", "message":"Issue added", "object": complete_issue(newissue)})

if __name__ == '__main__':
    app.run("0.0.0.0", port=8000)
