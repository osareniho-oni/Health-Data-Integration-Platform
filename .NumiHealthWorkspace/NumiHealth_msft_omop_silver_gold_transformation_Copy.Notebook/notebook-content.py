# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
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

import importlib.metadata as md

packages = [
    "azure-monitor-opentelemetry",
    "azure-monitor-opentelemetry-exporter",
    "azure-core-tracing-opentelemetry",
    "opentelemetry-api",
    "opentelemetry-sdk",
    "opentelemetry-instrumentation",
]

for p in packages:
    try:
        dist = md.distribution(p)
        print(f"\n{p} == {dist.version}")
        print("Requires:")
        for req in dist.requires or []:
            if "opentelemetry" in req.lower():
                print("  ", req)
    except Exception as e:
        print(p, "ERROR:", e)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

%run NumiHealth_msft_config_notebook

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

%run NumiHealth_msft_config_notebook {"enable_spark_setup" : true, "enable_packages_mount" : false}

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

inline_params = "{}"

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
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
# META   "language_group": "synapse_pyspark"
# META }
