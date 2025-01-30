from flask import Flask, render_template, url_for, redirect, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, logout_user, current_user, login_required
from flask_bcrypt import Bcrypt 
# from configYaml import *
from questionnier_manipulator import changeTitle,addQuestion, changeDescription, deleteQuestion, getMetadataDescription, getMetadataTitle, readJson, validateAndReadJson

import os
from dotenv import load_dotenv, dotenv_values 

from typing import List, Optional
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, join
from form import RegisterForm, LoginForm
from helper import is_admin

load_dotenv("../config/.env") 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# app.config['TESTING'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.app_context().push()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

config_path = os.getenv("QUESTIONNAIRE_PATH")  # Replace with your actual file path
# config = read_config(config_path)
config = validateAndReadJson(config_path)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), nullable=False,unique=True)
    password = db.Column(db.String(80), nullable=False)

class SolvedQuestioneer(db.Model):
    __tablename__ = "solved_questioneer"

    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[str] = mapped_column(String(500), nullable=False)
    question: Mapped[str] = mapped_column(String(500), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))

    def __repr__(self) -> str:
        return f"SolvedQuestioneer(id={self.id!r}, user_id={self.user_id!r}, value={self.value!r}, question={self.question!r})"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register/', methods=['POST','GET'])
def register():
    form = RegisterForm()
    username=form.username.data
    if User.query.filter_by(username = username).first():
        return render_template('register.html',form=form, user_exists=True)
    if form.validate_on_submit():
        hash = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data,password=hash)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html',form=form)

@app.route('/login/', methods=['POST','GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))
    return render_template('login.html',form=form,access_denied=True)

@app.route('/dashboard', methods=['POST','GET'])
@login_required
def dashboard():
    return render_template('dashboard.html', is_admin=is_admin(current_user), is_sent=False)

@app.route('/logout', methods=['POST','GET'])
@login_required 
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/questionnaire', methods=['POST','GET'])
@login_required 
def questionnaire():
    list_questions = []
    list_responses = []
    config = readJson(config_path)
    if config:
        for item in config['questionnaire']['questions']:
            list_questions.append(str(item['question']))
            if(item['type']) == "multiple_choice":
                for option in item['options']:
                    pass
    else:
        return 404

    if request.method == 'POST':
        processed_data = {}
        data = request.form
        for key in data.keys():
            processed_data[key] = data.getlist(key)
        for item in config['questionnaire']['questions']:
            if(item['type']) == "multiple_choice":
                for option in item['options']:
                    pass
         
        for q_id, response in processed_data.items():
            list_responses.append(response)
        
        for idx, questions in enumerate(list_questions):
            db.session.add(SolvedQuestioneer(value=list_responses[idx][0], question=questions,user_id=current_user.id))
            db.session.commit()

        return  render_template('dashboard.html', is_admin=is_admin(current_user), is_sent=True)

    title = config['questionnaire']['title']
    description = config['questionnaire']['description']
    questions = config['questionnaire']['questions']

    return render_template('questionnaire.html',questionnaire=config,title=title, description=description,questions=questions)

@app.route('/questionnaire/manipulator', methods=['POST','GET'])
@login_required 
def questionnaire_manipulator():
    config = readJson(config_path)
    if is_admin(current_user):
        list_questions = []
        list_responses = []
        if config:
            for item in config['questionnaire']['questions']:
                list_questions.append(str(item['question']))
                if(item['type']) == "multiple_choice":
                    for option in item['options']:
                        pass
        else:
            return 404

        if request.method == 'POST':
            print(request.form)
            if (request.form['type']=="text"):
                addQuestion(request.form['text'], config_path)
            if (request.form['type']=="multiple_choice"):
                addQuestion(request.form['text'], config_path , type_of_question="multiple_choice",options=request.form["multiple_choice"].split(":"))
            session['message'] = "question added"
            return redirect(url_for('questionnaire_manipulator'))

        title = config['questionnaire']['title']
        description = config['questionnaire']['description']
        questions = config['questionnaire']['questions']
        try:
            if session['message']:
                message = session['message'] 
                session['message'] = None
                return render_template('questionnaire_manipulator.html',message=message ,questionnaire=config,title=title, description=description,questions=questions)
        except:
                message = None
                return render_template('questionnaire_manipulator.html',message=message ,questionnaire=config,title=title, description=description,questions=questions)
        return render_template('questionnaire_manipulator.html',questionnaire=config,title=title, description=description,questions=questions)
        

    return redirect(url_for('dashboard'))

@app.route('/questionnaire/manipulator/remove/<int:id>', methods=['GET'])
@login_required 
def questionnaire_manipulator_remove_question(id):
    if is_admin(current_user):
        deleteQuestion(id,config_path)
        session['message'] = "question with id:["+str(id)+"] has been deleted"
        return redirect(url_for('questionnaire_manipulator'))
    else:
        return 404

@app.route('/questionnaire/manipulator/titleAndDescription', methods=['GET','POST'])
@login_required 
def questionnaire_manipulator_edit_questionner_metadata():
    if is_admin(current_user):
        if request.method == 'POST':

            newDescription=request.form['description']
            newTitle=request.form['title']
            changeDescription(newDescription,config_path)
            changeTitle(newTitle,config_path)
            session['message']="Metadata has been updated"
            return  redirect(url_for('questionnaire_manipulator'))
        if request.method == 'GET':
            return render_template('questionnair_metadata_edit.html',title=getMetadataTitle(config_path), description=getMetadataDescription(config_path))
    else:
        return 404




@app.route('/report', methods=['GET']) 
@login_required 
def report():

    if is_admin(current_user):
        solved_questioneer=SolvedQuestioneer.query.all()
        q = User.query.join(SolvedQuestioneer, User.id==SolvedQuestioneer.user_id)
        q = SolvedQuestioneer.query.join(User, User.id==SolvedQuestioneer.user_id)
        q = q.add_columns(User)
        result = db.session.execute(q).all()
        
        return render_template('report.html',solved_questioneer=solved_questioneer,result=result)

    return  redirect(url_for('questionnaire'))


@app.route('/posts/delete/<int:id>', methods=['GET']) 
@login_required 
def delete_single_post(id):

    if is_admin(current_user):
        print("dsa")
        # print(SolvedQuestioneer.pp)
        post = SolvedQuestioneer.query.filter(SolvedQuestioneer.id==id).first()
        try:
            db.session.delete(post)
            db.session.commit()
        except:
            return "There was a issue deleting selected post"

        return redirect(url_for('report'))

    return  redirect(url_for('questionnaire'))

@app.route('/posts/<int:id>', methods=['GET','POST']) 
@login_required 
def view_single_post(id):

    if is_admin(current_user):
        post = SolvedQuestioneer.query.filter(SolvedQuestioneer.id==id).first()
        if request.method == 'POST':
            post.value=request.form['value']
            
            try:
                db.session.commit()



            except:
                return "There was an issue with updating of your post"
            q = SolvedQuestioneer.query.join(User, User.id==SolvedQuestioneer.user_id)
            q = q.add_columns(User).filter(User.id == id)
            result = db.session.execute(q).all()
            session['selected_user_id'] = request.form['user_id']

            return redirect('/user/report/'+request.form['user_id'])
       
        return render_template('edit_posts.html',item=post)


    return  redirect(url_for('questionnaire'))


@app.route('/user/report/<int:id>')
@login_required 
def report_by_id(id):
    try:
        if session['selected_user_id']:
            id = session['selected_user_id']
            session['selected_user_id'] = None
    except:
        print("no session id, all ok")
    if is_admin(current_user):
        solved_questioneer=SolvedQuestioneer.query.all()
        # q = User.query.join(SolvedQuestioneer, User.id==SolvedQuestioneer.user_id)
        q = SolvedQuestioneer.query.join(User, User.id==SolvedQuestioneer.user_id)
        q = q.add_columns(User).filter(User.id == id)
        result = db.session.execute(q).all()
        return render_template('report.html',solved_questioneer=solved_questioneer,result=result,id=id)

    return  redirect(url_for('questionnaire'))

@app.route('/managment', methods=['POST','GET'])
@login_required 
def managment():
    if is_admin(current_user):
        # solved_questioneer=SolvedQuestioneer.query.all()
        User.query.all()
        q = User.query.join(SolvedQuestioneer, User.id==SolvedQuestioneer.user_id)
        q = SolvedQuestioneer.query.join(User, User.id==SolvedQuestioneer.user_id)
        q = q.add_columns(User)
        # result = db.session.execute(q).all()
        return render_template('managment.html',users=User.query.all())
    return  redirect(url_for('dashboard'))

@app.route('/managment/delete/user/<int:id>')
@login_required
def delete_user(id):
    if is_admin(current_user):
        user = User.query.get_or_404(id)
        try:
            db.session.delete(user)
            db.session.commit()
            data =  SolvedQuestioneer.query.filter( SolvedQuestioneer.user_id == id).all()
            for i in data:
                try:
                    db.session.delete(i)
                except:
                    return "There was a issue in delete_userdata deleting selected task"
            try:
                db.session.commit()
                return redirect(url_for('managment'))
            except:          
                return "session commit issue"
        except:
            return "There was a issue deleting selected task"
    return  redirect(url_for('dashboard'))

@app.route('/managment/delete/userdata/<int:id>')
@login_required
def delete_userdata(id):
    data =  SolvedQuestioneer.query.filter( SolvedQuestioneer.user_id == id).all()
    for i in data:
        try:
            db.session.delete(i)
        except:
            return "There was a issue in delete_userdata deleting selected task"
    try:
        db.session.commit()
        return redirect(url_for('managment'))
    except:          
        return "session commit issue"


if __name__ == "__main__":
    if(validateAndReadJson(os.getenv("QUESTIONNAIRE_PATH"))== -1):
        print( "Json is not found or well formated, check .env variables - ",os.getenv("QUESTIONNAIRE_PATH"))
        exit()
    app.run(debug=True)