# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse_name": "",
# META       "default_lakehouse_workspace_id": "",
# META       "known_lakehouses": []
# META     },
# META     "environment": {
# META       "environmentId": "4f398fe5-0eed-9e0f-448a-86e9a84899e7",
# META       "workspaceId": "00000000-0000-0000-0000-000000000000"
# META     },
# META     "warehouse": {
# META       "default_warehouse": "903daddb-302b-4960-b832-bdf5dfe0869e",
# META       "known_warehouses": [
# META         {
# META           "id": "903daddb-302b-4960-b832-bdf5dfe0869e",
# META           "type": "Lakewarehouse"
# META         }
# META       ]
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
# META   "language": "python",
# META   "language_group": "synapse_pyspark",
# META   "frozen": false,
# META   "editable": false
# META }

# CELL ********************

%run NumiHealth_msft_config_notebook {"enable_spark_setup" : true, "enable_packages_mount" : false}

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark",
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

# Invoke the OMOPIngestionService to transform and load tables into target lakehouse
from microsoft.fabric.hls.hds.services.omop_ingestion_service import OMOPIngestionService
import json

# convert inline params into dictionary
inline_params_dict = json.loads(inline_params)

# Invoke the OMOPIngestionService to transform and load tables into target lakehouse
omop_ingestion_service = OMOPIngestionService(
        spark=spark,
        workspace_name=workspace_name,
        solution_name=solution_name,
        admin_lakehouse_name=administration_database_name,
        inline_params=inline_params_dict,
        one_lake_endpoint=one_lake_endpoint
        )
omop_ingestion_service.run()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark",
# META   "frozen": false,
# META   "editable": false
# META }

# CELL ********************

mssparkutils.fs.unmount(packages_mount_name)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark",
# META   "frozen": false,
# META   "editable": false
# META }
