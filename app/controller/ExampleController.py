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




class example(Resource):
    def __init__(self, **kwargs):
            self.logger = kwargs.get('logger')
        
    def post(self):
        status = None 
        message = None
        data = None 
        args = reqparse.RequestParser()\
            .add_argument('request01', type = str)\
            .add_argument('request02', type = str)\
            .parse_args()

        request01 = 'request' if args["request01"] is None else args["request01"]
        request02 = 'request' if args["request02"] is None else args["request02"]


        status = 200
        message = "hello word"
        data = {
            'request01' : request01,
            'request02' : request02,
        }

        return jsonify({
            "Status": status,
            "Message": message,
            "Data" : data
        })






    


