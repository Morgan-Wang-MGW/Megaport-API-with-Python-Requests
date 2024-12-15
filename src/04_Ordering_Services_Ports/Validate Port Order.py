import json
import requests
import datetime


# Function to read the config file
def read_config():
    with open('../../config/config.json', 'r') as config_file:
        return json.load(config_file)

# Function to write to the config file
def write_service_details(port_service_details):
    try:
        with open('port_service_validate_details.json', 'w') as port_service_detials_file:
            json.dump(port_service_details, port_service_detials_file, indent=4)
        print("Successfully wrote locations to port_service_validate_details.json")
    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")
    except TypeError as e:
        print(f"The data is not JSON serializable: {e}")

# Read the existing config
config = read_config()

access_token = config['access_token']

bearer_token_headers = {
   'Content-Type': 'application/json',
   'Authorization': f'Bearer {access_token}'
}


####### Send Port order details for validate ###########

port_order_url = "https://api.megaport.com/v3/networkdesign"


#information for Port ordering
payload = json.dumps([
  {
      "productName": "Python API Test Port",
      # A descriptive name for the Port.

      "term": 24,
      # The minimum number of months in the committed term. Specify 1, 12, 24, or 36.

      "productType": "MEGAPORT",
      # Specify MEGAPORT for a physical port.

      "portSpeed": 10000,
      # Speed for the Port. Specify 1000, 10000, or 100000 Mbps (1 Gbps, 10 Gbps, or 100 Gbps). Note: 100 Gbps is not available in all locations.

      "locationId": 4,
      # The ID of the data center where you are requesting the Port. This value is from the response returned by the locations endpoint.

      "config": {
          "diversityZone": "red"
          # (Optional) Specify blue or red to indicate the diversity zone for the Port.
          # (Not all locations support diversity zones - the locations endpoint indicates available diversity zones and Port speeds for each location.)
      },

      "market": "US",

      "costCentre": "Optional finance reference"
      #(Optional) A finance reference to be used for billing purposes, such as a purchase order number.
  }
])

# validate order details and get price
validate_response = requests.post(f"{port_order_url}/validate",
                        headers=bearer_token_headers,
                        data=payload,
                        verify=False
                        )

if validate_response.status_code == 200:

    port_service_details = validate_response.json()
    print("Port order validate service details : ", port_service_details)

    # Add a timestamp
    timestamp_now = datetime.datetime.now()
    port_service_details['Port validate timestamp'] = timestamp_now.strftime("%Y-%m-%d  %H-%M-%S")

    # Write the validate details to port_service_validate_details.json
    write_service_details(port_service_details)

else:
   print(f'Failed to validate, status code: {validate_response.status_code}')







