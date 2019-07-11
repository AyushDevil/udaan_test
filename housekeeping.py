from flask import Flask, render_template, url_for, flash, redirect, jsonify, json
from forms import AddAssetForm, AddWorkerForm, AddTaskForm, AddAssignmentForm, GetTasksForm
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'fa2f8d764b984e0af96fff26f2092d57'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
ma = Marshmallow(app)


class Asset(db.Model):
    assetid = db.Column(db.String(10), unique=True, primary_key=True)
    assetname = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Asset('{self.assetid}', '{self.assetname}')"


class Task(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    taskname = db.Column(db.String(100), nullable=False)
    taskdesc = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Task('{self.id}', '{self.taskname}')"


class Workers(db.Model):
    wid = db.Column(db.String(10), primary_key=True)
    workername = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"Workers('{self.wid}', '{self.workername}')"


class Assignment(db.Model):
    assignid = db.Column(db.Integer, primary_key=True)
    aid = db.Column(db.String(10), nullable=False)
    tid = db.Column(db.String(10), nullable=False)
    wid = db.Column(db.String(10), nullable=False)
    assigntime = db.Column(db.String(20), nullable=False, default=datetime.utcnow)
    exptime = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"Assignment('{self.assignid}', '{self.aid}', '{self.tid}', '{self.tid}', '{self.assigntime}', '{self.exptime}')"


class AssetSchema(ma.Schema):

    class Meta:
        fields = ('assetid', 'assetname')


asset_schema = AssetSchema()
asset_schema = AssetSchema(many=True)


class AssignSchema(ma.Schema):

    class Meta:
        fields = ('aid', 'tid', 'wid', 'assigntime', 'exptime')


assign_schema = AssignSchema()
assign_schema = AssignSchema(many=True)


@app.route("/", methods=["POST", "GET"])
@app.route("/add-asset", methods=["POST", "GET"])
def add_asset():
    form = AddAssetForm()
    if form.validate_on_submit():
        flash(f'Asset Successfully Added for {form.assetID.data}!', 'success')
        asset = Asset(assetid=form.assetID.data, assetname=form.assetName.data)
        db.session.add(asset)
        db.session.commit()
        return redirect(url_for('add_asset'))

    return render_template('addAsset.html', title='Add Asset', form=form)


@app.route("/asset/all", methods=["GET"])
def show_asset():
    asset_all = Asset.query.all()
    result = asset_schema.dump(asset_all)
    return jsonify(result.data)


@app.route("/add-worker", methods=["POST", "GET"])
def add_worker():
    form = AddWorkerForm()
    if form.validate_on_submit():
        flash(f'Worker Successfully Added for {form.workerID.data}!', 'success')
        worker = Workers(wid=form.workerID.data, workername=form.workerName.data)
        db.session.add(worker)
        db.session.commit()
        return redirect(url_for('add_worker'))
    return render_template('addWorker.html', title='Add Worker', form=form)


@app.route("/add-task", methods=["POST", "GET"])
def add_task():
    form = AddTaskForm()
    if form.validate_on_submit():
        flash(f'Task Successfully Added for {form.taskID.data}!', 'success')
        task = Task(id=form.taskID.data, taskname=form.taskName.data, taskdesc=form.taskDetails.data)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('add_task'))

    return render_template('addTask.html', title='Add Task', form=form)


@app.route("/allocate-task", methods=["POST", "GET"])
def add_assignment():
    form = AddAssignmentForm()
    if form.validate_on_submit():
        flash(f'Task Successfully Allocated to {form.workerID.data}!', 'success')
        altask = Assignment(aid=form.assetID.data, tid=form.taskID.data, wid=form.workerID.data,
                            assigntime=form.startTime.data, exptime=form.endTime.data)
        db.session.add(altask)
        db.session.commit()
        return redirect(url_for('add_assignment'))

    return render_template('AddAssignment.html', title='Add Task', form=form)


@app.route("/get-tasks-for-worker/", methods=["POST", "GET"])
def show_tasks():
    form = GetTasksForm()
    if form.validate_on_submit():
        wid = form.workerID.data
        assignment = Assignment.query.get(wid)
        result = assign_schema.dump(assignment)
        return jsonify(result.data)
    return render_template('gettasks.html', title='Get Task', form=form)


if __name__ == '__main__':
    app.run(debug=True)
