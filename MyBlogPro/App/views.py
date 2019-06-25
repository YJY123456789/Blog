import random

from flask import Blueprint, render_template, request, session, redirect, url_for, g
from App.models import *

blue = Blueprint('user', __name__)


# 首页
@blue.route('/')
def index():
    return render_template('home/index.html')
@blue.route('/myindex/<string:name>/')
def myindex(name):
    data = Sort.query.filter_by(name=name).first()
    return render_template('home/index.html',data=data)
@blue.route('/about/')
def about():
    res=request.url_root
    return render_template('home/about.html',res=res)
@blue.route('/gbook/')
def gbook():
    return render_template('home/gbook.html')
@blue.route('/info/')
def info():
    return render_template('home/info.html')

@blue.route('/infopic/')
def infopic():
    return render_template('home/infopic.html')

@blue.route('/list/')
def list():
    return render_template('home/list.html')

@blue.route('/share/')
def share():
    return render_template('home/share.html')
#后台



@blue.route('/addflink/')
def add_flink():
    return render_template('admin/add-flink.html')


@blue.route('/addnotice/')
def add_notice():
    return render_template('admin/add-notice.html')


@blue.route('/article/')
def article():
    data={
    'name':session.get('name'),
    "articles":Article.query.all()
    }
    return render_template('admin/article.html',data=data)


@blue.route('/category/')
def category():
    s =Sort.query.all()
    name = session.get('name')
    data={
        's':s,
        "name":name
    }
    return render_template('admin/category.html',data=data)
@blue.route('/comment/')
def commet():
    return render_template('admin/comment.html')
@blue.route('/flink/')
def flink():
    return render_template('admin/flink.html')
@blue.route('/index/')
def adminindex():
    name=session.get('name','请登录')

    return render_template('admin/index.html',name=name)
@blue.route('/login/',methods=["GET","POST"])
def login():
    if request.method =="POST":
        name = request.form.get('username')
        pwd = request.form.get('userpwd')
        if name == User.query.get(1).name and pwd == User.query.get(1).password:
            session['name'] = name
            return redirect(url_for('user.adminindex'))
    return render_template('admin/login.html')
@blue.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('user.adminindex'))
@blue.route('/loginlog/')
def loginlog():
    return render_template('admin/loginlog.html')
@blue.route('/manageuser/')
def manage_user():
    return render_template('admin/manage-user.html')
@blue.route('/notice/')
def notice():
    return render_template('admin/notice.html')
@blue.route('/readset/')
def readset():
    return render_template('admin/readset.html')
@blue.route('/setting/')
def setting():
    return render_template('admin/setting.html')
@blue.route('/updatearticle/',methods=["GET","POST"])
def update_article():
    if request.method == "POST":
        title = request.form.get('title')
        content = request.form.get('content')
        id = request.form.get('tags')
        myarticle =Article.query.filter_by(id=id).first()
        myarticle.name = title
        myarticle.content = content.replace('<','').replace('>','').replace('p','').replace('/','')
        try:
            db.session.add(myarticle)
            db.session.commit()
        except:
            db.session.roolback()
            db.session.flush()
        return redirect(url_for('user.article'))
    return render_template('admin/update-article.html')

@blue.route('/aarticle/<string:article>/')
def aarticle(article):
    data = Article.query.filter_by(name=article).first()
    return render_template('admin/update-article.html',data=data)


@blue.route("/movearticle/<int:id>/")
def movearticle(id):
    mya = Article.query.filter_by(id=id).first()
    try:
        db.session.delete(mya)
        db.session.commit()
    except:
        db.session.roolback()
        db.session.flush()
    return redirect(url_for('user.article'))
@blue.route('/mycatedate/<int:id>/')
def mycatedate(id):
    data = Sort.query.filter_by(id=id).first()
    return render_template('admin/update-category.html',data=data)
@blue.route("/movecategory/<int:id>/")
def movecategory(id):
    mysort=Sort.query.filter_by(id=id).first()
    db.session.delete(mysort)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        db.session.flush()
    return redirect(url_for('user.category'))


@blue.route('/updatecategory/',methods=["GET",'POST'])
def update_category():
    if request.method == "POST":
        myname =request.form.get("name")
        myothername=request.form.get('alias')
        myid = request.form.get('describe')[0:1]
        id=int(myid)
        mysort=Sort.query.filter_by(id=id).first()
        mysort.name=myname
        mysort.othername=myothername
        try:
            db.session.commit()
        except:
            db.session.rollback()
            db.session.flush()
        return redirect(url_for('user.category'))
    return render_template('admin/update-category.html')
@blue.route('/updateflink/')
def update_flink():
    return render_template('admin/update-flink.html')
@blue.route('/addarticle/',methods=['GET','POST'])
def add_article():
    if request.method == "POST":
        title = request.form.get('title')
        content = request.form.get('content')
        tags = request.form.get('tags')
        a = Article()
        a.name = title
        a.content = content.replace('<','').replace('p','').replace('>','').replace('br','').replace('/','')
        a.my_sort = Sort.query.filter_by(name=tags).first().id
        try:
            db.session.add(a)
            db.session.commit()
        except:
            db.session.rollback()
            db.session.flush()
        return redirect(url_for('user.article'))
    name=session.get('name')
    return render_template('admin/add-article.html',name=name)
@blue.route('/addcategory/',methods=['GET','POST'])
def add_category():
    if request.method == "POST":
        name = request.form.get('name')
        othername= request.form.get('alias')
        s=Sort()
        m = Sort.query.all()
        for x in m:
            if x.name == name and x.othername == othername:
                res=x.num+1
                c=Sort.query.filter_by(name=name).first()
                c.num=res
                try:
                    db.session.add(c)
                    db.session.commit()
                except:
                    db.session.roolback()
                    db.session.flush()
                break
            elif (x.name != name and x.othername == othername) or (x.name == name and x.othername != othername):
                break
            else:
                pass
        else:
            s.name = name
            s.othername=othername
            s.num=str(random.randint(1,162))
            try:
                db.session.add(s)
                db.session.commit()
            except:
                db.session.roolback()
                db.session.flush()
        return redirect(url_for('user.category'))
    return render_template('admin/add-category.html')
#
#
#
#
#


