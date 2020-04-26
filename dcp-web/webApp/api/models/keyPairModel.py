from . import *

COLLECTION_NAME = "KeyPair"


class KeyPair(BaseModel):
    database = createFirestoreClient()
    collection = database.collection(COLLECTION_NAME)

    def __init__(self,**kwargs):
        name = str()
        buyerID = str()
        fingerprint = str()
        keyFileUrl = str()
        
        self.update(kwargs)