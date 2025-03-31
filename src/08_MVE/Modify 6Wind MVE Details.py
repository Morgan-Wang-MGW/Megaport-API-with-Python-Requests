import json
import requests
import datetime


# Function to read the config file
def read_config():
    with open('../../config/config.json', 'r') as config_file:
        return json.load(config_file)

# Function to read the config file
def read_existing_mve_service_details():
    with open('6Wind_MVE_order_details.json', 'r') as existing_mve_service_details_file:
        return json.load(existing_mve_service_details_file)


# Function to write to the config file
def write_service_details(MVE_service_update_details):
    try:
        with open('6Wind_MVE_update_details.json', 'w') as mve_service_update_detials_file:
            json.dump(MVE_service_update_details, mve_service_update_detials_file, indent=4)
        print("Successfully wrote locations to 6Wind_MVE_update_details.json")
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

current_mve_detail = read_existing_mve_service_details()
print("current_mve_detail : ", current_mve_detail)

technicalServiceUid = current_mve_detail["data"][0]["technicalServiceUid"]
print("technicalServiceUid : ", technicalServiceUid)

name = current_mve_detail["data"][0]["name"]
print("name : ", name)


#######  details for Modify ###########

put_request_url = f"https://api.megaport.com/v2/product/mve/{technicalServiceUid}"


#information for Port ordering
payload = json.dumps(
  {
      "name": "Python API Test MVE  20250331 - updated",
      # A descriptive name for the MVE.

      "costCentre": "Optional finance reference - updated",
      #(Optional) A finance reference to be used for billing purposes, such as a purchase order number.

      "marketplaceVisibility": False
      # (Optional) Publish the service on MarketPlace.

  }
)

# validate response details
put_response = requests.put(f"{put_request_url}",
                        headers=bearer_token_headers,
                        data=payload,
                        )

if put_response.status_code == 200:

    put_response_details = put_response.json()
    print("MVE update order service details : ", put_response_details)

    # Add a timestamp
    timestamp_now = datetime.datetime.now()
    put_response_details['MVE Update order timestamp'] = timestamp_now.strftime("%Y-%m-%d  %H-%M-%S")

    # Write the port service details to port_service_details.json
    write_service_details(put_response_details)

else:
   print(f'Failed to update, status code: {put_response.status_code}')
   print(f'Failed to update, details: {put_response.text}')







