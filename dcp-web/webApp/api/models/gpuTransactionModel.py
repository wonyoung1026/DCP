from . import *

COLLECTION_NAME = "GPUTransaction"


class GPUTransaction(BaseModel):
    database = createFirestoreClient()
    collection = database.collection(COLLECTION_NAME)

    def __init__(self,**kwargs):
        gpuID = str()
        buyerID = str()
        providerID = str()
        containerID = str()
        totalPrice = int()
        paid = bool()
        pricePerHour= int()

        startTime = None
        endTime = None
        self.update(kwargs)