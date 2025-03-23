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
        with open('service_key_generation_details.json', 'w') as service_detials_json_file:
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

post_request_url = "https://api.megaport.com/v2/service/key"


#request payload information
payload = json.dumps(
  {
      "productUid": "012fb924-cd54-4a9e-8812-d05f27be420b",
      "description": "API Service Key - Single Use",
      "active": True,
      "_set_singleUse_to_false_to_make_service_key_multiUse": True,
      "singleUse": True,
      "maxSpeed": "500",
      "preApproved": True,
      "vlan": 3,
      # "validFor": {
      #     "_make_start_timestamp_equal_to_now": 1742767526295,
      #     "start": 1742767526295,
      #     "_make_end_timestamp_equal_to_1_month_forward": 1745363099065,
      #     "end": 1745363099065
      # }

  }
)

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







