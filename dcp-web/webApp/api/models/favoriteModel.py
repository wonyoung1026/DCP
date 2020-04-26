from . import *

COLLECTION_NAME = "Favorite"


class Favorite(BaseModel):
    database = createFirestoreClient()
    collection = database.collection(COLLECTION_NAME)

    def __init__(self,**kwargs):
        userID = str()
        virtualMachineID = str()
        
        self.update(kwargs)