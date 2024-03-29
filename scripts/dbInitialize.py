import hashlib
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:ji394iii@192.168.70.98:8459/FL_RESULT'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
bcrypt = Bcrypt()


#Client模型名稱
class ClientModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    clientId = db.Column(db.String(45))
    clientIp = db.Column(db.String(45))
    clientPort = db.Column(db.String(45))
    filePath = db.Column(db.String(128))
    fileName = db.Column(db.String(45))
    createTime = db.Column(db.DateTime , nullable=False)



    def __init__(self, clientId, clientIp, clientPort ,filePath, fileName , createTime):
        self.clientId = clientId
        self.clientIp = clientIp
        self.clientPort = clientPort
        self.filePath = filePath
        self.fileName = fileName
        self.createTime = createTime


class GlobalModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    globalModelId = db.Column(db.String(45))
    filePath = db.Column(db.String(128))
    fileName = db.Column(db.String(45))
    createTime = db.Column(db.DateTime , nullable=False)
    clientIdList = db.Column(db.String(128))



    def __init__(self, globalModelId, filePath, fileName, createTime, clientIdList):
        self.globalModelId = globalModelId
        self.filePath = filePath
        self.fileName = fileName
        self.createTime = createTime
        self.clientIdList = clientIdList



db.create_all()



db.session.commit()


db.session.close()
