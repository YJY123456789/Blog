import random

from flask import Blueprint, render_template, request, session, redirect, url_for, g
from App.models import *

blue = Blueprint('user', __name__)


# 首页
@blue.route('/')
def index():
    sorts=Sort.query.filter(Sort.num>0)
    article = Article.query.limit(6)
    page=(Article.query.count())//6+2
    data={
        'sorts':sorts,
        'article':article,
        'page':page
    }
    return render_template('home/index.html',data=data)

@blue.route('/page/<int:num>/')
def page(num):
    num=num
    sorts=Sort.query.filter(Sort.num>0)
    article = Article.query.offset((num-1)*6).limit(6)
    page=(Article.query.count())//6+2
    print(page)
    data={
        'sorts':sorts,
        'article':article,
        'page':page
    }
    return render_template('home/index.html',data=data)



@blue.route('/myindex/<string:name>/')
def myindex(name):
    data = Sort.query.filter_by(name=name).first()
    sorts =Sort.query.all()
    page=Sort.query.filter_by(name=name).first().num//6+2
    mydata = {
        'data':data,
        "sorts":sorts,
        'page':page,
    }
    return render_template('home/index.html',data=mydata)
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
    if session.get("name"):
        return render_template('admin/index.html',name=session.get("name"))
    else:
        return redirect(url_for('user.login'))

@blue.route('/login/',methods=["GET","POST"])
def login():
    if request.method =="POST":
        name = request.form.get('username')
        pwd = request.form.get('userpwd')
        user=User.query.all()
        for x in user:
            if x.name !=name or x.password != pwd:
                continue
            else:
                session['name'] = name
                break
        else:
            return "账户或者密码错误"
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
        id = request.form.get('category')
        myarticle = Article.query.filter_by(id=id).first()
        myarticle.name = title
        myarticle.content = content
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
    data={
        'data':data,
        'sort':Sort.query.all()
    }
    return render_template('admin/update-article.html',data=data)


@blue.route("/movearticle/<int:id>/")
def movearticle(id):
    mya = Article.query.filter_by(id=id).first()
    s=Sort.query.filter_by(id=mya.my_sort).first()
    c=s.num
    s.num=c-1
    if s.num ==0:
        db.session.delete(s)
    else:
        db.session.add(s)
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
        myid = request.form.get('fid')
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
        cate = request.form.get('category')
        a = Article()
        a.name = title
        a.content = content
        a.pic=random.randint(1,12)
        if tags:
            s = Sort()
            s.name = tags
            s.num = Sort.query.filter_by(name=tags).count()+1

            try:
                db.session.add(s)
                db.session.commit()
            except:
                db.session.rollback()
                db.session.flush()
            a.my_sort = Sort.query.filter_by(name=tags).first().id
            try:
                db.session.add(a)
                db.session.commit()

            except:
                db.session.rollback()
                db.session.flush()
            return redirect(url_for('user.article'))
        else:
            a.my_sort = cate
            so = Sort.query.filter_by(id=cate).first()
            c=so.num
            so.num=c+1
            try:
                db.session.add(a)
                db.session.commit()
                try:
                    db.session.add(so)
                    db.session.commit()
                except:
                    db.session.rollback()
                    db.session.flush()
            except:
                db.session.rollback()
                db.session.flush()
            return redirect(url_for('user.article'))
    name=session.get('name')
    sorts = Sort.query.all()
    data={
        'name':name,
        'sorts':sorts
    }
    return render_template('admin/add-article.html',data=data)
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
            s.num=0
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
@blue.route('/register/',methods=['GET','POST'])
def register():
    if request.method == "POST":
        pwd = request.form.get('userpwd')
        checkpwd = request.form.get('checkuserpwd')
        username = request.form.get('username')
        user=User.query.all()
        for x in user:
            if username == x.name:
                return render_template('admin/register.html',data='用户名已存在')
                break
            else:
                continue
        else:
            if pwd == checkpwd:
                myuser = User()
                myuser.name =username
                myuser.password = pwd
                try:
                    db.session.add(myuser)
                    db.session.commit()
                except:
                    db.session.roolback()
                    db.session.flush()
                return render_template('admin/login.html')
            else:
                return render_template('admin/register.html',date='密码错误')
    return render_template('admin/register.html')

