from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateTimeField
from wtforms.validators import DataRequired, Length, Required
from wtforms.fields.html5 import DateTimeLocalField


class AddAssetForm(FlaskForm):
    assetID = StringField('Asset ID', validators=[DataRequired()])
    assetName = StringField('Asset Name', validators=[DataRequired()])
    submit = SubmitField('Submit Data')


class AddWorkerForm(FlaskForm):
    workerID = StringField('Worker ID', validators=[DataRequired()])
    workerName = StringField('Worker Name', validators=[DataRequired()])
    submit = SubmitField('Submit Data')


class AddTaskForm(FlaskForm):
    taskID = StringField('Task ID', validators=[DataRequired()])
    taskName = StringField('Task Name', validators=[DataRequired()])
    taskDetails = StringField('Task Description', validators=[DataRequired(), Length(min=10, max=100)])
    submit = SubmitField('Submit Data')


class AddAssignmentForm(FlaskForm):
    assetID = StringField('Asset ID', validators=[DataRequired()])
    taskID = StringField('Task ID', validators=[DataRequired()])
    workerID = StringField('Worker ID', validators=[DataRequired()])
    startTime = StringField('Start Date', validators=[DataRequired()])
    endTime = StringField('End Date', validators=[DataRequired()])
    submit = SubmitField('Submit Data')


class GetTasksForm(FlaskForm):
    workerID = StringField('Worker ID', validators=[DataRequired()])
    submit = SubmitField('Submit Data')
