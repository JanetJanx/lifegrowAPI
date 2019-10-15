import json

class User:
    def __init__(self, entryId, landowner, name_owner, farm_location, landsize, soiltests):
        self.entryId = entryId
        self.landowner = landowner
        self.name_owner = name_owner
        self.farm_location = farm_location
        self.landsize = landsize
        self.soiltests = soiltests
    def json(self):
        return json.dumps({
            'entryId': self.entryId,
            'land owner': self.landowner, 
            'name owner': self.name_owner, 
            'farm location': self.farm_location,
            'land size': self.landsize, 
            'soil tests': self.soiltests,
        })


class LandEntry:

    def __init__(self, entryId, landowner, name_owner, farm_location, landsize, soiltests):
        self.entryId = entryId
        self.landowner = landowner
        self.name_owner = name_owner
        self.farm_location = farm_location
        self.landsize = landsize
        self.soiltests = soiltests