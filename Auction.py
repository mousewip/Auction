import  datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, func

app = Flask(__name__)
app.config.from_pyfile('config.cfg')

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    items = db.relationship('Items', backref='user', lazy = True)

    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

class Items(db.Model):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    start_time = Column(DateTime, default=datetime.datetime.utcnow)

    def __init__(self, id, name, des, user_id):
        self.id = id
        self.name = name
        self.description = des
        self.user_id = user_id

class Bid(db.Model):
    __tablename__ = 'bid'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    item_id = Column(Integer, ForeignKey('items.id'))
    price = Column(Float, nullable=False)
    def __init__(self,id, uid, iid, price):
        self.id = id
        self.user_id = uid
        self.item_id = iid
        self.price = price


@app.route('/insert')
def Insert():
    user1 = User(1, "abc", "abc")
    user2 = User(2, "Phong", "911")
    user3 = User(3, "Tan", "XYZ123")
    db.session.add(user1)
    db.session.add(user3)
    db.session.add(user2)
    db.session.commit()

    baseball = Items(1, "BaseBall", "abc xyz", 1)
    db.session.add(baseball)

    baseball2 = Items(2, "BaseBall22", "abc xyz22", 2)
    db.session.add(baseball2)
    db.session.commit()

    bid1 = Bid(1, 2, 1, 25000)
    bid2 = Bid(2, 3, 1, 14000)
    bid3 = Bid(3, 2, 1, 36000)
    bid4 = Bid(4, 3, 1, 30000)

    bid5 = Bid(5, 1, 2, 40000)
    db.session.add(bid1)
    db.session.add(bid2)
    db.session.add(bid3)
    db.session.add(bid4)
    db.session.add(bid5)
    db.session.commit()

    return "Inserted" + '</br></br>  <a href="#" onClick="history.go(-1);return true;"> Go Back!</a>'
@app.route('/show')
def Show():
    item_id = 1
    result = Bid.query.filter(Bid.item_id == item_id).order_by(Bid.price.desc()).first()

    user = User.query.filter(User.id == result.user_id).first()

    # max_price = db.session.query(db.func.max(Bid.price)).scalar()
    # result = db.session.query(Bid).filter(Bid.price == max_price).all()
    rs = ""

    print("%d : %.2f" % (result.user_id, result.price))
    rs += str(result.user_id) + " : " + str(result.price) + "</br>"

    # for bid in result:
    #     print("%d : %.2f" %(bid.user_id, bid.price))
    #     rs += str(bid.user_id) + " : " + str(bid.price) + "</br>"

    #print(str(result.price))
    return user.username + " : " +  rs + '</br></br>  <a href="#" onClick="history.go(-1);return true;"> Go Back!</a>'
@app.route('/createall')
def CreateBD():
    db.create_all()
    return 'Create all schema success </br></br>  <a href="#" onClick="history.go(-1);return true;"> Go Back!</a> '

@app.route('/removeall')
def RemoveBD():
    db.drop_all()
    return 'Remove all schema success </br></br>  <a href="#" onClick="history.go(-1);return true;"> Go Back!</a> '


@app.route('/')
def Init():
    return "<a href='/createall'>CREATE SCHEMA </a> </br> </br> <a href='/removeall'>DROP ALL SCHEMA </a> </br> </br> <a href='/insert'>INSERT DATA </a> </br> </br> <a href='/show'>SHOW QUERY</a>"


if __name__ == '__main__':
    app.run(debug=True)
