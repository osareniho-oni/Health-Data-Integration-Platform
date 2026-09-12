# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "7864078c-7c67-4e33-ab08-7a92ea1ad166",
# META       "default_lakehouse_name": "NumiHealth_msft_bronze",
# META       "default_lakehouse_workspace_id": "bbae1573-fb7c-412a-9619-e1fa6a4e548e"
# META     },
# META     "environment": {
# META       "environmentId": "4f398fe5-0eed-9e0f-448a-86e9a84899e7",
# META       "workspaceId": "00000000-0000-0000-0000-000000000000"
# META     }
# META   }
# META }

# MARKDOWN ********************

# ##### WARNING
# The following notebook is intended to be read only. Please do not modify the contents of this notebook.


# CELL ********************

%run NumiHealth_msft_config_notebook

# METADATA ********************

# META {
# META   "frozen": false,
# META   "editable": false
# META }

# CELL ********************

%run NumiHealth_msft_config_notebook {"enable_spark_setup" : true, "enable_packages_mount" : false}

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
