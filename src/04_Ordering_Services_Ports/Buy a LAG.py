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
        with open('lag_service_details.json', 'w') as lag_service_detials_file:
            json.dump(port_service_details, lag_service_detials_file, indent=4)
        print("Successfully wrote locations to lag_service_details.json")
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


####### Send Port order details for Order ###########

port_order_url = "https://api.megaport.com/v3/networkdesign"


#information for Port ordering
payload = json.dumps([
  {
      "productName": "Python API Test LAG Port",
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

      "lagPortCount": 2,
      # for LAG orders, lagPortCount is required and indicates the number of Ports
      # you can configure single Port LAGs (for example “lagPortCount”:1)
      # all Ports in LAG must have the same speed
      # only 10 G and 100 G ports are supported.
      # maximum eight Ports per LAG (for example “lagPortCount”:8)

      "market": "AU",

      "costCentre": "Optional finance reference"
      #(Optional) A finance reference to be used for billing purposes, such as a purchase order number.
  }
])

# validate order details and get price
order_response = requests.post(f"{port_order_url}/buy",
                        headers=bearer_token_headers,
                        data=payload,
                        verify=False
                        )

if order_response.status_code == 200:

    port_service_details = order_response.json()
    # location_dictionary = json.loads(response.content)
    print("LAG order service details : ", port_service_details)

    # Add a timestamp
    timestamp_now = datetime.datetime.now()
    port_service_details['LAG order timestamp'] = timestamp_now.strftime("%Y-%m-%d  %H-%M-%S")

    # Write the port service details to port_service_details.json
    write_service_details(port_service_details)

else:
   print(f'Failed to order, status code: {order_response.status_code}')







