import os 
from firebase_admin import firestore
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

    def save(self):
        if not self.id:
            #Provided without id => save a new doc
            self.createdOn = datetime.datetime.now(TZ_OFFSET)
            self.updatedOn = datetime.datetime.now(TZ_OFFSET)

            tup = self.collection.add(self)

            #returns id of created object
            return tup[1].id
        
        else:
            #Provided with id => update an existing doc
            self.updatedOn = datetime.datetime.now(TZ_OFFSET)

            self.collection.document(self.id).set(dict(self), merge=True)
            return self.id 