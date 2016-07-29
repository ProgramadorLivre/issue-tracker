# -*- encoding: utf-8 -*-

from flask import Flask, render_template, jsonify, request, redirect, abort
from slugify import slugify
from datetime import datetime
from peewee import *
from playhouse.shortcuts import model_to_dict

db = SqliteDatabase("issues.db")

# ==================================================== MODELS

class BaseModel(Model):
    class Meta:
        database = db

class SimpleTable(BaseModel):
    name = CharField() 
    slug = CharField()
    datetime = DateTimeField(default=datetime.now)

class Projects(SimpleTable):
    class Meta:
        db_table = "project"

class Types(SimpleTable):
    class Meta:
        db_table = "type"

class Prioritys(SimpleTable):
    class Meta:
        db_table = "priority"

class Status(SimpleTable):
    begin = BooleanField(default=False)
    end = BooleanField(default=False)
    class Meta:
        db_table = "status"

class Tags(SimpleTable):
    class Meta:
        db_table = "tag"


class Milestones(BaseModel):
    name = CharField()
    project_id = ForeignKeyField(Projects, related_name='milestones')
    slug = CharField()
    datetime = DateTimeField(default=datetime.now)
    class Meta:
        db_table = "milestone"

class Issues(BaseModel):
    name = CharField(),
    project_id = ForeignKeyField(Projects, related_name='issues')
    milestone_id = ForeignKeyField(Milestones, related_name='issues')
    type_id = ForeignKeyField(Types, related_name='issues')
    priority_id = ForeignKeyField(Prioritys, related_name='issues')
    status_id = ForeignKeyField(Status, related_name='issues')
    datetime = DateTimeField(default=datetime.now)
    class Meta:
        db_table = "issue"

class IssuesTags(BaseModel):
    issue_id = ForeignKeyField(Issues, related_name='issues')
    tag_id = ForeignKeyField(Tags, related_name='tags')

# ==================================================== FLASK APP/CONFIG

app = Flask(__name__)
app.debug = True

# ==================================================== UTIL METHODS

def valid_slug(klass, text):
    '''
    Verify if the slug already exists in the database
    '''
    newslug = slugify(text)
    s = newslug

    ct = 0
    while True:
        have = klass.select(klass.slug==newslug)
        if not have:
            return newslug
        else:
            ct+=1
            newslug = "%s-%d" % (s, ct)

# ==================================================== VIEWS

@app.route("/")
def index():
    projetos = Projects.select()
    return render_template("index.html", projetos=projetos)


@app.route("/add_project", methods=("POST",))
def addprojetc():
    data = request.form.get

    savedproject = Projects.create(
        name =  data("name"), 
        slug = valid_slug(Projects, data("name")),
    )
    
    return jsonify({"status":"ok","message":"Project added", "object": model_to_dict(savedproject) })


@app.route("/rm_project", methods=("POST",))
def del_project():
    data = request.form.get
    
    pid = int(data("pid"))

    proj = Projects.select().where(Projects.id == pid).get()
    if proj:
        proj.delete_instance()
    else:
        return abort(404)

    return jsonify({"status":"ok","message":"Project removed" })


@app.route("/add_milestone", methods=("POST",))
def addmilestone():
    data = request.form.get
    print(data)
    newmilestone = Milestones.create(
        name = data("name"), 
        project_id = int(data("pid")), 
        slug = valid_slug(Milestones, data("name")),
    )

    return jsonify({"status": "ok", "message":"Milestone added", "object": model_to_dict(newmilestone) })


@app.route("/rm_milestone", methods=("POST",))
def del_milestone():
    data = request.form.get 
    
    mid = int(data("mid"))

    mil = Milestones.select().where(Milestones.id == mid).get()
    if mil:
        mil.delete_instance()
    else:
        return abort(404)

    return jsonify({"status":"ok","message":"Milestone removed" })


def get_order(klass, order):
    '''
    Return the field of the class for 'order_by' clause.
    Must be the name of the field in the class.
    '''
    field, direction = request.args['order'].split(",")
    if "_" in field:
        '''
        if receives 'milestone_id' transform to 'Milestone.id' and 
        gets the memory object
        '''
        klassname = field.split("_")[0].capitalize()
        klass_fieldname = field.split("_")[1]
        fieldorder = eval( "{0}.{1}".format(klassname,klass_fieldname) )
    else:
        fieldorder = getattr(klass, field)[0]
    if direction == "desc":
        return fieldorder.desc()
    else:
        return fieldorder


@app.route("/<project_slug>/")
def listissues(project_slug):
    projeto = Projects.select().where(Projects.slug == project_slug).get()
    if not projeto:
        return redirect("/")

    milestones = Milestones.select().where(Milestones.project_id == projeto.id)
        
    if "order" in request.args.keys():
        issueslist = Issues.select().where(Issues.project_id == projeto.id) \
            .order_by(get_order(Issues, request.args['order']))
    else:
        issueslist = Issues.select().where(Issues.project_id == projeto.id)

    projetos = Projects.select()

    #return jsonify({"status":"ok", "projeto": projeto, "issueslist": issueslist})
    return render_template("index.html", projetos = projetos, milestones = milestones, projeto = projeto, issueslist = issueslist)


@app.route("/<project_slug>/<milestone_slug>/")
def listissuesmilestone(project_slug, milestone_slug):

    projeto = Projects.select().where(Projects.slug == project_slug).get()
    if not projeto:
        return redirect("/")

    milestone = Milestones.select() \
     .where( (Milestones.project_id == projeto.id) & (Milestones.slug == milestone_slug) ).get()
    if not milestone:
        return redirect("listissues", project_slug=project_slug)

    if "order" in request.args.keys():
        issueslist = Issues.select().join(Status).join(Milestones).join(Types) \
            .join(Prioritys).join(Projects) \
            .where(Issues.project_id == projeto.id) \
            .order_by(get_order(Issues, request.args['order']))
    else:
        issueslist = Issues.select().where(Issues.project_id == projeto.id)

    projetos = Projects.select()
    milestones = Milestones.select().where( Milestones.project_id == projeto.id )

    # =========================================== Milestone Counting Graph
    query = Issues.select(Issues, fn.Count(Issues.id)).join(Status)
    ct_data = {
        "total": query.where( (Issues.project_id==projeto.id) & (Issues.milestone_id==milestone.id) ).count(),
        "todo": query.where( (Issues.project_id==projeto.id) & (Issues.milestone_id==milestone.id) & (Status.begin==True) ).count(),
        "doing": query.where( (Issues.project_id==projeto.id) & (Issues.milestone_id==milestone.id) & (Status.end==False & Status.begin==False) ).count(),
        "done": query.where( (Issues.project_id==projeto.id) & (Issues.milestone_id==milestone.id) & (Status.end==True) ).count(),
    }
    if ct_data['total'] == 0:
        ct_data['total'] = 100
    ct_data['todo_perc'] = round( (ct_data['todo'] * 100)/ct_data['total'] ,1)
    ct_data['doing_perc'] = round( (ct_data['doing'] * 100)/ct_data['total'] ,1)
    ct_data['done_perc'] = round( (ct_data['done'] * 100)/ct_data['total'] ,1)

    #return jsonify({"status":"ok", "projeto": projeto, "issueslist": issueslist})
    return render_template("index.html", projetos = projetos, 
        milestones = milestones, projeto = projeto, milestone = milestone, 
        cts = ct_data, issueslist = issueslist)



@app.route("/add_issue", methods=("POST",))
def add_issue():
    data = request.form.get

    name = data("name")
    pid = data("pid")
    mid = data("mid")
    status = data("status")
    type_issue = data("type")
    priority = data("priority")

    newissue = Issues.create(
        name = name,
        project_id = int(pid),
        milestone_id = int(mid),
        status_id = status,
        type_id = type_issue,
        priority_id = priority
    )

    return jsonify({"status":"ok", "message":"Issue added", "object": complete_issue(newissue)})

if __name__ == '__main__':
    app.run("0.0.0.0", port=8080)
