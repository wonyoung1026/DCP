import os
from firebase_admin import firestore
import json
import datetime

global TZ_OFFSET
TZ_OFFSET = datetime.timezone.utc

global datetimeFormat
def datetimeFormat(dt):
    return dt.strftime("%m/%d/%Y, %H:%M:%S %Z")

def createFirestoreClient():
    return firestore.client()


class BaseModel(dict):
    __getattr__ = dict.get
    __delattr__ = dict.__delitem__
    __setattr__ = dict.__setitem__
    
    def toJson(self):
        # This line required because Datetime cannot be serialized into json 
        self.update({k: datetimeFormat(v) if isinstance(v,datetime.datetime) else v for k,v in self.items()})
        return json.loads(json.dumps((self)))

    def save(self):
        if not self.id:
            # Provided without id => save a new doc
            self.createdOn = datetime.datetime.now(TZ_OFFSET)
            self.updatedOn = datetime.datetime.now(TZ_OFFSET)
            # self.createdOn = firestore.SERVER_TIMESTAMP
            # self.updatedOn = firestore.SERVER_TIMESTAMP
            tup = self.collection.add(self)
            # returns id of created object
            return tup[1].id
            
        else:
            # Provided with id => update an existing doc
            self.updatedOn = datetime.datetime.now(TZ_OFFSET)
            # self.updatedOn = firestore.SERVER_TIMESTAMP
            self.collection.document(self.id).set(dict(self), merge=True)
            return self.id
    
    def reload(self):
        if self.id:
            try:
                self.update(self.collection\
                    .document(self.id)\
                    .get()\
                    .to_dict())
            except:
                # if resource does not exist do nothing
                self.clear()
                pass
            
    def remove(self):
        if self.id:
            self.collection.document(self.id).delete()

    @classmethod
    def getByQuery(cls, triplets=None):
        query = cls.collection
        if triplets:
            for triplet in triplets:
                query = query.where(triplet[0],triplet[1],triplet[2])
        docs = query.stream()
        obj_list = []
        for doc in docs:
            obj = cls(id=doc.id)
            obj.update(doc.to_dict())
            obj_list.append(obj)
        return obj_list
    