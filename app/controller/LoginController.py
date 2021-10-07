from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, jwt_required ,get_jwt_identity
# from app.model.User import User
# from app.model.Role import Role
import werkzeug
from app import jwt
import os


@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({
        'code': 201,
        'message': "token expired"
    })

PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = '{}/uploads/'.format(PROJECT_HOME)

def create_new_folder(local_dir):
	newpath = local_dir
	if not os.path.exists(newpath):
		os.makedirs(newpath)
	return newpath

class uploadMalware(Resource):
    def __init__(self, **kwargs):
            self.logger = kwargs.get('logger')
        
    def post(self):
        status = None 
        message = None
        data = None 
        args = reqparse.RequestParser()\
            .add_argument('file', type=werkzeug.datastructures.FileStorage,location='files')\
            .add_argument('password', type = str )\
            .parse_args()

        print(args)
        files = args.get("file")
        password = args['password']


        file_name = files.filename
        create_new_folder(UPLOAD_FOLDER)
        saved_path = os.path.join(UPLOAD_FOLDER, file_name)			
        files.save(saved_path)

        status = 200
        message = "上傳成功"
        data = {
            'file' : file_name,
            'password' : password
        }

        return jsonify({
            "Status": status,
            "Message": message,
            "Data" : data
        })






    



# class Login(Resource):
#     def __init__(self, **kwargs):
#         self.logger = kwargs.get('logger')

#     def post(self):
#         status = None
#         message = None
#         token = None
#         userId = None
#         roleId = None
#         roleName = None
#         data = None

#         args = reqparse.RequestParser() \
#             .add_argument('account', type=str, location='json', required=True, help="用戶名不能為空") \
#             .add_argument("password", type=str, location='json', required=True, help="密碼不能為空") \
#             .parse_args()

#         flag_user_exist, flag_password_correct, user = User.authenticate(args['account'], args['password'])
#         if not flag_user_exist:
#             status = 201
#             message = "user not exist"
#         elif not flag_password_correct:
#             status = 202
#             message = "wrong password"
#         else:
#             status = 200
#             message = "success"
#             token = create_access_token(identity=user.id)
#             id = user.id
#             roleId =  user.id_role
#             roleName = user.role.name

#             data = {
#                 "Token": token,
#                 "Id": id,
#                 "RoleId" : roleId , 
#                 "RoleName" : roleName
#             }

#         return jsonify({
#             "Status": status,
#             "Message": message,
#             "Data" : data
#         })

