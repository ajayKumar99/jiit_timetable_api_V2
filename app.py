from flask import Flask , request , jsonify
from flask_restful import Resource , Api

app = Flask(__name__)
api = Api(app)

class TimetableApi(Resource):
    def post(self):
        req = request.get_json()
        return {'result' : [req , req]} , 201

api.add_resource(TimetableApi , '/')

if __name__ == '__main__':
  app.run(host='192.168.1.201' , port= '88')