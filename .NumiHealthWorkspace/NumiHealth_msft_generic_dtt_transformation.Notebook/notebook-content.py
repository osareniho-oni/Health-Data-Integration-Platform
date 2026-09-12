# Fabric notebook source

# METADATA ********************

# META {
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "f4dfa09a-6b83-4863-b051-4a257543a5f9",
# META       "default_lakehouse_name": "NumiHealth_msft_silver",
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


# MARKDOWN ********************

# # Overview
# In this notebook, we will leverage the DTT generic service shipped as part of Healthcare data solutions library to transform data from the `source` lakehouse delta tables in to `target` lakehouse delta tables. 
# 
# ### DTTService
# The `DTTService` takes in the following arguments:
# - `workspace_name`: Name of the Fabric Workspace
# - `solution_name`:  DMH OneLake workload solution name
# - `inline_params` : Json dictionary of parameters(configuration values)
# - `admin_lakehouse_name`: The lakehouse name of where the administration configurations are located
# - `one_lake_endpoint` (str): The one lake endpoint. Default is `onelake.dfs.fabric.microsoft.com`
# ### Usage
# - Execute the notebook.
# 
# _For more information and detailed steps see the [Healthcare data solutions Documentation](https://aka.ms/hds-doc)_


# MARKDOWN ********************

# ##### Configuration management and setup
# The following cells will setup and manage configurations for the Healthcare data solutions:

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

# MARKDOWN ********************

# ##### Invoke the Healthcare data solutions API
# Now we will invoke the `run()` of `DTTService` to transform data from `source` lakehouse delta tables in to `target` lakehouse delta tables.
# `inline_params` is a json dictionary of parameters(configuration values) which will take precedence and be use to set the following arguments:
# - `dtt_source_lakehouse_id`: Source lakehouse id*
# - `dtt_target_lakehouse_id`:  Target lakehouse id*
# - `dtt_service_config_path`: File path of the configuration files*
# -  arguments marked as `*` are mandatory and required for transformation.

# PARAMETERS CELL ********************

inline_params = "{}"

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark",
# META   "frozen": false,
# META   "editable": false
# META }

# MARKDOWN ********************

# To locate `Source/Target` lakehouse id, open the `Source/Target` lakehouse and check the URL in the browser’s address bar (https://{baseurl}/lakehouses/{GUID}?experience=power-bi).The {GUID} part of the URL is the `Source/Target` lakehouse id.
# 
`dtt_service_config_path` value should be `ABFS path` like `abfss://{Workspace_name}@com/{Lakehouse_name}.Lakehouse/Files/{Folder_name}`
# - As per transformation, `dtt_service_config_path` may contain below files:
#     - `dbTargetSchema.json` to define the structure (schema) of the target database.
#         - **Schema Validation:** to validate that the data being written to or read from the database matches the expected schema.
#         - **Dynamic Table Creation:** to dynamically create or alter database tables to match the required structure.
#         - **Data Mapping:** to help mapping incoming data fields to the correct database columns.
#         - **Error Checking:** Ensures that any data processed by the workflow adheres to the constraints and types defined in the schema.
#     - `dbTargetSchemaConfig.json` to define metadata and configuration for database schema fields, partitioning, and reference table ranges.
#         - **Schema Definition**: Specify which fields (like `SourceModifiedOn`, `SourceTable`) should be included in the target schema, their types, and which tables they apply to.
#         - **Partitioning**: Define how data should be partitioned (e.g., by year, month, day, person ID, location ID) to optimize storage and querying.
#         - **Reference Ranges**: Provide value ranges for reference tables (like `Concept`) to validate or filter data.
#         - **Configuration**: Indicate which fields in the schema correspond to special roles (e.g., which field tracks modification time).
#     - `dmfAdapter.json` to transform and map data fields during the execution.
#         - **Field Mapping:** To define how source fields are mapped to target fields in database tables. 
#         - **Transformation Rules:** The `fieldCalculatedValue` property specifies how to compute the value for each field, possibly using functions (e.g., `concat_ws('<->', ...)`) or direct assignments.
#         - **Type and Enablement:** Each field mapping includes type information and an `enabled` flag to control whether the mapping is active.
#     - `dmfAdapterSchema.json` to define and validate the structure of configuration or data files related to DMF (Data Mapping Framework) adapters for parsing and extraction.
#     - `dbSemantics.json` to define metadata about your database schema.
#         - **referenceTables**: Tables used for lookups (e.g., mapping IDs to names).
#         - **extensionTables**: Relationships between tables (e.g., parent-child).
#         - **modifiedOnTargetField**: To track modifications.
#     - `dbSemanticsConfig.json` to define partitioning rules for database operations.
#         - **Load Partitioning Rules:** to understand how data should be partitioned or sharded for processing.
#         - **Apply Partition Logic:** to determine which partition a record belongs to.
#     

# CELL ********************

# Invoke the DTTService to transform data from the source lakehouse into target lakehouse
from microsoft.fabric.hls.hds.services.dtt_service import DTTService
import json

# convert inline params into dictionary
inline_params_dict = json.loads(inline_params)

# Invoke the DTTService to transform data from the source lakehouse into target lakehouse
dtt_ingestion_service = DTTService(
        spark=spark,
        workspace_name=workspace_name,
        solution_name=solution_name,
        admin_lakehouse_name=administration_database_name,
        inline_params=inline_params_dict,
        one_lake_endpoint=one_lake_endpoint
        )
dtt_ingestion_service.run()


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
