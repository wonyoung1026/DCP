from . import *

COLLECTION_NAME = "vmMetric"


class VmMetric(BaseModel):
    database = createFirestoreClient()
    collection = database.collection(COLLECTION_NAME)

    def __init__(self, **kwargs):
        cpuUtil = int()
        memoryUtil = int()
        network = int()
        numOfContainers = int()

        self.update(kwargs)
