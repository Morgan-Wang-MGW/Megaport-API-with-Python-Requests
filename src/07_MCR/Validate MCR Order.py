import json
import requests
import datetime


# Function to read the config file
def read_config():
    with open('../../config/config.json', 'r') as config_file:
        return json.load(config_file)

# Function to write to the config file
def write_response_details(response_json):
    try:
        with open('MCR_validate_details.json', 'w') as service_detials_json_file:
            json.dump(response_json, service_detials_json_file, indent=4)
        print("Successfully wrote response details to", service_detials_json_file)
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


####### details for post request ###########

#information for Port ordering
payload = json.dumps([
  {

      "locationId": 4,
      # The ID of the data center where you are requesting the MCR. This value is from the response returned by the locations endpoint.

      "term": 24,
      # The minimum number of months in the committed term. Specify 1, 12, 24, or 36.

      "productName": "Python API Test MCR",
      # A descriptive name for the Port.

      "productType": "MCR2",
      # Specify MCR2 for MCR.

      "portSpeed": 1000,
      # Speed for the MCR.
      # Specify 1000, 2500, 5000, or 10000 Mbps (1 Gbps, 2.5 Gbps, 5 Gbps and 10 Gbps).
      # Note: High speed MCR 25 Gbps, 50 Gbps and 100 Gbps are not available in all locations.


      "config": {
          "diversityZone": "red",
          # (Optional) Specify blue or red to indicate the diversity zone for the Port.
          # (Not all locations support diversity zones - the locations endpoint indicates available diversity zones and Port speeds for each location.)

          "mcrAsn": 133937
      },

      "market": "AU",

      "costCentre": "Optional finance reference"
      #(Optional) A finance reference to be used for billing purposes, such as a purchase order number.
  }
])


post_request_url = "https://api.megaport.com/v3/networkdesign/validate"


# validate order details and get price
post_response = requests.post(f"{post_request_url}",
                        headers=bearer_token_headers,
                        data=payload,
                        )

if post_response.status_code == 200:

    response_json = post_response.json()
    print("post response json details : ", response_json)

    # Add a timestamp
    timestamp_now = datetime.datetime.now()
    response_json['Response timestamp'] = timestamp_now.strftime("%Y-%m-%d  %H-%M-%S")

    # Write the response json details to .json
    write_response_details(response_json)

else:
   print(f'Failed to post request, status code: {post_response.status_code}')
   print(f'Details: {post_response.text}')







