from flask import Blueprint
from flask_restful import Api
from .entries import *

entry = Blueprint('Land_entries', __name__)
api = Api(entry)

#Land
api.add_resource(GetAllLandEntries, '/api/v1/getlandentries')
api.add_resource(AddNewLandEntry, '/api/v1/addlandentries')
api.add_resource(ViewSpecificLandEntry, '/api/v1/viewlandentries/<int:entryid>')
api.add_resource(DeleteSpecificLandEntry, '/api/v1/dellandentries/<int:entryid>')
api.add_resource(ModifySpecificLandEntry, '/api/v1/modlandentries/<int:entryid>')

#crop
api.add_resource(GetAllCropDetails, '/api/v1/getcrops', methods=['GET'])
api.add_resource(AddNewCropDetail, '/api/v1/addcrop', methods=['POST'])
api.add_resource(ViewSpecificCropDetail, '/api/v1/viewcrop/<int:entryid>', methods=['GET'])
api.add_resource(DeleteSpecificCropDetail, '/api/v1/delcrop/<int:entryid>', methods=['DELETE'])
api.add_resource(ModifySpecificCropDetail, '/api/v1/modcrop/<int:entryid>', methods=['PUT'])