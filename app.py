import os
from flask import Flask, render_template, request, redirect, url_for
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy

current_dir = os.path.abspath(os.path.dirname(__file__))


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///"+os.path.join(current_dir,"database25.sqlite3")
db = SQLAlchemy()
db.init_app(app)
app.app_context().push()


class Username(db.Model):
   __tablename__ = "username"
   id = db.Column(db.Integer, primary_key=True)
   nam = db.Column(db.String, nullable=False)

class List(db.Model):
   __tablename__ = "list"
   listid = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String, nullable=False)
   description = db.Column(db.String)
   cards = db.relationship('Card', backref='poster')

class Card(db.Model):
   __tablename__="card"
   cardid = db.Column(db.Integer, primary_key=True)
   title = db.Column(db.String, nullable=False)
   content = db.Column(db.String)
   deadline = db.Column(db.String)
   ecardid = db.Column(db.Integer, db.ForeignKey("list.listid"))




@app.route('/',methods=['GET','POST'])
def home():
   return render_template('home.html')



@app.route('/adduser',methods=['GET','POST'])
def adduser():
   if request.method == 'POST':
      data = Username(nam=request.form['nm'])
      db.session.add(data)
      db.session.commit()

      username= Username.query.filter_by(nam = request.form['nm']).first()

      return render_template("result.html",username=username)



@app.route('/logout',methods=['GET','POST'])
def logout():
   return render_template('logout.html')



@app.route('/addlist/<int:id>',methods=['GET','POST'])
def addlist(id):

   username = Username.query.filter_by(id=id).first()

   if request.method == 'GET':
      return render_template('addlist.html',username=username)

   elif request.method == 'POST':
      data = List(name=request.form['top'], description=request.form['des'])
      db.session.add(data)
      db.session.commit()

      list = List.query.filter_by(name = request.form['top']).first()

      lists = List.query.all()
         
   return render_template('list.html',list=list, lists=lists, username=username)




@app.route('/addlist/<int:id>/<int:listid>/edit',methods=['GET','POST'])
def edit(id,listid):

   username = Username.query.filter_by(id=id).first()

   list = List.query.filter_by(listid=listid).first()

   if request.method == 'GET':
      return render_template('update.html',username=username, list=list)


   elif request.method == 'POST':
      lid = list.listid
      db.session.delete(list)
      up = List(listid=lid,name=request.form['listname'])
      db.session.add(up)

      db.session.commit()

      list = List.query.filter_by(listid=listid).first()

      lists = List.query.all()

      return render_template('list.html',username=username,list=list, lists=lists)


   

@app.route('/addlist/<int:id>/<int:listid>/delete',methods=['GET','POST'])
def delete(id,listid):

   username = Username.query.filter_by(id=id).first()

   listid = List.query.filter_by(listid=listid).first()

   db.session.delete(listid)
   db.session.commit()

   lists = List.query.all()

   return render_template('list.html',username=username, lists=lists)




@app.route('/addcard/<int:id>/<int:listid>',methods=['GET','POST'])
def addcard(id,listid):

   poster = listid

   username = Username.query.filter_by(id=id).first()

   list = List.query.filter_by(listid=listid).first()

   if request.method == 'GET':
      return render_template('card.html',username=username, list=list)

   elif request.method == 'POST':


      data = Card(title=request.form['t1'], content=request.form['c1'], deadline=request.form['d1'], ecardid = poster)
      db.session.add(data)
      db.session.commit()

      lists = List.query.all()

      card = Card.query.filter_by(ecardid = poster).first()

      cards = Card.query.all()


   return render_template('listcard.html', username=username, list=list, lists=lists, cards=cards, card=card)





@app.route('/addcard/<int:id>/<int:listid>/<int:cardid>/edit',methods=['GET','POST'])
def editcard(id,listid,cardid):

   username = Username.query.filter_by(id=id).first()

   list = List.query.filter_by(listid=listid).first()

   lists = List.query.all()

   card = Card.query.filter_by(cardid=cardid).first()


   if request.method == 'GET':
      return render_template('updatecard.html',username=username, list=list, card=card, lists=lists)


   elif request.method == 'POST':

      data = List.query.filter_by(name=request.form['lists']).first()

      ecardid = data.listid

      ''''up = List(listid=cid,name=request.form['listname'])

      daya1 = List.query.filter_by(name=request.form['val']).first()

      data = Card.query.filter_by(cardid=cardid).first()'''
      db.session.commit()

      card = Card.query.filter_by(cardid=cardid).first()


      lists = List.query.all()

      cards = Card.query.all()

      return render_template('listcard.html',username=username,list=list, lists=lists, cards=cards, card=card, ecardid=listid)



   
@app.route('/addcard/<int:id>/<int:listid>/<int:cardid>/delete',methods=['GET','POST'])
def deletecard(id,listid,cardid):

   username = Username.query.filter_by(id=id).first()

   list = List.query.filter_by(listid=listid).first()

   card = Card.query.filter_by(cardid=cardid).first()

   db.session.delete(card)
   db.session.commit()

   lists = List.query.all()

   cards = Card.query.all()


   return render_template('listcard.html',username=username, lists=lists, cards=cards, card=card, list=list)




if __name__ == '__main__':
   app.run(debug = True)