from globus_sdk import (TransferClient, TransferAPIError, TransferData, DeleteData, AccessTokenAuthorizer)
import glob, os
import shutil
import globus_sdk
import time
import os.path
#os.path.isfile(fname) 
from pathlib import Path
from os import makedirs


#from find_uuid import find_uuid
# ddb59aef-6d04-11e5-ba46-22000b92c6ec
# 2b5e59d2-409e-11e7-bd30-22000b9a448b

#=================================================================================#
#-------------------------------    transfer    ----------------------------------#
#=================================================================================#

def transfer():

    token_authorizer = AccessTokenAuthorizer(access_token = 'AQBZKFOiAAAAAAAFF9UrJWHsmrT0ZxNuzwDzSGiAlJ1q4g-djunpQ2iDx9z-lvNbePOJWK9fuVKSRBSNQYoo')
    tc = globus_sdk.TransferClient(token_authorizer)
    #UUID can be found at your endpoint at globus or through tokens.globus.org
    #endpoints need to be established before transfer data
    
    #UUID -this is my endpoint UUID
    source_endpoint_id = '2b5e59d2-409e-11e7-bd30-22000b9a448b'
    # source_endpoint_id = raw_input('Input source endpoint UUID: ')
    #destination path

    source_path = '/home/parallels/globus-sdk-python/globusnram/test_files/'
    #destination path
    destination_path = '/~/'
    #Using my sample UUID from globus tutorial
    destination_endpoint_id = 'ddb59aef-6d04-11e5-ba46-22000b92c6ec'



    #tc.endpoint_autoactivate(source_endpoint_id)
    #tc.endpoint_autoactive(destination_endpoint_id)
    ep1 = tc.get_endpoint(destination_endpoint_id)
    tc.endpoint_autoactivate(destination_endpoint_id)
    #ep1 is setting the activated endpoint to be a variable to work with
    tc.endpoint_autoactivate(source_endpoint_id)

    label = "medium data transfer"
    tdata = globus_sdk.TransferData(tc, source_endpoint_id, destination_endpoint_id,label=label, sync_level='checksum')
    tdata.add_item(source_path,destination_path,recursive=True)

    submit_result = tc.submit_transfer(tdata)
    #print("Task ID:", submit_result["task_id"])

    #setup of the transfer, submits as a https post request
    #transfer_data = TransferData(transfer_client=tc,
    #                     source_endpoint=source_endpoint_id,
    #                     destination_endpoint=destination_endpoint_id,
    #                     label='Transfer',
    #                     sync_level='checksum')
    #transfer_data.add_item(source_path=source_path,destination_path=destination_path, recursive=False)
    #task_id=transfer.submit_transfer(transfer_data)['task_id']
     
    #waiting for file to transfer
    status = tc.get_task(submit_result["task_id"],fields="status")["status"]
    poll_interval = 15
    max_wait = 90
    wait_time = 0
    while not (status in ["SUCCEEDED", "FAILED"]):
        if (wait_time >= max_wait): break
        print("Task not yet complete (status {}), sleeping for {} seconds..." \
            .format(status, poll_interval))
        time.sleep(poll_interval)
        wait_time += poll_interval
        status = tc.get_task(submit_result["task_id"], fields="status")["status"]
    
    if status == "FAILED":
        print("WARNING! File transfer FAILED!")
    
    #deleting file after transfer
    if status == "SUCCEEDED":
        print("File transfer SUCCEEDED, will delete file from local directory now")
        files = glob.glob('/home/parallels/globus-sdk-python/globusnram/test_files/*')
        for f in files:
            os.remove(f)
        
        print("Files have been transferred and deleted")


#=================================================================================#
#-------------------------------      MAIN      ----------------------------------#
#=================================================================================#

if __name__ == "__main__":

    while True:
        #my_file = Path("/home/parallels/globus-sdk-python/globusnram/test_files/")
        #if my_file.is_file():
        #    transfer()
        files = glob.glob('/home/parallels/globus-sdk-python/globusnram/test_files/*')
        if len(files) > 0: transfer()






