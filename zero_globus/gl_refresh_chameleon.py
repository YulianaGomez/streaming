#!/usr/bin/env python

import re
import datetime
import requests
import logging
import json
import time
import sys
import webbrowser
import globus_sdk

#from utils import enable_requests_logging, is_remote_session

from globus_sdk import (NativeAppAuthClient, TransferClient,
                        RefreshTokenAuthorizer)
from globus_sdk.exc import GlobusAPIError


CLIENT_ID = '59a91e4c-6717-4301-8d93-f02ff19ffdf0'
TOKEN_FILE = 'refresh-tokens.json'
REDIRECT_URI = 'https://auth.globus.org/v2/web/auth-code'
SCOPES = ('openid email profile '
          'urn:globus:auth:scope:transfer.api.globus.org:all')

#change this endpoints
TUTORIAL_ENDPOINT_ID = 'ddb59aef-6d04-11e5-ba46-22000b92c6ec'


#get_input = getattr(__builtins__, 'raw_input', input)

# uncomment the next line to enable debug logging for network requests
# enable_requests_logging()


def load_tokens_from_file(filepath):
    """Load a set of saved tokens."""
    with open(filepath, 'r') as f:
        tokens = json.load(f)

    return tokens


def save_tokens_to_file(filepath, tokens):
    """Save a set of tokens for later use."""
    with open(filepath, 'w') as f:
        json.dump(tokens, f)


def update_tokens_file_on_refresh(token_response):
    """
    Callback function passed into the RefreshTokenAuthorizer.
    Will be invoked any time a new access token is fetched.
    """
    save_tokens_to_file(TOKEN_FILE, token_response.by_resource_server)


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
    #uncomment on linux machine to get a new auth code
    #if not is_remote_session():
    #    webbrowser.open(url, new=1)

    #auth_code = get_input('Enter the auth code: ').strip()
    auth_code = raw_input('Enter the auth code: ').strip()

    token_response = client.oauth2_exchange_code_for_tokens(auth_code)

    # return a set of tokens, organized by resource server name
    return token_response.by_resource_server


def transfer(sp,destination_endpoint_id,one_endpoint):
    tokens = None
    try:
        # if we already have tokens, load and use them
        tokens = load_tokens_from_file(TOKEN_FILE)
    except:
        pass

    if not tokens:
        # if we need to get tokens, start the Native App authentication process
        tokens = do_native_app_authentication(CLIENT_ID, REDIRECT_URI, SCOPES)

        try:
            save_tokens_to_file(TOKEN_FILE, tokens)
        except:
            pass

    transfer_tokens = tokens['transfer.api.globus.org']

    auth_client = NativeAppAuthClient(client_id=CLIENT_ID)

    authorizer = RefreshTokenAuthorizer(
        transfer_tokens['refresh_token'],
        auth_client,
        access_token=transfer_tokens['access_token'],
        expires_at=transfer_tokens['expires_at_seconds'],
        on_refresh=update_tokens_file_on_refresh)

    #transfer = TransferClient(authorizer=authorizer)
    tc = TransferClient(authorizer=authorizer)

    """# print out a directory listing from an endpoint
    try:
        transfer.endpoint_autoactivate(TUTORIAL_ENDPOINT_ID)
    except GlobusAPIError as ex:
        print(ex)
        if ex.http_status == 401:
            sys.exit('Refresh token has expired. '
                     'Please delete refresh-tokens.json and try again.')
        else:
            raise ex"""

      ####COPIED####
    source_endpoint_id = 'b0b16296-88e7-11e7-a971-22000a92523b' #bare chameleon
    #source_endpoint_id = 'e5762bc2-8466-11e7-a8ed-22000a92523b' #large_chameleon
    source_endpoint_id = '8b26cc0e-877b-11e7-a949-22000a92523b'#ubuntu-vm
    #source_endpoint_id = 'ad19b012-77cf-11e7-8b98-22000b9923ef'#chameleon
    # source_endpoint_id = raw_input('Input source endpoint UUID: ')
    #destination path
    ##############SOURCE PATH######################
    #source_path = '/home/parallels/stream_transfer/test_files/'
    #source_path = '/home/parallels/stream_transfer/zero_globus/test_files/'
    source_path = sp
    #source_path ='/home/cc/streaming/zero_globus/test_files/test.txt'
    #source_path = '/home/parallels/stream_transfer/zero_globus/test_files/test.txt'
    #destination path
    #destination_path = '/~/'
    #destination_path = '/~/'+ sp.split("/")[-1] #use for one file
    if one_endpoint:
        destination_path = '/projects/BrainImagingADSP/yzamora/'
    else:
        destination_path = '/projects/BrainImagingADSP/yzamora/'+ sp.split("/")[-1] #use for one file
    #Using my sample UUID from globus tutorial
    #destination_endpoint_id = 'ddb59aef-6d04-11e5-ba46-22000b92c6ec' #globus
    #destination_endpoint_id = '5d1da0fe-3c07-11e7-bcfc-22000b9a448b' #laptop



    #tc.endpoint_autoactivate(source_endpoint_id)
    #tc.endpoint_autoactive(destination_endpoint_id)
    ep1 = tc.get_endpoint(destination_endpoint_id)
    tc.endpoint_autoactivate(destination_endpoint_id)
    #ep1 is setting the activated endpoint to be a variable to work with
    tc.endpoint_autoactivate(source_endpoint_id)

    label = "medium data transfer"
    #tdata = globus_sdk.TransferData(tc, source_endpoint_id, destination_endpoint_id,label=label, sync_level='0')
    tdata = globus_sdk.TransferData(tc, source_endpoint_id, destination_endpoint_id,label=label, sync_level=None, verify_checksum=False)
    #tdata = globus_sdk.TransferData(tc, source_endpoint_id, destination_endpoint_id,label=label)
    if one_endpoint:
        tdata.add_item(source_path,destination_path,recursive=True)
    else:
        tdata.add_item(source_path,destination_path,recursive=False)

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
        """ r = tc.task_list(num_results=1, filter="type:TRANSFER,DELETE")
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
        """

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


  ###################MAIN METHOD##########################
def main():
  #if len(sys.argv)<3:
  #    print("Usage: python " + sys.argv[0] + " < endpoint = desitination endpoint>,<file path>")
  #    sys.exit(0)

  destination_ep = sys.argv[1]
  #files = sys.argv[2]


  transfer('/home/cc/streaming/zero_globus/test_files2',destination_ep)




if __name__ == '__main__':
  main()
    #for entry in transfer.operation_ls(TUTORIAL_ENDPOINT_ID, path='/~/'):
      #  print(entry['name'] + ('/' if entry['type'] == 'dir' else ''))

    # revoke the access token that was just used to make requests against
    # the Transfer API to demonstrate that the RefreshTokenAuthorizer will
    # automatically get a new one
    #auth_client.oauth2_revoke_token(authorizer.access_token)
    # Allow a little bit of time for the token revocation to settle
    #time.sleep(1)
    # Verify that the access token is no longer valid
    #token_status = auth_client.oauth2_validate_token(
    #    transfer_tokens['access_token'])
    #assert token_status['active'] is False, 'Token was expected to be invalid.'

    #print('\nDoing a second directory listing with a new access token:')
    #for entry in transfer.operation_ls(TUTORIAL_ENDPOINT_ID, path='/~/'):
    #    print(entry['name'] + ('/' if entry['type'] == 'dir' else ''))
