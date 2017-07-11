#!/usr/bin/env python

from globus_sdk import (TransferClient, TransferAPIError, TransferData, DeleteData, AccessTokenAuthorizer)
import glob, os
import shutil
import globus_sdk
import time
import os.path
import re
import datetime
#os.path.isfile(fname)
from pathlib import Path
from os import makedirs


#from find_uuid import find_uuid
# ddb59aef-6d04-11e5-ba46-22000b92c6ec
# 2b5e59d2-409e-11e7-bd30-22000b9a448b

#=================================================================================#
#-------------------------------    transfer    ----------------------------------#
#=================================================================================#
def service():
    print 'you are in globus_transfer script'
def transfer(files):
    print("Globus transfer will begin")

    CLIENT_ID = '59a91e4c-6717-4301-8d93-f02ff19ffdf0'

    client = globus_sdk.NativeAppAuthClient(CLIENT_ID)

    # create a client object that tracks state as we do this flow
    native_auth_client = globus_sdk.NativeAppAuthClient(CLIENT_ID)
    # explicitly start the flow (some clients may support multiple flows)
    native_auth_client.oauth2_start_flow()

    ############################################################################
    #-----------------------------NEW NATIVE CLIENT----------------------------#
    ############################################################################
    # fill this line in with the code that you got
    auth_code = "mFdyQVVvnmMn51PWRWQeu9OfNSRixp"

    # and exchange it for a response object containing your token(s)
    token_response = native_auth_client.oauth2_exchange_code_for_tokens(auth_code)

    # extract the Access Token for Globus Transfer, known as "transfer.api.globus.org"
    transfer_access_token = token_response.by_resource_server['transfer.api.globus.org']['access_token']

    # wrap the token in an object that implements the globus_sdk.GlobusAuthorizer interface
    # in this case, an AccessTokenAuthorizer, which takes an access token and produces Bearer Auth headers
    transfer_authorizer = globus_sdk.AccessTokenAuthorizer(transfer_access_token)

    # create a TransferClient object which Authorizes its calls using that GlobusAuthorizer
    tc = globus_sdk.TransferClient(authorizer=transfer_authorizer)
    ############################################################################
    #-------------------------NEW NATIVE CLIENT(end)---------------------------#
    ############################################################################

    #UUID -this is my endpoint UUID
    source_endpoint_id = '2b5e59d2-409e-11e7-bd30-22000b9a448b'#ubuntu-vm
    # source_endpoint_id = raw_input('Input source endpoint UUID: ')
    #destination path
    #source_path = '/home/parallels/stream_transfer/test_files/'
    source_path = '/home/parallels/stream_transfer/zero_globus/test_files/'
    #destination path
    destination_path = '/~/'
    #Using my sample UUID from globus tutorial
    destination_endpoint_id = 'ddb59aef-6d04-11e5-ba46-22000b92c6ec' #globus
    #destination_endpoint_id = '5d1da0fe-3c07-11e7-bcfc-22000b9a448b' #laptop

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
    print("Task ID:", submit_result["task_id"])
    #print("Completion time:", submit_result["completion_time"])

    #waiting for file to transfer
    status = tc.get_task(submit_result["task_id"],fields="status")["status"]
    poll_interval = 2
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
        end_time = datetime.datetime.utcnow()
        start_time = end_time - datetime.timedelta(minutes=200)

        #limit = response objects
#        data = tc.task_list(filter="type:TRANSFER,DELETE/request_time:%s,%s"
#        % (start_time, end_time), limit=5)

        print("File transfer SUCCEEDED, will delete file from local directory now")
        r = tc.task_list(num_results=1, filter="type:TRANSFER,DELETE")
        all_data = []
        for d in r.data:
            new_event = {}
            new_event['completion_time'] = d['completion_time']
            new_event['request_time'] = d['request_time']
            new_event['task_id'] = d['task_id']
            all_data.append(new_event)

            p = re.compile(r'\W+')
            ct = p.split(new_event['completion_time'])
            rt = p.split(new_event['request_time'])
            hr = int(ct[3])-int(rt[3])
            mn = int(ct[4])-int(rt[4])
            sec = int(ct[5])-int(rt[5])
            print ("Duration of time:%i:%i:%i"% (hr,mn,sec))

        """rt = int(item['request_time'])
        ct = int(item['completion_time'])
        duration = ct - rt"""
        #print('Duration time:',duration)
        #print(item['effective_bytes_per_second'])
        #files = glob.glob('/home/parallels/stream_transfer/test_files/*')
        #files = glob.glob('/home/parallels/stream_transfer/zero_globus/test_files/*')
        for f in files:
            os.remove(f)


        #print("Files have been transferred and deleted")
#/home/parallels/stream_transfer/test_files

#=================================================================================#
#-------------------------------      MAIN      ----------------------------------#
#=================================================================================#

if __name__ == "__main__":

    while True:
        #my_file = Path("/home/parallels/globus-sdk-python/globusnram/test_files/")
        #if my_file.is_file():
        #    transfer()
        #files = glob.glob('/home/parallels/stream_transfer/test_files/*')
        files = glob.glob('/home/parallels/stream_transfer/zero_globus/test_files/*')
        if len(files) > 0: transfer(files)
