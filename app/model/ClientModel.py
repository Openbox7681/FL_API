from app import db
from flask_bcrypt import Bcrypt


#Client模型名稱
class ClientModel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    clientId = db.Column(db.String(45))
    clientIp = db.Column(db.String(45))
    filePath = db.Column(db.String(128))
    fileName = db.Column(db.String(45))

    createTime = db.Column(db.DateTime , nullable=False)





    def __init__(self, clientId, clientIp, filePath, fileName , createTime):
        self.clientId = clientId
        self.clientIp = clientIp
        self.filePath = filePath
        self.fileName = fileName
        self.createTime = createTime
        

    #利用id 取得 ClientModel資料
    @staticmethod
    def get_clientModel(id):
        return ClientModel.query.filter(ClientModel.id == id).first()
    
    #取得所有模型
    @staticmethod
    def get_all_clientModels():
        return ClientModel.query.all()

     #新增模型
    @staticmethod
    def insert_clientModel(clientModel):
        db.session.add(clientModel)
        db.session.commit()
        return clientModel 
    
     #刪除角色
    @staticmethod
    def delete_role(clientModel):
        db.session.delete(clientModel)
        db.session.commit()
    
    #模型更新
    @staticmethod
    def update_clientModel(clientModel):
        db.session.merge(clientModel)
        db.session.commit()
        return clientModel

    #利用clientIp 取得多筆ClientModel資料
    @staticmethod
    def get_clientModel(clientIp):
        return ClientModel.query.filter(ClientModel.clientIp == clientIp).all()
    
    #利用ClientId 取得多筆ClientModel資料
    @staticmethod
    def get_clientModel(clientId):
        return ClientModel.query.filter(ClientModel.clientId == clientId).all()
