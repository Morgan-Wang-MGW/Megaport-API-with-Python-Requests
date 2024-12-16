import json
import requests
import datetime


# Function to read the config file
def read_config():
    with open('../../config/config.json', 'r') as config_file:
        return json.load(config_file)

# Function to read the current service file
def read_existing_port_service_details():
    with open('port_service_details.json', 'r') as existing_port_service_details_file:
        return json.load(existing_port_service_details_file)


# Read the existing config file for current access token
config = read_config()
access_token = config['access_token']

# Carry current access token in request header
bearer_token_headers = {
   'Content-Type': 'application/json',
   'Authorization': f'Bearer {access_token}'
}

current_port_detail = read_existing_port_service_details()
print("current_port_detail : ", current_port_detail)

technicalServiceId = current_port_detail["data"][0]["technicalServiceId"]
print("technicalServiceId : ", technicalServiceId)

technicalServiceUid = current_port_detail["data"][0]["technicalServiceUid"]
print("technicalServiceUid : ", technicalServiceUid)

first_part = technicalServiceUid.split('-')[0]
print("technicalServiceUid_first_part : ", first_part)

####### Get LOA file of Port ###########
port_update_url = "https://api.megaport.com/v2/product/"


#information for LOA
payload = json.dumps(
  {

  }
)

# Get LOA file with Service Uid
response = requests.get(f"{port_update_url}/{technicalServiceUid}/loa",
                        headers=bearer_token_headers,
                        data=payload,
                        )

if response.status_code == 200:


    # Use the Servie IDs as a default name
    file_name = f"Service ID {first_part} ({technicalServiceId}) LOA.pdf"

    # Open a local file to write the downloaded content
    with open(file_name, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    print(f"File downloaded successfully as {file_name}!")

else:
   print(f'Failed to update, status code: {order_response.status_code}')
   print(f'Failed to update, details: {order_response.text}')







