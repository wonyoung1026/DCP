from . import *
from enum import Enum

COLLECTION_NAME = "VirtualMachine"

class VirtualMachineStatus(Enum):
    Running = 0
    Pending = 1
    Unstable = 2
    Disconnected = 3


class VirtualMachine(BaseModel):
    database = createFirestoreClient()
    collection = database.collection(COLLECTION_NAME)

    def __init__(self,**kwargs):
        price = int()
        name = str()
        providerEmail = str()
        providerID = str()
        status = int()
        numberOfDisconnections = int()

        processor = list()
        memory = list()
        disk = list()
        gpuIDs = list()
        ipAddress = str()
        isHidden = bool()
        expireTime = None

        self.update(kwargs)


    def statusAsString(self):
        if self.status is not None:
            # TODO: add error handling when status input is out of range
            try:
                return str(VirtualMachineStatus(self.status)).split(".")[1]
            except:
                return "Unknown status"
    # 나중에 data manipulation 할때 유용
    # e.g. name 불러올때 name[0] 해서 initial 가져 올 수 있음
    # @property
    # def checkIfProvider(self):
    #     res = json.dumps(self.isProvider)
    #     return res