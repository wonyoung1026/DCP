from . import *
from enum import Enum


COLLECTION_NAME = "Container"

class ContainerStatus(Enum):
    Running = 0
    Pending = 1
    Unstable = 2
    Disconnected = 3
    Stopped = 4

class Container(BaseModel):
    database = createFirestoreClient()
    collection = database.collection(COLLECTION_NAME)

    def __init__(self,**kwargs):
        buyerID = str()
        virtualMachineID = str()
        name = str()
        imageID = str()
        status = int()
        costRate= int()


        self.update(kwargs)

    def statusAsString(self):
        if self.status is not None:
            # TODO: add error handling when status input is out of range
            try:
                return str(ContainerStatus(self.status)).split(".")[1]
            except:
                return "Unknown status"

