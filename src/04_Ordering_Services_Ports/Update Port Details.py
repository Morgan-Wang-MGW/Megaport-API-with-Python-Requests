import json
import requests
import datetime


# Function to read the config file
def read_config():
    with open('../../config/config.json', 'r') as config_file:
        return json.load(config_file)

# Function to read the config file
def read_existing_port_service_details():
    with open('port_service_details.json', 'r') as existing_port_service_details_file:
        return json.load(existing_port_service_details_file)


# Function to write to the config file
def write_service_details(port_service_details):
    try:
        with open('updated_port_service_details.json', 'w') as port_service_detials_file:
            json.dump(port_service_details, port_service_detials_file, indent=4)
        print("Successfully wrote locations to updated_port_service_details.json")
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

current_port_detail = read_existing_port_service_details()
print("current_port_detail : ", current_port_detail)

technicalServiceUid = current_port_detail["data"][0]["technicalServiceUid"]
print("technicalServiceUid : ", technicalServiceUid)

name = current_port_detail["data"][0]["name"]
print("name : ", name)

costCentre = current_port_detail["data"][0]["costCentre"]
print("costCentre : ", costCentre)

marketplaceVisibility = current_port_detail["data"][0]["marketplaceVisibility"]
print("marketplaceVisibility : ", marketplaceVisibility)



####### Send Port order details for Order ###########
port_update_url = "https://api.megaport.com/v2/product/"


#information for Port ordering
payload = json.dumps(
  {
      "name": "Python API Test Port - updated details",
      # A descriptive name for the Port.

      "costCentre": "Optional finance reference - updated",
      #(Optional) A finance reference to be used for billing purposes, such as a purchase order number.

      "marketplaceVisibility": False
      # (Optional) Publish the service on MarketPlace.

  }
)

# validate order details and get price
order_response = requests.put(f"{port_update_url}/{technicalServiceUid}",
                        headers=bearer_token_headers,
                        data=payload,
                        )

if order_response.status_code == 200:

    port_service_details = order_response.json()
    # location_dictionary = json.loads(response.content)
    print("Port update order service details : ", port_service_details)

    # Add a timestamp
    timestamp_now = datetime.datetime.now()
    port_service_details['Port Update order timestamp'] = timestamp_now.strftime("%Y-%m-%d  %H-%M-%S")

    # Write the port service details to port_service_details.json
    write_service_details(port_service_details)

else:
   print(f'Failed to update, status code: {order_response.status_code}')
   print(f'Failed to update, details: {order_response.text}')







