from app import db
from flask_bcrypt import Bcrypt
import pandas as pd
import numpy as np
import pyminizip, glob
import requests
#Client模型名稱
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

    #利用id 取得 GlobalModel資料
    @staticmethod
    def get_globalModel(id):
        return GlobalModel.query.filter(GlobalModel.id == id).first()
    
    #取得所有模型
    @staticmethod
    def get_all_globalModels():
        return GlobalModel.query.all()

     #新增模型
    @staticmethod
    def insert_globalModel(globalModel):
        db.session.add(globalModel)
        db.session.commit()
        return globalModel 
    
    
    #模型更新
    @staticmethod
    def update_globalModel(globalModel):
        db.session.merge(globalModel)
        db.session.commit()
        return globalModel

    
    #利用ClientId 取得多筆ClientModel資料
    @staticmethod
    def get_globalModel_by_global_id(globalModelId):
        return GlobalModel.query.filter(GlobalModel.globalModelId == globalModelId).first()


    #Global Model 資料前組裡 , 給定資料集合輸出訓練資料
    @staticmethod
    def processData(benign, malware):
        label_table = {"Benign":0,"T0803":3,"T0804":1,"T0808":3,"T0841":2,"T0846":2,"T0855":3}
        preds = list(malware.columns)
        
        be = benign.copy()
        df = pd.concat([be, malware], axis=0)
        
        def mapping_y(m):
            encode = int()
            for k, v in label_table.items():
                if m == k:
                    encode = v
                    break
            return encode
        Y = df["class"].apply(mapping_y).values
        
        # 刪掉 label
        df.drop("class", axis=1, inplace=True)

        preds.remove("class")
        preds.remove("dst_ip")
        preds.remove("src_ip")
        preds.remove("timestamp")
        df = df[preds].astype("float")
        
        # 數值過大 以 1E6 替換
        df.replace(np.inf, 1E6, inplace=True)
        df.fillna(0, inplace=True) 
        
        return df, Y, preds
    @staticmethod
    def zip(model_path, zip_name, password):
        list_files = glob.glob(model_path + '*')
        print(list_files)
        compression_level = 4
        pyminizip.compress_multiple(list_files, [], zip_name, password, compression_level)

    @staticmethod
    def passServer(client_ip, client_port, global_model_id ,file_path, hash_file_path):
        url = "http://" + client_ip + ":" + client_port + "/eta/v1/uploadGlobalModel"

        print(url)

        payload={'model_id': global_model_id}

        files=[('hashfile',('encrypted_data.bin',open(hash_file_path,'rb'),'application/octet-stream')),
        ('file',('global_model.zip',open(file_path,'rb'),'application/zip'))]

        headers = {}
        response = requests.request("POST", url, headers=headers, data=payload, files=files)

        print(response.text)

        return response.text
    
