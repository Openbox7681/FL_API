from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required ,get_jwt_identity
import werkzeug
from app import jwt
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
import os, pickle
import zipfile
from app.model.ClientModel import ClientModel
from app.model.GlobalModel import GlobalModel
from datetime import datetime
from sklearn.ensemble import VotingClassifier
from app.config import Config
import pandas as pd
import numpy as np
import pyminizip
import uuid


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'code': 201,
        'message': "token expired"
    })

PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
GLOBALFILE_FOLDER = '{}/globalmodel/'.format(PROJECT_HOME)


# zipfile example
def zip_list(file_path,password,to_path):
    zf = zipfile.ZipFile(file_path, 'r')
    zf.extractall(pwd = password, path = to_path)
    return zf.namelist()[1:]

def zip_file(file_path,password,to_path):
    with zipfile.ZipFile(to_path, 'w') as myzip:
        myzip.write(file_path)
        myzip.setpassword(password)

PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = '{}/uploads/'.format(PROJECT_HOME)
ENCRYPTED_FOLDER = '{}/encrypted/'.format(PROJECT_HOME)
KEYFILE_FOLDER = '{}/keyfile/'.format(PROJECT_HOME)

def create_new_folder(local_dir):
	newpath = local_dir
	if not os.path.exists(newpath):
		os.makedirs(newpath)
	return newpath

class QueryGlobalModel(Resource):
    def __init__(self, **kwargs):
            self.logger = kwargs.get('logger')
    def post(self):
        status = None 
        message = None
        data = None 
        args = reqparse.RequestParser()\
            .add_argument('globalModelId', type=str,location='json')\
            .parse_args()
        globalModelId = args.get('globalModelId')
        globalModel = GlobalModel.get_globalModel_by_global_id(globalModelId)
        if globalModel is not None :
            status = 200
            message = "成功"
            globalModelJson = {
                        "GlobalModelId" : globalModel.globalModelId,
                        "FilePath" : globalModel.filePath,
                        "FileName" : globalModel.fileName,
                        "ClientIdList" : globalModel.clientIdList
                        }
        else:
            status = 201
            message = "查無此Id"
            globalModelJson = None

        

        data = globalModelJson

        ClientIdList = globalModelJson["ClientIdList"].split(",")
        for clientId in ClientIdList:
            print(clientId)
            clientModel = ClientModel.get_clientModel_by_client_id(clientId)[0]
            client_ip = clientModel.clientIp
            client_port = clientModel.clientPort
            global_model_id = globalModelId
            file_path = globalModelJson["FilePath"] + globalModelJson["FileName"]
            hash_file_path = ENCRYPTED_FOLDER + "encrypted_data.bin"
            response = GlobalModel.passServer(client_ip, client_port, global_model_id ,file_path, hash_file_path)
        data = response
        return jsonify({
            "Status": status,
            "Message": message,
            "Data" : data
        })



class AggModel(Resource):
    def __init__(self, **kwargs):
            self.logger = kwargs.get('logger')
        
    def post(self):
        status = None 
        message = None
        data = None 
        args = reqparse.RequestParser()\
            .add_argument('clientIdList', type=list,location='json')\
            .parse_args()
        clientIdList = args.get('clientIdList')
        
        clientModelList = list()
        model_list = list()


        #利用ID取得所有Client ID得資料
        for clientId in clientIdList:
            clientModels = ClientModel.get_clientModel_by_client_id(clientId)
            if clientModels is not None :
                for clientModel in clientModels:
                    clientModelJson = dict()
                    FilePath = clientModel.filePath
                    FileName = clientModel.fileName
                    m_path = FilePath + "/" +FileName
                    m = pickle.load(open(m_path, "rb"))
                    model_list.append(m)
                    clientModelJson = {
                        "ClientId" : clientModel.clientId,
                        "ClientIp" : clientModel.clientIp,
                        "FilePath" : clientModel.filePath,
                        "FileName" : clientModel.fileName,
                        "m_path" : m_path,
                        "config" : Config.TRAIN_DATA
                    }
                    clientModelList.append(clientModelJson)

        malware_train = pd.read_csv(Config.TRAIN_DATA + "mal_server_train.csv", index_col=[0])
        benign_train = pd.read_csv(Config.TRAIN_DATA + "benign_server_train.csv", index_col=[0])
        malware_train = malware_train[malware_train['class'] != 'T0836']

        print(malware_train)
        print(benign_train)

        X_train, Y_train, preds =  GlobalModel.processData(benign_train,malware_train)


        estimators_list = list()
        for i in range(len(model_list)):
            tuple_model = ('xgb' + str(i) , model_list[i])
            estimators_list.append(tuple_model)
        eclf = VotingClassifier(estimators=estimators_list, voting='soft')

        estimator = eclf.fit(X_train,Y_train)

        create_new_folder(GLOBALFILE_FOLDER)

        #檔案壓縮後存入
        pickle.dump(estimator, open(GLOBALFILE_FOLDER+"global_model.pickle.dat", "wb"))
        GLOBALMODEL_FILE = GLOBALFILE_FOLDER+"global_model.pickle.dat"
        GLOBALMODEL_ZIP = GLOBALFILE_FOLDER+"global_model.zip"
        compression_level = 5
        pyminizip.compress(GLOBALMODEL_FILE, None, GLOBALMODEL_ZIP, "123", compression_level)


        globalModelId = uuid.uuid4()

        globalModel = GlobalModel(
                    globalModelId= globalModelId,
                    filePath = GLOBALFILE_FOLDER, 
                    fileName =  "global_model.zip" , 
                    createTime = datetime.now(),
                    clientIdList = ",".join(clientIdList)
        )

        GlobalModel.insert_globalModel(globalModel)     

        status = 200
        message = "上傳成功"
        data = {
            "GloblaModelId" : globalModel.globalModelId
        }
        

        return jsonify({
            "Status": status,
            "Message": message,
            "Data" : data
        })






    



