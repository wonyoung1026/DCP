from . import *

COLLECTION_NAME = "UserImage"


class UserImage(BaseModel):
    database = createFirestoreClient()
    collection = database.collection(COLLECTION_NAME)

    def __init__(self,**kwargs):
        name = str()
        description = str()

        self.update(kwargs)
