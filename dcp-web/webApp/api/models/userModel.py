from . import *

COLLECTION_NAME = "User"


class User(BaseModel):
    database = createFirestoreClient()
    collection = database.collection(COLLECTION_NAME)
    def __init__(self,**kwargs):
        email = str()
        isBuyer = bool()
        isProvider = bool()
        credit = int()

        self.update(kwargs)
    

    
    # 나중에 data manipulation 할때 유용
    # e.g. name 불러올때 name[0] 해서 initial 가져 올 수 있음
    # @property
    # def checkIfProvider(self):
    #     res = json.dumps(self.isProvider)
    #     return res