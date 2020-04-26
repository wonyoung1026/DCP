# ========================================================================
# Storage related helpers
# ========================================================================
from google.cloud import storage

def storageUploadBlob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # bucket_name = "your-bucket-name"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )


# ========================================================================
# Get past N months dictionary 
# > type => "m" :month, "d":day 
# ========================================================================
def getPastNDict(type, n):
    current_year = getCurrentTime().year
    current_month = getCurrentTime().month
    
    past_n_dict = {}
    
    if type == "m":
        for month in range(current_month - n +1, current_month+1):
            if month > 0:
                key = yearMonthKeyFormat(current_year, month)
            elif month == 0:
                key = yearMonthKeyFormat(current_year-1, 12)
            else:
                key = yearMonthKeyFormat(current_year-1, month%12)
            past_n_dict[key] = 0
    elif type == "d":
        # TODO
        pass

    return past_n_dict

# YYYY - MM
def yearMonthKeyFormat(year, month):
    return str(year) + "-" + str(month)



# ========================================================================
# Time related helpers
# ========================================================================
# hourly_price => int
# returns int
def hourlyPriceToSecondlyPrice(hourly_price):
    return hourly_price/3600

# start_time, end_time => datetime
# returns int
def getTimeDifferenceInSeconds(start_time, end_time):
    return int((end_time-start_time).total_seconds())

import datetime
from ..models import TZ_OFFSET
# returns datetime
def getCurrentTime():
    return datetime.datetime.now(TZ_OFFSET)