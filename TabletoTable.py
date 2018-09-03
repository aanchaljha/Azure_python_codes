from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.datafactory.models import AzureMySqlTableDataset
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.datafactory import DataFactoryManagementClient
from azure.mgmt.datafactory.models import *
from datetime import datetime, timedelta

import azure.mgmt.resource
import azure.datalake.store
import azure.mgmt.datalake.store
import azure.mgmt.datalake.analytics
import time
import configparser

config = configparser.ConfigParser()
config.read('/home/zensar/Config_data/TableToTable.cfg')

subscription_id = config.get('CONNECTION', 'subscription_id')
azureSqlConnectionString=config.get('CONNECTION','azureSqlConnString')
rg_name = config.get('CONNECTION', 'rg_name')
df_name = config.get('CONNECTION', 'df_name')
client_id = config.get('CONNECTION', 'client_id')
secret = config.get('CONNECTION', 'secret')
tenant = config.get('CONNECTION', 'tenant')
ls_name = config.get('CONNECTION', 'ls_name')
ls_name1 = config.get('CONNECTION', 'ls_name1')
ds_name = config.get('CONNECTION', 'dsIn_name')

dsOut_name = config.get('CONNECTION', 'dsOut_name')
integrationRuntime=config.get('CONNECTION','integrationRuntime')
act_name = config.get('CONNECTION', 'act_name')
act_description = config.get('CONNECTION', 'act_description')
p_name = config.get('CONNECTION', 'p_name')
storage_account_details = config.get('CONNECTION', 'storage_account_details')



class SqlToSql:

    def print_item(group):
        print("\tName: {}".format(group.name))
        print("\tId: {}".format(group.id))
        if hasattr(group, 'location'):
            print("\tLocation: {}".format(group.location))
        if hasattr(group, 'tags'):
            print("\tTags: {}".format(group.tags))
        if hasattr(group, 'properties'):
            SqlToSql.print_properties(group.properties)
        print("\n")

    def print_properties(props):
        if props and hasattr(props, 'provisioning_state') and props.provisioning_state:
            print("\tProperties:")
            print("\t\tProvisioning State: {}".format(props.provisioning_state))
        print("\n")

    def print_activity_run_details(activity_run):
        print("\n\tActivity run details\n")
        print("\tActivity run status: {}".format(activity_run.status))
        if activity_run.status == 'Succeeded':
            print("\tNumber of bytes read: {}".format(activity_run.output['dataRead']))
            print("\tNumber of bytes written: {}".format(activity_run.output['dataWritten']))
            print("\tCopy duration: {}".format(activity_run.output['copyDuration']))
        else:
            print("\tErrors: {}".format(activity_run.error['message']))

    def main(self):
	

        credentials = ServicePrincipalCredentials(client_id=client_id, secret=secret, tenant=tenant)

        adf_client = DataFactoryManagementClient(credentials, subscription_id)


        # Create a data factory
        df_resource = Factory(location='eastus')
        df = adf_client.factories.create_or_update(rg_name, df_name, df_resource)

        SqlToSql.print_item(df)
        while df.provisioning_state != 'Succeeded':
            df = adf_client.factories.get(rg_name, df_name)
        time.sleep(1)


        mysqlConnString = 'server='';port='';database='';user='';password=''S;sslmode=1;usesystemtruststore=0'
        mysqlTableName = 'test'
        storage_string = SecureString(mysqlConnString)

        #Pass Integrationruntime name
        ls_azure_storage = AzureMySqlLinkedService(connection_string=storage_string,connect_via={'referenceName':integrationRuntime,'type':'IntegrationRuntimeReference'})

        azureSqlConnString = azureSqlConnectionString
        azureSqlTableName = 'test'

        storage_string1 = SecureString(azureSqlConnString)
        ls_azure_storage1 = AzureSqlDatabaseLinkedService(connection_string=storage_string1)

        ls = adf_client.linked_services.create_or_update(rg_name, df_name, ls_name, ls_azure_storage)

        ls1 = adf_client.linked_services.create_or_update(rg_name, df_name, ls_name1, ls_azure_storage1)

        ds_ls = LinkedServiceReference(ls_name)

        ds_ls1 = LinkedServiceReference(ls_name1)

        ds_azure_blob = AzureMySqlTableDataset(ds_ls,table_name=mysqlTableName)
        ds = adf_client.datasets.create_or_update(rg_name, df_name, ds_name, ds_azure_blob)
        SqlToSql.print_item(ds)

        dsOut_azure_blob1 = AzureSqlTableDataset(linked_service_name=ds_ls1, table_name=azureSqlTableName)
        dsOut = adf_client.datasets.create_or_update(rg_name, df_name, dsOut_name, dsOut_azure_blob1)

        SqlToSql.print_item(dsOut)

        blob_source = BlobSource()
        blob_sink = BlobSink()
        dsin_ref = DatasetReference(ds_name)
        dsOut_ref = DatasetReference(dsOut_name)

        p = ActivityPolicy();
        p.timeout = '3.00:00:00'
        p.retry = 2
        p.retry_interval_in_seconds = 50

        copy_activity = CopyActivity(name=act_name,
                                     description='copy data from SQL to SQL',
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

        SqlToSql.print_item(p)

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
        SqlToSql.print_activity_run_details(activity_runs_paged[0])

        # Start the main method


if __name__ == '__main__':
    print("hello")
    SqlToSql.main(self='self')
