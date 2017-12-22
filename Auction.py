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
    db.session.commit()

    bid1 = Bid(1, 2, 1, 25)
    bid2 = Bid(2, 3, 1, 14)
    bid3 = Bid(3, 2, 1, 36)
    bid4 = Bid(4, 3, 1, 36)
    db.session.add(bid1)
    db.session.add(bid2)
    db.session.add(bid3)
    db.session.add(bid4)
    db.session.commit()

    return "Inserted"
@app.route('/show')
def Show():
    #result = Bid.query.order_by(Bid.price.desc()).first()

    max_price = db.session.query(db.func.max(Bid.price)).scalar()
    result = db.session.query(Bid).filter(Bid.price == max_price).all()
    rs = ""
    for bid in result:
        print("%d : %.2f" %(bid.user_id, bid.price))
        rs += str(bid.user_id) + " : " + str(bid.price) + "</br>";

    #print(str(result.price))
    return rs



@app.route('/')
def Init():
    db.create_all()
    return "<a href='/insert'>INSERT DATA</a> </br> <a href='/show'>SHOW QUERY</a>"


if __name__ == '__main__':
    app.run(debug=True)
