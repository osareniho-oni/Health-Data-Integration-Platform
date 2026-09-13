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
# META     }
# META   }
# META }

# CELL ********************

# Welcome to your new notebook
# Type here in the cell editor to add code!


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

import json

# Define the source file path
abfs_path = "abfss://bbae1573-fb7c-412a-9619-e1fa6a4e548e@onelake.dfs.fabric.microsoft.com/e7202eb9-35b9-46a9-94cb-eb13d23b04cd/Files"
source_file_path = f"{abfs_path}/system-configurations/deploymentParametersConfiguration.json"

# Step 1: Read the JSON file content (first 1MB)
file_content = mssparkutils.fs.head(source_file_path, 1024 * 1024)  # Read the first MB of the file

# Step 2: Parse the JSON data
json_data = json.loads(file_content)

# Step 3: Iterate over all activities and update the parameters (source_path_pattern, move_failed_files_enabled, compression_enabled)
if "activities" in json_data:
    for activity_id, activity_data in json_data["activities"].items():

        # Check if the activity name partially matches " msft_fhir_ndjson_bronze_ingestion"
        if "name" in activity_data and "msft_fhir_ndjson_bronze_ingestion" in activity_data["name"]:
            if "parameters" in activity_data:
                parameters = activity_data["parameters"]

                # Modify source_path_pattern
                if "source_path_pattern" in parameters:
                    current_path = parameters["source_path_pattern"]
                    updated_path = current_path.replace('/Files/External/Clinical/FHIR-NDJSON', '/Files/Process/Clinical/FHIR-NDJSON')
                    parameters["source_path_pattern"] = updated_path
                    print(f"Updated source_path_pattern for activity {activity_id}")

                # Set move_failed_files_enabled to "false"
                if "move_failed_files_enabled" in parameters:
                    parameters["move_failed_files_enabled"] = "true"
                    print(f"Set move_failed_files_enabled to true for activity {activity_id}")

                # Set compression_enabled to "false"
                if "compression_enabled" in parameters:
                    parameters["compression_enabled"] = "true"
                    print(f"Set compression_enabled to true for activity {activity_id}")
        else:
            print(f"Activity {activity_id} does not match the filter")
else:
    raise KeyError("No activities found in the JSON file")

# Step 4: Convert the modified JSON data back to string
modified_json_content = json.dumps(json_data, indent=4)

# Step 5: Delete the existing file (to avoid FileAlreadyExistsException)
mssparkutils.fs.rm(source_file_path)

# Step 6: Save the modified JSON content back to the destination file
mssparkutils.fs.put(source_file_path, modified_json_content)

# Confirm that the modification was successful
print(f"Modified parameters in {source_file_path}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
