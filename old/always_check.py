from globus_sdk import (TransferClient, TransferAPIError,
                        TransferData, DeleteData, AccessTokenAuthorizer)
import glob, os
import shutil
#from find_uuid import find_uuid

#Transfer script that is 'always' running and waiting to see if there is a file to transfer
#Will check if transferred onto GLOBUS and delete after transfer only

def transfer():
    while True:
        token_authorizer = AccessTokenAuthorizer(access_token = 'AQBZKFOiAAAAAAAFF9UrJWHsmrT0ZxNuzwDzSGiAlJ1q4g-djunpQ2iDx9z-lvNbePOJWK9fuVKSRBSNQYoo')
        transfer = TransferClient(token_authorizer)
#UUID can be found at your endpoint at globus or through tokens.globus.org
#endpoints need to be established before transfer data

#UUID -this is my endpoint UUID
        source_endpoint_id = '2b5e59d2-409e-11e7-bd30-22000b9a448b'
# source_endpoint_id = raw_input('Input source endpoint UUID: ')
#destination path
        source_path = os.listdir("/home/parallels/globus-sdk-python/globusnram/test_files/")
        for files in source_path:
            if files.endswith(".txt"):
# source_path = raw_input('Input source path: ')
#destination path
        	    destination_path = '~/'
#destination_path = raw_input('Input destination path: ')
#Using my sample UUID from globus tutorial
#destination_endpoint_id = raw_input('Input destination endpoint UUID: ')
       	        destination_endpoint_id = 'ddb59aef-6d04-11e5-ba46-22000b92c6ec'

#you can't transfer without telling the endpoints you are about to transfer
	            ep1 = transfer.get_endpoint(destination_endpoint_id)
	            transfer.endpoint_autoactivate(destination_endpoint_id)om
        #ep1 is setting the activated endpoint to be a variable to work with
	            transfer.endpoint_autoactivate(source_endpoint_id)
        #setup of the transfer, submits as a https post request
	            transfer_data = TransferData(transfer_client=transfer,
				                 source_endpoint=source_endpoint_id,
				                 destination_endpoint=destination_endpoint_id,
				                 label='Transfer',
				                 sync_level='checksum')
	            transfer_data.add_item(source_path=source_path,destination_path=destination_path, recursive=False)
	            task_id=transfer.submit_transfer(transfer_data)['task_id']

            transfer()
