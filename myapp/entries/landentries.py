import json
from datetime import datetime
import os.path
import sys
import pymysql

from myapp import mysql
from flask import Flask, jsonify, request, make_response
#from flask_restful import Resource, Api
from flask_restplus import Api, Resource, fields
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from .landmodel import LandEntry
app = Flask(__name__)
app.config["DEBUG"] = True
api = Api(app, version = "1.0", title = "Land Entries", description = "manages land entries for the lifegrow application")

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
            
            db = mysql.connection("ctiafrica.io","root","Silversands123!","cti_lifegrow" )
            cursor = db.cursor()
            cursor.execute("SELECT * FROM `farm_land`")
            rows = cursor.fetchall()
            resp = jsonify(rows)
            print(resp)
            resp.status_code = 200
            mysql.connection.commit()
            cursor.close()
            return make_response(jsonify({"message": "Land Entries successfully fetched"}), 200)
        except (ValueError, KeyError, TypeError):
            return make_response(jsonify(
                {'message': "JSON Format Error"+str(KeyError)+str(TypeError)}), 401)

            
class AddNewLandEntry(Resource):
    @classmethod
    def post(self):
        try:
            landdata = request.json()
            landowner = landdata.get('landowner')
            name_owner = landdata.get('name_owner')
            farm_location = landdata.get('farm_location')
            landsize = landdata.get('landsize')
            soiltests = landdata.get('soiltests')

            sql = "INSERT INTO farm_land(farmland_id, land_owner, name_owner, farm_location, landsize, soiltests) VALUES(%s, %s, %s, %s, %s, %s)"
            data = (increment_landentryId(), landowner, name_owner, farm_location, landsize, soiltests)
            conn = mysql.connection.cursor()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            cursor.close()
            conn.close()
            
            return make_response(jsonify({'message': "Land Entry successfully added"}), 200)

        except Exception as e:
            return make_response(
                jsonify(
                    {"message": e}), 
                    500)


class ViewSpecificLandEntry(Resource):
    """get specific entry"""
    @classmethod
    def get(self, entryid):
        try:
            conn = mysql.connection.cursor()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("SELECT * FROM farm_land WHERE farmland_id=%s", entryid)
            row = cursor.fetchone()
            resp = jsonify(row)
            resp.status_code = 200
            #return resp
            cursor.close()
            conn.close()
            return make_response(jsonify(
                {'entry': resp},
                {"message": "Land Entry successfully fetched"}), 200)

        except Exception as e:
            return make_response(jsonify({"message": e}), 500)

class DeleteSpecificLandEntry(Resource):
    """delete a specify entry"""
    @classmethod
    def delete(self, entryid):

        try:
            conn = mysql.connection.cursor()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("DELETE * FROM farm_land WHERE farmland_id=%s", entryid)
            row = cursor.fetchall()
            resp = jsonify(row)
            resp.status_code = 200
            cursor.close()
            conn.close()
            #return resp
            return make_response(jsonify(
                {'entry': resp},
                {"message": "Land Entry successfully removed"}), 200)

        except Exception as e:
            return make_response(jsonify({"message": e}), 500)

class ModifySpecificLandEntry(Resource):
    """modify a specific entry"""
    @classmethod
    def put(self, entryid):
        try:
            landdata = request.get_json()
            farmland_id = landdata.get('entryId')
            landowner = landdata.get('land owner')
            name_owner = landdata.get('name owner')
            farm_location = landdata.get('farm location')
            landsize = landdata.get('land size')
            soiltests = landdata.get('soil tests')

            sql = "UPDATE farm_land SET land_owner=%s, name_owner=%s, farm_location=%s, landsize=%s, soiltests=%s WHERE farmland_id=%s"
            data = (landowner, name_owner, farm_location, landsize, soiltests, farmland_id)
            conn = mysql.connection.cursor()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            cursor.close()
            conn.close()
            resp = jsonify('Land detail updated successfully!')
            resp.status_code = 200

            return make_response(jsonify(
                {'entry': resp},
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