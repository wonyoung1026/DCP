from . import *

COLLECTION_NAME = "GPUMetric"


class GPUMetric(BaseModel):
    database = createFirestoreClient()
    collection = database.collection(COLLECTION_NAME)

    def __init__(self,**kwargs):
        gpuUtil = int()
        memoryUtil = int()
        gpuUUID = str()
        
        
        self.update(kwargs)
