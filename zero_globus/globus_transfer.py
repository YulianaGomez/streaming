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
#------------------------------- GLOBUS TOKEN ------------------------------------#
#=================================================================================#
CLIENT_ID = '59a91e4c-6717-4301-8d93-f02ff19ffdf0'

client = globus_sdk.NativeAppAuthClient(CLIENT_ID)
client.oauth2_start_flow(refresh_tokens=True)

authorize_url = client.oauth2_get_authorize_url()
print('Please go to this URL and login: {0}'.format(authorize_url))

# this is to work on Python2 and Python3 -- you can just use raw_input() or
# input() for your specific version
get_input = getattr(__builtins__, 'raw_input', input)
auth_code = get_input(
    'Please enter the code you get after login here: ').strip()
print("Past auth_code input")
token_response = client.oauth2_exchange_code_for_tokens(auth_code)
print("received token response")
globus_auth_data = token_response.by_resource_server['auth.globus.org']
print("past auth data")
globus_transfer_data = token_response.by_resource_server['transfer.api.globus.org']
print("past transfer data")
# the refresh token and access token, often abbr. as RT and AT
transfer_rt = globus_transfer_data['refresh_token']
print("past transfer rt: ", transfer_rt)
transfer_at = globus_transfer_data['access_token']
expires_at_s = globus_transfer_data['expires_at_seconds']
print("past expires")
# Now we've got the data we need, but what do we do?
# That "GlobusAuthorizer" from before is about to come to the rescue

authorizer = globus_sdk.RefreshTokenAuthorizer(
    transfer_rt, client, access_token=transfer_at, expires_at=expires_at_s)
print("past autorizer")
# and try using `tc` to make TransferClient calls. Everything should just
# work -- for days and days, months and months, even years
tc = globus_sdk.TransferClient(authorizer=authorizer)
# most specifically, you want these tokens as strings
#AUTH_TOKEN = globus_auth_data['access_token']
#TRANSFER_TOKEN = globus_transfer_data['access_token']
print("past tc: ", tc)

#=================================================================================#
#------------------------------- GLOBUS TOKEN ------------------------------------#
#=================================================================================#

#=================================================================================#
#-------------------------------    transfer    ----------------------------------#
#=================================================================================#
def service():
    print 'you are in globus_transfer script'

def transfer(files):
    print("Globus transfer will begin")
    #token_authorizer = AccessTokenAuthorizer(access_token = 'AQBZXNu8AAAAAAAFF9V3ePa7fHNGjBlfFpY7FJcrg2JqZa_R-iowMQII6HVsvm5DTKlorRY4Wyk9rN1tzI0K')
    #tc = globus_sdk.TransferClient(token_authorizer)
    #UUID can be found at your endpoint at globus or through tokens.globus.org
    #endpoints need to be established before transfer data
    #task list
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

#if __name__ == "__main__":

   # while True:
        #my_file = Path("/home/parallels/globus-sdk-python/globusnram/test_files/")
        #if my_file.is_file():
        #    transfer()
        #files = glob.glob('/home/parallels/stream_transfer/test_files/*')
        files = glob.glob('/home/parallels/stream_transfer/zero_globus/test_files/*')
        if len(files) > 0: transfer(files)
