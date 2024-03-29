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
from app.model.GlobalModel import GlobalModel

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
    if len(zf.namelist()) >1:
        ziplist = zf.namelist()[1:]
    else :
        ziplist = zf.namelist()
    return ziplist

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

class uploadModel(Resource):
    def __init__(self, **kwargs):
            self.logger = kwargs.get('logger')
        
    def post(self):
        status = None 
        message = None
        data = None 
        args = reqparse.RequestParser()\
            .add_argument('file', type=werkzeug.datastructures.FileStorage,location='files')\
            .add_argument('hashfile', type=werkzeug.datastructures.FileStorage,location='files')\
            .add_argument('clientId', type = str ,required = True)\
            .add_argument('clientIp', type = str ,required = True)\
            .add_argument('clientPort', type = str ,required = True)\
            .parse_args()

        files = args.get("file")
        hashfiles = args.get("hashfile")
        clientId = args.get('clientId')
        clientIp = args.get('clientIp')
        clientPort = args.get('clientPort')
        #壓縮檔案
        file_name = files.filename
        UPLOAD_CLIENT_FOLDER = UPLOAD_FOLDER + clientId 

        create_new_folder(UPLOAD_CLIENT_FOLDER)
        saved_path = os.path.join(UPLOAD_CLIENT_FOLDER, file_name)			
        files.save(saved_path)

        #RSA加密資料儲存
        hashfile_name = hashfiles.filename
        create_new_folder(ENCRYPTED_FOLDER)
        hash_file_saved_path = os.path.join(ENCRYPTED_FOLDER, hashfile_name)			
        hashfiles.save(hash_file_saved_path)

        # 讀取 RSA 私鑰
        privateKey = RSA.import_key(open(KEYFILE_FOLDER+"private.pem").read())

        # 從檔案讀取加密資料
        with open(hash_file_saved_path, "rb") as f:
            encSessionKey = f.read(privateKey.size_in_bytes())
            nonce = f.read(16)
            tag = f.read(16)
            ciphertext = f.read(-1)

        # 以 RSA 金鑰解密 Session 金鑰
        cipherRSA = PKCS1_OAEP.new(privateKey)
        sessionKey = cipherRSA.decrypt(encSessionKey)

        # 以 AES Session 金鑰解密資料
        cipherAES = AES.new(sessionKey, AES.MODE_EAX, nonce)
        data = cipherAES.decrypt_and_verify(ciphertext, tag)

        # 輸出解密後的資料
        hash_code = data.decode("utf-8")

        # 將上傳的壓縮檔案利用解密後的明文解壓縮
        file_list = zip_list(saved_path,data, UPLOAD_CLIENT_FOLDER)

        clientModels = ClientModel.get_clientModel_by_client_id(clientId)

        if clientModels is not None :
            for item in clientModels:
                ClientModel.delete_role(item)

        #寫入資料庫(新增)
        for fileName in file_list:
            #建構clientModel 物件
            clientModel = ClientModel(
                    clientId= clientId,
                    clientIp = clientIp, 
                    filePath = UPLOAD_CLIENT_FOLDER, 
                    fileName =  fileName , 
                    clientPort = clientPort,
                    createTime = datetime.now()
                    )
            ClientModel.insert_clientModel(clientModel)            


        status = 200
        message = "上傳成功"
        data = {
            'File' : file_name,
            'HashCode' : hash_code,
            'ClientId' : clientId ,
            'Upload_Client_Path' : UPLOAD_CLIENT_FOLDER,
            "File_List" : file_list
        }

        return jsonify({
            "Status": status,
            "Message": message,
            "Data" : data
        })






    



