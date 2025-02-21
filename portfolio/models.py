from sqlalchemy import select,text, Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from werkzeug.security import generate_password_hash, check_password_hash
from typing import List
from portfolio import Base


job_skill = Table(
'job_skill',
Base.metadata,
Column("job_id", ForeignKey("work.id"), primary_key=True),
Column("skill_id", ForeignKey("skills.id"), primary_key=True)
)


class WorkORM(Base):
    __tablename__ = 'work'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    company = Column(String)
    start = Column(String)
    end = Column(String)
    description = Column(String)
    img = Column(String)

    skills: Mapped[List["SkillORM"]] = relationship("SkillORM",secondary='job_skill',back_populates='jobs')

class WorkDAO:
    def JobById(job_id, db):
        stm = select(WorkORM).where(WorkORM.id == job_id)
        job = db.session.scalar(stm)
        return job


    def AllJobs(db):
        stm = select(WorkORM)
        jobs = db.session.scalars(stm).all()
        print(jobs)
        return jobs


class SkillORM(Base):
    __tablename__ = 'skills'
    id = Column(Integer, primary_key=True)
    skill = Column(String)
    type = Column(String)
    description = Column(String)
    thumbnail = Column(String)
    jobs: Mapped[List["WorkORM"]] = relationship("WorkORM", secondary='job_skill', back_populates='skills')


class SkillDAO:
    def SkillById(skill_id, db):
        stm = select(SkillORM).where(SkillORM.id == skill_id)
        skill = db.session.scalar(stm)
        return skill


    def AllSkills(db):
        stm = select(SkillORM)
        skills = db.session.scalars(stm).all()
        return skills


class BlogORM(Base):
    __tablename__ = 'blogs'
    id = Column(Integer, primary_key=True)
    title = Column(String(75), nullable=False)
    blog = Column(String(1000), nullable=False)
    date = Column(String(8), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user: Mapped["UserORM"] = relationship("UserORM", back_populates="blogs")

class BlogDAO:
    def BlogById(blog_id, db):
        stm = select(BlogORM).where(BlogORM.id == blog_id)
        blog = db.session.scalar(stm)
        return blog


    def AllBlogs(db):
        stm = select(BlogORM)
        blogs = db.session.scalars(stm).all()
        return blogs


    def BlogsByUser(user_id, db):
        stm = select(BlogORM).where(BlogORM.user_id == user_id)
        blogs = db.session.scalars(stm).all()
        return blogs


class UserORM(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(25), unique=True, nullable=False)
    password_hash = Column(String(150), nullable=False)

    blogs: Mapped[List["BlogORM"]] = relationship("BlogORM", back_populates="user")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class UserDAO:
    def UserById(user_id, db):
        stm = select(UserORM).where(UserORM.id == user_id)
        user = db.session.scalar(stm)
        return user


    def UserByUsername(username, db):
        stm = select(UserORM).where(UserORM.username == username)
        user = db.session.scalar(stm)
        return user


    def AllUsers(db):
        stm = select(UserORM)
        users = db.session.scalars(stm).all()
        return users



































# class ProjectORM(Base):
#     __tablename__ = 'projects'
#     id = Column(Integer, primary_key=True)
#     title = Column(String)
#     description = Column(String)
#     reflection = Column(String)


# class ProjectDAO:
#     def AllProjects(db):
#         stm = select(ProjectORM)
#         projects = db.session.scalars(stm).all()
#         return projects

    # def AllWork(db):
    #     sql = f"SELECT job_id,job_title FROM work;"
    #     sql = text(sql)
    #     result = db.engine.connect().execute(sql)
    #     found_work = []
    #     for row in result:
    #         work = Work(row.job_title, row.job_id)
    #         found_work.append(work)
    #     return found_work

    # def JobById(job_id,db):
    #     sql = f"SELECT * FROM work WHERE job_id = {job_id};"
    #     sql_q = text(sql)
    #     result = db.engine.connect().execute(sql_q)
    #     row = next(iter(result))
    #     job = Work(row.job_title, row.job_id)
    #     return job