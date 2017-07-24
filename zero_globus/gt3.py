#!/usr/bin/env python

from globus_sdk import (TransferClient, TransferAPIError, TransferData, DeleteData, AccessTokenAuthorizer, NativeAppAuthClient)
import glob, os
import shutil
import globus_sdk
import time
import os.path
import re
import json
import datetime
#os.path.isfile(fname)
from pathlib import Path
from os import makedirs
import webbrowser
#import gl_refresh
get_input = getattr(__builtins__, 'raw_input', input)
TOKEN_FILE = 'refresh-tokens.json'
#from find_uuid import find_uuid
# ddb59aef-6d04-11e5-ba46-22000b92c6ec
# 2b5e59d2-409e-11e7-bd30-22000b9a448b

#=================================================================================#
#-------------------------------    transfer    ----------------------------------#
#=================================================================================#

def load_tokens_from_file(filepath):
    """Load a set of saved tokens."""
    with open(filepath, 'r') as f:
        tokens = json.load(f)

    return tokens


def save_tokens_to_file(filepath, tokens):
    """Save a set of tokens for later use."""
    with open(filepath, 'w') as f:
        json.dump(tokens, f)

def service():
    print 'you are in globus_transfer script'
"""def get_auth():
    CLIENT_ID = '59a91e4c-6717-4301-8d93-f02ff19ffdf0'
    client = globus_sdk.NativeAppAuthClient(CLIENT_ID)
    client.oauth2_start_flow(refresh_tokens=True)
    authorize_url = client.oauth2_get_authorize_url()
    print('Please go to this URL and login: {0}'
         .format(client.oauth2_get_authorize_url()))

    get_input = getattr(__builtins__, 'raw_input', input)
    auth_code = get_input('Please enter the code here: ').strip()
    return auth_code"""

def do_native_app_authentication(client_id, redirect_uri,
                                 requested_scopes=None):
    """
    Does a Native App authentication flow and returns a
    dict of tokens keyed by service name.
    """
    client = NativeAppAuthClient(client_id=client_id)
    # pass refresh_tokens=True to request refresh tokens
    client.oauth2_start_flow(requested_scopes=requested_scopes,
                             redirect_uri=redirect_uri,
                             refresh_tokens=True)

    url = client.oauth2_get_authorize_url()

    print('Native App Authorization URL: \n{}'.format(url))

    #if not is_remote_session():
    webbrowser.open(url, new=1)

    auth_code = get_input('Enter the auth code: ').strip()

    token_response = client.oauth2_exchange_code_for_tokens(auth_code)

    # return a set of tokens, organized by resource server name
    return token_response.by_resource_server

def transfer(files):
    TOKEN_FILE = 'refresh-tokens.json'
    REDIRECT_URI = 'https://auth.globus.org/v2/web/auth-code'
    SCOPES = ('openid email profile '
              'urn:globus:auth:scope:transfer.api.globus.org:all')
    print("Globus transfer will begin")
    #SCOPES = 'openid profile email urn:globus:auth:scope:transfer.api.globus.org:all urn:globus:auth:scope:auth.globus.org:view_identities'
    #token_authorizer = AccessTokenAuthorizer(access_token = 'AQBZXNu8AAAAAAAFF9V3ePa7fHNGjBlfFpY7FJcrg2JqZa_R-iowMQII6HVsvm5DTKlorRY4Wyk9rN1tzI0K')
    #CLIENT_ID = '59a91e4c-6717-4301-8d93-f02ff19ffdf0'
    #auth_client = globus_sdk.AuthClient(client_id=..., client_secret=...)
    # do some flow to get a refresh tauth_client = globus_sdk.AuthClient(client_id=..., client_secret=...)oken from auth_client
    #rt_authorizer = globus_sdk.RefreshTokenAuthorizer(
    #                refresh_token, auth_client)
    # create a new client
    #transfer_client = globus_sdk.TransferClient(authorizer=rt_authorizer)
    #############################################
    # create an authorized transfer client
    """client = globus_sdk.NativeAppAuthClient(client_id=CLIENT_ID)
    client.oauth2_start_flow(requested_scopes=SCOPES)
    url = client.oauth2_get_authorize_url()
    if os.path.getsize("/home/parallels/stream_transfer/zero_globus/refresh_token.txt") > 0:
        with open ("/home/parallels/stream_transfer/zero_globus/refresh_token.txt", "r") as myfile:
            auth_code = str(myfile.readlines())
    else:
        #print("Login with SDK Tester: \n{}".format(url))
        get_input = getattr(__builtins__, 'raw_input', input)
        auth_code = get_input("Enter auth code: ").strip()

    # get tokens and make a transfer client
    tokens = client.oauth2_exchange_code_for_tokens(
        auth_code).by_resource_server
    globus_transfer_data = tokens['transfer.api.globus.org']
    transfer_rt = globus_transfer_data['refresh_token']
    transfer_at = globus_transfer_data['access_token']
    expires_at_s = globus_transfer_data['expires_at_seconds']

    authorizer = globus_sdk.RefreshTokenAuthorizer(
        transfer_rt, client, access_token=transfer_at, expires_at=expires_at_s)
    tc = globus_sdk.TransferClient(authorizer=authorizer)"""
    #native_auth_client.oauth2_start_flow(refresh_tokens=True)

    #SCOPES = 'openid profile email urn:globus:auth:scope:transfer.api.globus.org:all urn:globus:auth:scope:auth.globus.org:view_identities'

   # import globus_sdk

    # this is the ID of the Jupyter Demo App
    CLIENT_ID = '59a91e4c-6717-4301-8d93-f02ff19ffdf0'
    #print("Login with SDK Tester: \n{}".format(url))
    #get_input = getattr(__builtins__, 'raw_input', input)
    #auth_code = get_input("Enter auth code: ").strip()

    # start Native App Grant, and print out the URL where users login as part of the flow (step 2 above)
    #SCOPES = 'offline_access openid profile email urn:globus:auth:scope:transfer.api.globus.org:all urn:globus:auth:scope:auth.globus.org:view_identities'

    # create a client object that tracks state as we do this flow
    """ native_auth_client = globus_sdk.NativeAppAuthClient(CLIENT_ID)

    # explicitly start the flow (some clients may support multiple flows)
    native_auth_client.oauth2_start_flow(refresh_tokens=True)
    print("Login Here:\n\n{0}".format(native_auth_client.oauth2_get_authorize_url()))
    get_input = getattr(__builtins__, 'raw_input', input)
    auth_code = get_input("Enter auth code: ").strip()
    # print URL

    ##print(("\n\nNote that this link can only be used once! "
           ##"If login or a later step in the flow fails, you must restart it."))


    # fill this line in with the code that you got
    #auth_code = "I6pwiFX77qtIf8zp3XbOR0klnbxNnk"

    # and exchange it for a response object containing your token(s)
    token_response = native_auth_client.oauth2_exchange_code_for_tokens(auth_code)
    print token_response"""



    """client = globus_sdk.NativeAppAuthClient(CLIENT_ID)
    #client.oauth2_start_flow(refresh_tokens=True)

    #authorize_url = client.oauth2_get_authorize_url()
    #print('Please go to this URL and login: {0}'
    #       .format(client.oauth2_get_authorize_url()))
    auth_code = 'WojMfO2T0fAEqUdpvcqDUiTfZIy0AD'
    #get_input = getattr(__builtins__, 'raw_input', input)
    #auth_code = get_input('Please enter the code here: ').strip()
    #token_response = client.oauth2_exchange_code_for_tokens(auth_code)
    # start Native App Grant, and print out the URL where users login as part of the flow (step 2 above)
    ############################################################################
    #-----------------------------NEW NATIVE CLIENT----------------------------#
    ############################################################################
    # create a client object that tracks state as we do this flow
    native_auth_client = globus_sdk.NativeAppAuthClient(CLIENT_ID)
    # explicitly start the flow (some clients may support multiple flows)
    native_auth_client.oauth2_start_flow()
    # and exchange it for a response object containing your token(s)
    token_response = native_auth_client.oauth2_exchange_code_for_tokens(auth_code)

    # extract the Access Token for Globus Transfer, known as "transfer.api.globus.org"
    transfer_access_token = token_response.by_resource_server['transfer.api.globus.org']['access_token']

    # wrap the token in an object that implements the globus_sdk.GlobusAuthorizer interface
    # in this case, an AccessTokenAuthorizer, which takes an access token and produces Bearer Auth headers
    transfer_authorizer = globus_sdk.AccessTokenAuthorizer(transfer_access_token)

    # create a TransferClient object which Authorizes its calls using that GlobusAuthorizer
    tc = globus_sdk.TransferClient(authorizer=transfer_authorizer)"""
    ############################################################################
    #-------------------------NEW NATIVE CLIENT(end)---------------------------#
    ############################################################################
    """globus_auth_data = token_response.by_resource_server['auth.globus.org']
    globus_transfer_data = token_response.by_resource_server['transfer.api.globus.org']
    # the refresh token and access token, often abbr. as RT and AT
    transfer_rt = globus_transfer_data['refresh_token']
    transfer_at = globus_transfer_data['access_token']"""
    ##expires_at_s = globus_transfer_data['expires_at_seconds']

    # Now we've got the data we need, but what do we do?
    # That "GlobusAuthorizer" from before is about to come to the rescue

    ##authorizer = globus_sdk.RefreshTokenAuthorizer(
        ##transfer_rt, client, access_token=transfer_at, expires_at=expires_at_s)

    # and try using `tc` to make TransferClient calls. Everything should just
    # work -- for days and days, months and months, even years
    ##tc = globus_sdk.TransferClient(authorizer=authorizer)
    # most specifically, you want these tokens as strings
    #AUTH_TOKEN = globus_auth_data['access_token']
    #TRANSFER_TOKEN = globus_transfer_data['access_token']
    #load from file  here for tokens...
###############################################################################
    #tokens = token_response.by_resource_server
    #tokens = load_tokens_from_file(TOKEN_FILE)

    tokens = None
    try:
        # if we already have tokens, load and use them
        tokens = load_tokens_from_file(TOKEN_FILE)
    except Exception as e:
        print ("I am here too")
        print (e)
        pass

    if not tokens:
        # if we need to get tokens, start the Native App authentication process
        tokens = do_native_app_authentication(CLIENT_ID, REDIRECT_URI, SCOPES)

        try:
            save_tokens_to_file(TOKEN_FILE, tokens)
        except Exception as e:
            print ("i am here")
            print (e)
            pass


    transfer_tokens = tokens['transfer.api.globus.org']
    auth_client = NativeAppAuthClient(client_id=CLIENT_ID)


    globus_transfer_data = tokens['transfer.api.globus.org']
    transfer_rt = globus_transfer_data['refresh_token']
    transfer_at = globus_transfer_data['access_token']
    expires_at_s = globus_transfer_data['expires_at_seconds']
    authorizer = globus_sdk.RefreshTokenAuthorizer(
            transfer_rt, auth_client, access_token=transfer_at, expires_at=expires_at_s)
    tc = globus_sdk.TransferClient(authorizer=authorizer)



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

    label = "stream test transfer"
    tdata = globus_sdk.TransferData(tc, source_endpoint_id, destination_endpoint_id,label=label) #, sync_level='checksum'
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
            #if data["status"] == "SUCCEEDED":
            if d["status"] == "SUCCEEDED":
                print ("Bytes transferred:", d["bytes_transferred"])
                print ("Files transferred:", d["files_transferred"])
                print ("Transfer rate:", d["effective_bytes_per_second"], "bps")

        """rt = int(item['request_time'])
        ct = int(item['completion_time'])
        duration = ct - rt"""
        #print('Duration time:',duration)
        #print(item['effective_bytes_per_second'])
        #files = glob.glob('/home/parallels/stream_transfer/test_files/*')
        #files = glob.glob('/home/parallels/stream_transfer/zero_globus/test_files/*')
        """for f in files:
            os.remove(f)"""


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
