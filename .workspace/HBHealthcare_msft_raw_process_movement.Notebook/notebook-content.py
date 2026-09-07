# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "aee9e277-f8b3-4691-9a0e-0d62dcfe6144",
# META       "default_lakehouse_name": "HBHealthcare_msft_bronze",
# META       "default_lakehouse_workspace_id": "34ae0cb3-7f44-43a7-8685-084dd84d8af3"
# META     },
# META     "environment": {
# META       "environmentId": "d94b227b-02a4-9afd-4990-f301dbda3492",
# META       "workspaceId": "00000000-0000-0000-0000-000000000000"
# META     }
# META   }
# META }

# MARKDOWN ********************

# ##### WARNING
# The following notebook is intended to be read only. Please do not modify the contents of this notebook.


# CELL ********************

%run HBHealthcare_msft_config_notebook

# METADATA ********************

# META {
# META   "frozen": false,
# META   "editable": false
# META }

# CELL ********************

%run HBHealthcare_msft_config_notebook {"enable_spark_setup" : true, "enable_packages_mount" : false}

# METADATA ********************

# META {
# META   "frozen": false,
# META   "editable": false
# META }

# PARAMETERS CELL ********************

inline_params = "{}"

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark",
# META   "frozen": false,
# META   "editable": false
# META }

# CELL ********************

from microsoft.fabric.hls.hds.services.file_orchestration_service import FileOrchestrationService
import json

# convert inline params into dictionary
inline_params_dict = json.loads(inline_params)

service = FileOrchestrationService(spark, 
                workspace_name=workspace_name,
                solution_name=solution_name,
                admin_lakehouse_name=administration_database_name,
                inline_params=inline_params_dict,
                one_lake_endpoint=one_lake_endpoint)

service.run()

# METADATA ********************

# META {
# META   "frozen": false,
# META   "editable": false
# META }

# CELL ********************

mssparkutils.fs.unmount(packages_mount_name)

# METADATA ********************

# META {
# META   "frozen": false,
# META   "editable": false
# META }
