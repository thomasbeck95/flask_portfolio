from portfolio import app, db
from portfolio.models import *
from flask import flash, render_template, session, request, redirect, url_for
from sqlalchemy import text
from datetime import datetime


@app.route('/')
@app.route('/index')
def index():
    found_skills = SkillDAO.AllSkills(db)
    return render_template('index.html', title='Home', skills=found_skills)

@app.route('/work/')
def work():
    found_work = WorkDAO.AllJobs(db)
    return render_template('work.html', title='Work Experience', jobs = found_work)

@app.route('/work/<job_id>')
def job(job_id):
    found_work = WorkDAO.AllJobs(db)
    job_found = WorkDAO.JobById(job_id, db)
    return render_template('job.html', title='Work Experience', jobs = found_work, job = job_found)

@app.route('/skills/')
def skills():
    found_skills = SkillDAO.AllSkills(db)
    return render_template('skills.html', title='Skills', skills = found_skills)

@app.route('/skills/<skill_id>')
def skill(skill_id):
    found_skills = SkillDAO.AllSkills(db)
    skill_found = SkillDAO.SkillById(skill_id, db)
    return render_template('skill.html', title='Skill', skills = found_skills, skill = skill_found)


@app.route('/projects/')
def projects():
    return render_template('projects.html', title='Projects')



@app.route('/projects/trips')
def trips():
    return render_template('trips.html', title='Trips')


@app.route('/projects/products')
def products():
    return render_template('products.html', title='Product Catalog')


@app.route('/projects/message')
def mb_index():
    if "username" in session:
        return redirect(url_for('dashboard'))
    return render_template('mb_index.html', title='Message Board')


@app.route('/projects/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = UserDAO.UserByUsername(username, db)
    if user and user.check_password(password):
        session['username'] = username
        return redirect(url_for('dashboard'))
    else:
        flash("Error: Incorrect username or password")
        return render_template('mb_index.html', title='Message Board')


@app.route("/projects/register", methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    user = UserDAO.UserByUsername(username, db)
    if user:
        flash("Error: Username taken!")
        return render_template('mb_index.html', error="User already created!", title='Message Board')
    else:
        new_user = UserORM(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = username
        return redirect(url_for('dashboard'))



@app.route('/projects/dashboard', methods=["GET", "POST"])
def dashboard():
    if "username" in session:
        user = UserDAO.UserByUsername(session['username'], db)
        if not user:
            flash("Error: User not found!")
            return redirect(url_for('mb_index'))

        if request.method == "POST":
            title = request.form.get("title")
            blog_text = request.form.get("blogText")
            date = datetime.today().strftime('%d-%m-%Y')
            new_blog = BlogORM(title=title, blog=blog_text, date=date, user_id=user.id)
            db.session.add(new_blog)
            db.session.commit()
            flash("Success: Message post added!")
            return redirect(url_for('dashboard'))
        else:
            blogs = BlogDAO.AllBlogs(db)
            users = UserDAO.AllUsers(db)
            return render_template("dashboard.html", username=session['username'], blogs=blogs, users=users)
    return redirect(url_for('mb_index'))


@app.route("/projects/logout")
def logout():
    session.pop('username', None)
    return redirect(url_for('mb_index'))

