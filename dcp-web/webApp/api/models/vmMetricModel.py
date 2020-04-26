from . import *

COLLECTION_NAME = "vmMetric"


class VMMetric(BaseModel):
    database = createFirestoreClient()
    collection = database.collection(COLLECTION_NAME)

    def __init__(self,**kwargs):
        cpuUtil = int()
        memoryUtil = int()
        numOfContainers = int()
        network = int()
        virtualMachineID = str()
        
        self.update(kwargs)
