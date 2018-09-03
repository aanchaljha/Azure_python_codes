from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.datafactory import DataFactoryManagementClient
from azure.mgmt.datafactory.models import *
from datetime import datetime, timedelta

import os, uuid, sys, os
from azure.storage.blob import BlockBlobService, PublicAccess

import azure.mgmt.resource
import azure.datalake.store
import azure.mgmt.datalake.store
import azure.mgmt.datalake.analytics
import time
import configparser

config = configparser.ConfigParser()
config.read('/home/zensar/Config_data/CSVToTable.cfg')

subscription_id = config.get('CONNECTION', 'subscription_id')

accountkey=config.get('CONNECTION','accountkey')
accountname=config.get('CONNECTION','accountname')
azureSqlConnectionString=config.get('CONNECTION','azureSqlConnString')
rg_name = config.get('CONNECTION', 'rg_name')
df_name = config.get('CONNECTION', 'df_name')
client_id = config.get('CONNECTION', 'client_id')
secret = config.get('CONNECTION', 'secret')
tenant = config.get('CONNECTION', 'tenant')
ls_name = config.get('CONNECTION', 'ls_name')
ls_name1 = config.get('CONNECTION', 'ls_name1')
ds_name = config.get('CONNECTION', 'dsIn_name')
blob_path = config.get('CONNECTION', 'blob_path')
path1 = config.get('CONNECTION', 'path')
dsOut_name = config.get('CONNECTION', 'dsOut_name')
output_blobpath = config.get('CONNECTION', 'output_blobpath')
act_description = config.get('CONNECTION', 'act_description')
storage_account_details = config.get('CONNECTION', 'storage_account_details')
p_name = config.get('CONNECTION', 'p_name')
act_name = config.get('CONNECTION', 'act_name')
azureSqlTableName = config.get('CONNECTION','azureSqlTableName')

print("azureSqlConnectionString:"+azureSqlConnectionString)


class BlobToSql:
       
    def print_item(group):
        print("Name: {}".format(group.name))
        print("Id: {}".format(group.id))
        if hasattr(group, 'location'):
            print("Location: {}".format(group.location))
        if hasattr(group, 'tags'):
            print("Tags: {}".format(group.tags))
        if hasattr(group, 'properties'):
            BlobToSql.print_properties(group.properties)
        print("\n")

    def print_properties(props):
        if props and hasattr(props, 'provisioning_state') and props.provisioning_state:
            print("Properties:")
            print("Provisioning State: {}".format(props.provisioning_state))
        print("\n")

    def print_activity_run_details(activity_run):
        print("\nActivity run details\n")
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
            path = path1
            print(container_name)
            head, tail = os.path.split(path)
            print(tail)
           

            # Upload the created file, use local_file_name for the blob name
            block_blob_service.create_blob_from_path(container_name, tail, path)

            # List the blobs in the container
            print("\nList blobs in the container")
            generator = block_blob_service.list_blobs(container_name)
            for blob in generator:
                print("\t Blob name: " + blob.name)


        except Exception as e:
            print(e)



        credentials = ServicePrincipalCredentials(client_id=client_id, secret=secret, tenant=tenant)

        adf_client = DataFactoryManagementClient(credentials, subscription_id)

        # Create a data factory
        df_resource = Factory(location='eastus')
        df = adf_client.factories.create_or_update(rg_name, df_name, df_resource)
        BlobToSql.print_item(df)
        while df.provisioning_state != 'Succeeded':
            df = adf_client.factories.get(rg_name, df_name)
        time.sleep(1)

        storage_string = SecureString(storage_account_details)
        ls_azure_storage = AzureStorageLinkedService(connection_string=storage_string)
	
        storage_string1 = SecureString(azureSqlConnectionString)
        ls_azure_storage1 = AzureSqlDatabaseLinkedService(connection_string=storage_string1)

        ls = adf_client.linked_services.create_or_update(rg_name, df_name, ls_name, ls_azure_storage)

        ls1 = adf_client.linked_services.create_or_update(rg_name, df_name, ls_name1, ls_azure_storage1)

        ds_ls = LinkedServiceReference(ls_name)

        ds_ls1 = LinkedServiceReference(ls_name1)

        ds_azure_blob = AzureBlobDataset(ds_ls, folder_path=blob_path, file_name=tail, format={'type':'TextFormat','skipLineCount':'0','firstRowAsHeader': 'true'})
        ds = adf_client.datasets.create_or_update(rg_name, df_name, ds_name, ds_azure_blob)
        BlobToSql.print_item(ds)

        dsOut_azure_blob1 = AzureSqlTableDataset(linked_service_name=ds_ls1, table_name=azureSqlTableName,)
        dsOut = adf_client.datasets.create_or_update(rg_name, df_name, dsOut_name, dsOut_azure_blob1)


        BlobToSql.print_item(dsOut)

        blob_source = BlobSource()
        blob_sink = BlobSink()
        dsin_ref = DatasetReference(ds_name)
        dsOut_ref = DatasetReference(dsOut_name)

        p = ActivityPolicy();
        p.timeout = '3.00:00:00'
        p.retry = 2
        p.retry_interval_in_seconds = 50

        copy_activity = CopyActivity(name=act_name,
                                     description=act_description,
                                     enable_staging='false',
                                     # cloud_data_movement_units='',
                                     # parallel_copies='',
                                     enable_skip_incompatible_row='false',
                                     inputs=[dsin_ref],
                                     outputs=[dsOut_ref],
                                     source=blob_source,
                                     sink=blob_sink,
                                     policy=p)

        params_for_pipeline = {}
        p_obj = PipelineResource(activities=[copy_activity], parameters=params_for_pipeline)
        p = adf_client.pipelines.create_or_update(rg_name, df_name, p_name, p_obj)

        BlobToSql.print_item(p)

        # Create a pipeline run
        run_response = adf_client.pipelines.create_run(rg_name, df_name, p_name,
                                                       {
                                                       }
                                                       )
        # Monitor the pipeilne run
        time.sleep(20)

        # file = open('/home/zensar/azure_log1.txt', 'a+')

        pipeline_run = adf_client.pipeline_runs.get(rg_name, df_name, run_response.run_id)
        print("\n\tPineLine Id:{}".format(pipeline_run.run_id))

        print("\n\tPipeline run status: {}".format(pipeline_run.status))

        activity_runs_paged = list(adf_client.activity_runs.list_by_pipeline_run(rg_name, df_name,
                                                                                 pipeline_run.run_id,
                                                                                 datetime.now() - timedelta(1),
                                                                                 datetime.now() + timedelta(1)))
        BlobToSql.print_activity_run_details(activity_runs_paged[0])

        # Start the main method


if __name__ == '__main__':
	
    BlobToSql.main(self='self')
