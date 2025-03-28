import json
import requests
import datetime


# Function to read the config file
def read_config():
    with open('../../config/config.json', 'r') as config_file:
        return json.load(config_file)

# Function to read the config file
def read_existing_service_details():
    with open('MCR_service_order_details.json', 'r') as existing_service_details_file:
        return json.load(existing_service_details_file)


# Function to write to the config file
def write_service_details(mcr_prefix_details):
    try:
        with open('MCR_prefix_list.json', 'w') as mcr_prefix_details_file:
            json.dump(mcr_prefix_details, mcr_prefix_details_file, indent=4)
        print("Successfully wrote to mcr_prefix_details.json")
    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")
    except TypeError as e:
        print(f"The data is not JSON serializable: {e}")

# Read the existing config file for current access token
config = read_config()
access_token = config['access_token']

# Carry current access token in request header
bearer_token_headers = {
   'Content-Type': 'application/json',
   'Authorization': f'Bearer {access_token}'
}

current_mcr_detail = read_existing_service_details()
print("current_mcr_detail : ", current_mcr_detail)

technicalServiceUid = current_mcr_detail["data"][0]["technicalServiceUid"]
print("technicalServiceUid : ", technicalServiceUid)

name = current_mcr_detail["data"][0]["name"]
print("name : ", name)


####### Send VXC update details ###########
mcr_prefix_url = f"https://api.megaport.com/v2/product/mcr2/{technicalServiceUid}/prefixLists"


#information for Port ordering
payload = json.dumps(
    {
    }
)

# get prefix details
get_response = requests.get(mcr_prefix_url, headers=bearer_token_headers)


if get_response.status_code == 200:

    mcr_prefix_details = get_response.json()
    print("MCR Prefix details : ", mcr_prefix_details)

    # Add a timestamp
    timestamp_now = datetime.datetime.now()
    mcr_prefix_details['MCR Get Prefix timestamp'] = timestamp_now.strftime("%Y-%m-%d  %H-%M-%S")

    # Write the VXC service details to vxc_service_details.json
    write_service_details(mcr_prefix_details)

else:
   print(f'Failed to get Prefix, status code: {get_response.status_code}')
   print(f'Failed to get Prefix, details: {get_response.text}')







