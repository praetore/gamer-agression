import arrow
from flask.ext.bootstrap import Bootstrap
from flask import Flask, render_template, session, url_for, redirect, flash
from flask.ext.mongoalchemy import MongoAlchemy
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

__author__ = 'Darryl'

app = Flask(__name__)
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'bl4ckb0X'
app.config['MONGOALCHEMY_DATABASE'] = 'project3'
db = MongoAlchemy(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        new_name = form.name.data.title()
        if old_name is not None and old_name != new_name:
            flash('Looks like you have changed your name!')
        session['name'] = new_name
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))


@app.route('/time')
def show_time():
    current_time = arrow.now('Europe/Amsterdam')
    return render_template('time.html', current_time=current_time)


@app.route('/user')
@app.route('/user/<name>')
def get_name(name=""):
    return render_template('user.html', name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', e=e), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', e=e), 500


class NameForm(Form):
    name = StringField('What\'s your name?', validators=[Required()])
    submit = SubmitField('Submit')


if __name__ == '__main__':
    app.run(debug=True)