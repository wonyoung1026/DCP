from . import *

COLLECTION_NAME = "BaseImage"


class BaseImage(BaseModel):
    database = createFirestoreClient()
    collection = database.collection(COLLECTION_NAME)

    def __init__(self,**kwargs):
        name = str()
        description = str()

        self.update(kwargs)
