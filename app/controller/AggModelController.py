from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required ,get_jwt_identity
# from app.model.User import User
# from app.model.Role import Role
import werkzeug
from app import jwt
import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES, PKCS1_OAEP
import os
import zipfile
from app.model.ClientModel import ClientModel
from datetime import datetime


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'code': 201,
        'message': "token expired"
    })

# zipfile example
def zip_list(file_path,password,to_path):
    zf = zipfile.ZipFile(file_path, 'r')
    zf.extractall(pwd = password, path = to_path)
    return zf.namelist()[1:]

PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = '{}/uploads/'.format(PROJECT_HOME)
ENCRYPTED_FOLDER = '{}/encrypted/'.format(PROJECT_HOME)
KEYFILE_FOLDER = '{}/keyfile/'.format(PROJECT_HOME)

def create_new_folder(local_dir):
	newpath = local_dir
	if not os.path.exists(newpath):
		os.makedirs(newpath)
	return newpath

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

        #利用ID取得所有Client ID得資料
        for clientId in clientIdList:
            clientModels = ClientModel.get_clientModel_by_client_id(clientId)
            for clientModel in clientModels:
                clientModelJson = dict()
                clientModelJson = {
                    "ClientId" : clientModel.clientId,
                    "ClientIp" : clientModel.clientIp,
                    "FilePath" : clientModel.filePath,
                    "FileName" : clientModel.fileName
                }
                clientModelList.append(clientModelJson)

        status = 200
        message = "上傳成功"
        data = clientModelList
        

        return jsonify({
            "Status": status,
            "Message": message,
            "Data" : data
        })






    



