import json
from datetime import datetime
import os.path
import sys
import pymysql

from myapp import mysql, app
from flask import Flask, jsonify, request, make_response
#from flask_restful import Resource, Api
from flask_restplus import Api, Resource, fields
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from .landmodel import LandEntry
# app = Flask(__name__)
#app.config["DEBUG"] = True
api = Api(app, version = "1.0", title = "LifeGrow API", description = "manages db entries for the lifegrow application")

name_space = api.namespace('main', description='Main APIs')

#model = api.models('Land Entry', {'Land entry': fields.String(required = True, description="Entry of the Land", help="Entry cannot be blank.")})

def get_timestamp():
    return datetime.now().strftime(("%Y-%m-%d %H:%M:%S"))

count = 0
def increment_landentryId():
    global count
    count = count + 1
    return count

class CounterfeitEntryError(Exception):
    pass

class GetAllLandEntries(Resource):
    # land_entries = []
    @classmethod
    def get(self):
        try:
            cursor = mysql.cursor()
            cursor.execute("SELECT landowner, name_owner, farm_location, landsize, soiltests FROM farmland")
            rows = cursor.fetchall()
            return make_response(jsonify(
                {'entries': rows },
                {"message": "Land Entries successfully fetched"}), 200)
        except (ValueError, KeyError, TypeError):
            return make_response(jsonify(
                {'message': "JSON Format Error"+str(KeyError)}))

            
class AddNewLandEntry(Resource):
    @classmethod
    def post(self):
        try:
            landowner = request.args.get('landowner')
            name_owner = request.args.get('nameowner')
            farm_location = request.args.get('farmlocation')
            landsize = request.args.get('landsize')
            soiltests = request.args.get('soiltests')

            sql = "INSERT INTO farmland(landowner, name_owner, farm_location, landsize, soiltests) VALUES(%s, %s, %s, %s, %s)"
            data = (landowner, name_owner, farm_location, landsize, soiltests)
            cursor = mysql.cursor()
            cursor.execute(sql, data)
            mysql.commit()
            return make_response(jsonify({'message': "Land Entry successfully added"}), 200)
        except (ValueError, KeyError, TypeError):
            return make_response(jsonify(
                {'message': "JSON Format Error" +str(KeyError) +str(TypeError) +str(ValueError)}))


class ViewSpecificLandEntry(Resource):
    """get specific entry"""
    @classmethod
    def get(self, entryid):
        try:
            cursor = mysql.cursor()
            cursor.execute("SELECT landowner, name_owner, farm_location, landsize, soiltests FROM farmland WHERE farmland_id=%s", entryid)
            row = cursor.fetchone()
            return make_response(jsonify(
                {'entry': row},
                {"message": "Land Entry successfully fetched"}), 200)

        except (ValueError, KeyError, TypeError):
            return make_response(jsonify(
                {'message': "JSON Format Error"}))

class DeleteSpecificLandEntry(Resource):
    """delete a specify entry"""
    @classmethod
    def delete(self, entryid):

        try:
            cursor = mysql.cursor()
            cursor.execute("DELETE FROM farmland WHERE farmland_id=%s", entryid)
            row = cursor.fetchone()
            #return resp
            return make_response(jsonify(
                {'entry': row},
                {"message": "Land Entry successfully removed"}), 200)

        except (ValueError, KeyError, TypeError):
            return make_response(jsonify(
                {'message': "JSON Format Error"}))

class ModifySpecificLandEntry(Resource):
    """modify a specific entry"""
    @classmethod
    def put(self, entryid):
        try:
            landowner = request.args.get('landowner')
            name_owner = request.args.get('nameowner')
            farm_location = request.args.get('farmlocation')
            landsize = request.args.get('landsize')
            soiltests = request.args.get('soiltests')

            sql = "UPDATE farmland SET landowner=%s, name_owner=%s, farm_location=%s, landsize=%s, soiltests=%s WHERE farmland_id=%s"
            data = (landowner, name_owner, farm_location, landsize, soiltests, entryid)
            cursor = mysql.cursor()
            cursor.execute(sql, data)
            mysql.commit()
            return make_response(jsonify(
                {'entry': data},
                {'message': "Land Entry successfully updated"}), 201)

        except (ValueError, KeyError, TypeError):
            return make_response(jsonify(
                {'message': "JSON Format Error"}), 401)


api.add_resource(GetAllLandEntries, '/api/v1/getlandentries', methods=['GET'])
api.add_resource(AddNewLandEntry, '/api/v1/addlandentries', methods=['POST'])
api.add_resource(ViewSpecificLandEntry, '/api/v1/viewlandentries/<int:entryid>', methods=['GET'])
api.add_resource(DeleteSpecificLandEntry, '/api/v1/dellandentries/<int:entryid>', methods=['DELETE'])
api.add_resource(ModifySpecificLandEntry, '/api/v1/modlandentries/<int:entryid>', methods=['PUT'])

if __name__ == "__main__":
    app.run(port= 5000)