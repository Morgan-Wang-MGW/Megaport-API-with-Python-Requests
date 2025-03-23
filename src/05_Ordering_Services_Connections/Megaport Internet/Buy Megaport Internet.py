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
        with open('Megaport_Internet_VXC_details.json', 'w') as service_detials_json_file:
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

payload = json.dumps([
  {
    "productUid": "012fb924-cd54-4a9e-8812-d05f27be420b",
    # A-End Access service product UID. This value is from the response returned by the /products endpoint.

    "associatedVxcs": [
      {
        "rateLimit": 117,
        "term": 1,
        "productName": "API Example Megaport Internet Connection 202503241030",
        "aEnd": {
          "productName": "GB Megaport Internet Port"
        },
        "bEnd": {
          "productUid": "874dbcff-a1f9-4328-9c08-112cd87c20f6"
        },
        "productType": "VXC",
        "connectType": "TRANSIT"
      }
    ]
  }
])


post_request_url = "https://api.megaport.com/v3/networkdesign/buy"


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







