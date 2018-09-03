import os, uuid, sys, os
from azure.storage.blob import BlockBlobService, PublicAccess

from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.datafactory import DataFactoryManagementClient
from azure.mgmt.datafactory.models import *
from datetime import datetime, timedelta

import time
import configparser

config = configparser.ConfigParser()
config.read('/home/zensar/Config_data/BlobToBlob.cfg')

accountname=config.get('CONNECTION','accountname')
accountkey=config.get('CONNECTION','accountkey')
subscription_id = config.get('CONNECTION', 'subscription_id')
filepath = config.get('CONNECTION', 'path')
rg_name = config.get('CONNECTION', 'rg_name')
df_name = config.get('CONNECTION', 'df_name')
client_id=config.get('CONNECTION', 'client_id')
secret=config.get('CONNECTION', 'secret')
tenant=config.get('CONNECTION', 'tenant')
ls_name = config.get('CONNECTION', 'ls_name')
dsIn_name = config.get('CONNECTION', 'dsIn_name')
dsOut_name = config.get('CONNECTION', 'dsOut_name')
output_blobpath = config.get('CONNECTION', 'output_blobpath')
act_name = config.get('CONNECTION', 'act_name')
act_description= config.get('CONNECTION','act_description')
p_name = config.get('CONNECTION', 'p_name')
storage_account_details=config.get('CONNECTION','storage_account_details')
blob_path=config.get('CONNECTION','blob_path')


class BlobToBlob:

    def print_item(group):
        print("Name: {}".format(group.name))
        print("Id: {}".format(group.id))
        if hasattr(group, 'location'):
            print("Location: {}".format(group.location))
        if hasattr(group, 'tags'):
            print("Tags: {}".format(group.tags))
        if hasattr(group, 'properties'):
            BlobToBlob.print_properties(group.properties)
        print("\n")


    def print_properties(props):
        if props and hasattr(props, 'provisioning_state') and props.provisioning_state:
            print("Properties:")
            print("Provisioning State: {}".format(props.provisioning_state))
        print("\n")


    def print_activity_run_details(activity_run):
        print("Activity run details\n")
        print("Activity run status: {}".format(activity_run.status))

        if activity_run.status == 'Succeeded':
            print("Number of bytes read: {}".format(activity_run.output['dataRead']))
            print("Number of bytes written: {}".format(activity_run.output['dataWritten']))
            print("Copy duration: {}".format(activity_run.output['copyDuration']))
        else:
            print("Errors: {}".format(activity_run.error['message']))


    def main(self):


      
	
        try:
            # Create the BlockBlockService that is used to call the Blob service for the storage account
            block_blob_service = BlockBlobService(account_name=accountname, account_key=accountkey)

            # Create a container called 'quickstartblobs'.
            container_name=blob_path
            block_blob_service.create_container(container_name)

            # Set the permission so the blobs are public.
            block_blob_service.set_container_acl(container_name, public_access=PublicAccess.Container)

            # choose file from system
            path = filepath
            print(container_name)
            head, tail = os.path.split(path)
            print(tail)
           

            # Upload the created file, use local_file_name for the blob name
            block_blob_service.create_blob_from_path(container_name, tail, path)

            # List the blobs in the container
            print("\nList blobs in the container")
            generator = block_blob_service.list_blobs(container_name)
            for blob in generator:
                print("\nBlob name: " + blob.name)


        except Exception as e:
            print(e)


        

        credentials = ServicePrincipalCredentials(client_id=client_id,secret=secret, tenant=tenant)

        adf_client = DataFactoryManagementClient(credentials, subscription_id)

        # Create a data factory
        df_resource = Factory(location='eastus')
        df = adf_client.factories.create_or_update(rg_name, df_name, df_resource)
        BlobToBlob.print_item(df)
        while df.provisioning_state != 'Succeeded':
            df = adf_client.factories.get(rg_name, df_name)
        time.sleep(1)

        # Create an Azure Storage linked service
        storage_string = SecureString(storage_account_details)
        ls_azure_storage = AzureStorageLinkedService(connection_string=storage_string)


        ls = adf_client.linked_services.create_or_update(rg_name, df_name, ls_name, ls_azure_storage)
        BlobToBlob.print_item(ls)



        ds_ls = LinkedServiceReference(ls_name)

        ds_azure_blob = AzureBlobDataset(ds_ls, folder_path=blob_path, file_name=tail)
        ds = adf_client.datasets.create_or_update(rg_name, df_name, dsIn_name, ds_azure_blob)
        BlobToBlob.print_item(ds)

        dsOut_azure_blob = AzureBlobDataset(ds_ls, folder_path=output_blobpath)
        dsOut = adf_client.datasets.create_or_update(rg_name, df_name, dsOut_name, dsOut_azure_blob)
        BlobToBlob.print_item(dsOut)

        # Create a copy activity
        blob_source = BlobSource()
        blob_sink = BlobSink()
        dsin_ref = DatasetReference(dsIn_name)
        dsOut_ref = DatasetReference(dsOut_name)

        p=ActivityPolicy();
        p.timeout='3.00:00:00'
        p.retry=2
        p.retry_interval_in_seconds=50

        copy_activity=CopyActivity(name=act_name,
                                   description=act_description,
                                   enable_staging='false',
                                   enable_skip_incompatible_row='false',
                                   inputs=[dsin_ref],
                                   outputs=[dsOut_ref],
                                   source=blob_source,
                                   sink=blob_sink,
                                   policy=p)




        params_for_pipeline = {}
        p_obj = PipelineResource(activities=[copy_activity], parameters=params_for_pipeline)
        p = adf_client.pipelines.create_or_update(rg_name, df_name, p_name, p_obj)

        BlobToBlob.print_item(p)

        # Create a pipeline run
        run_response = adf_client.pipelines.create_run(rg_name, df_name, p_name,
                                                   {
                                                   }
                                                     )
        # Monitor the pipeilne run
        time.sleep(20)

        pipeline_run = adf_client.pipeline_runs.get(rg_name, df_name, run_response.run_id)
        print("\nPineLine Id:{}".format(pipeline_run.run_id))

        print("\nPipeline run status: {}".format(pipeline_run.status))



        activity_runs_paged = list(adf_client.activity_runs.list_by_pipeline_run(rg_name, df_name,
                                                                             pipeline_run.run_id,
                                                                             datetime.now() - timedelta(1),
                                                                             datetime.now() + timedelta(1)))
        BlobToBlob.print_activity_run_details(activity_runs_paged[0])

        # Start the main method

if __name__ == '__main__':

       BlobToBlob.main(self='self')
