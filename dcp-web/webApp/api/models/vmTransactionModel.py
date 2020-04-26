from . import *

COLLECTION_NAME = "VMTransaction"


class VMTransaction(BaseModel):
    database = createFirestoreClient()
    collection = database.collection(COLLECTION_NAME)

    def __init__(self,**kwargs):
        virtualMachineID = str()
        buyerID = str()
        providerID = str()
        containerID = str()
        totalPrice = int()
        paid = bool()
        pricePerHour= int()

        startTime = None
        endTime = None
        self.update(kwargs)