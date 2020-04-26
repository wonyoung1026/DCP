from . import *
from enum import Enum
COLLECTION_NAME = "GPU"


class GPUStatus(Enum):
    Vacant = 0
    Occupied = 1


class GPU(BaseModel):
    database = createFirestoreClient()
    collection = database.collection(COLLECTION_NAME)

    def __init__(self,**kwargs):
        virtualMachineID = str()
        containerID = str()
        price = int()

        name = str()
        uuid = str()
        processor = str()
        expireTime = None
        self.update(kwargs)


    def statusAsString(self):
        if self.status is not None:
            # TODO: add error handling when status input is out of range
            try:
                return str(GPUStatus(self.status)).split(".")[1]
            except:
                return "Unknown status"