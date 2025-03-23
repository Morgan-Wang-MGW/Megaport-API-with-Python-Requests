import json
import requests
import datetime


# Function to read the config file
def read_config():
    with open('../../../config/config.json', 'r') as config_file:
        return json.load(config_file)

# Function to write to the config file
def write_response_details(response_json):
    try:
        with open('vxc_details_created_by_service_key.json', 'w') as service_detials_json_file:
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
post_request_url = "https://api.megaport.com/v3/networkdesign/buy"


#request payload information

payload = json.dumps([
  {
    "productUid": "a3cb9e0c-edcb-4d2d-9743-b0ea84610486",
      # your A-End Access service product UID. This value is from the response returned by the /products endpoint.

    "associatedVxcs": [
      {
        "productName": "VXC created by API with Service key 02",
        "rateLimit": 100,
        "serviceKey": "d9ce6b4b-9e76-4e4d-b904-43bf2630a064",
          # The service key UID that you want to associate with the VXC.
        "aEnd": {
          "vlan": 0
        },
          # The VLAN ID for the A-End of the VXC.
        "bEnd": {
          "productUid": "012fb924-cd54-4a9e-8812-d05f27be420b"
        }
      }
    ]
  }
])

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







