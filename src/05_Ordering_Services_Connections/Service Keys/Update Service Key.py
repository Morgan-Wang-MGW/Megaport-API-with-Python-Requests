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
        with open('updated_service_key_details.json', 'w') as service_detials_json_file:
            json.dump(response_json, service_detials_json_file, indent=4)
        print("Successfully wrote response details to", service_detials_json_file)
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


####### details for PUT request ###########

put_request_url = "https://api.megaport.com/v2/service/key"


#request payload information

payload = json.dumps({
  "description": "API Service Key Update - Multi Use",
  "key": "e5f164c0-9d6b-4e2d-b558-9cfa4ed5cf99",
  "productId": 234815,
  "singleUse": False,
  "active": True,
  "maxSpeed": "500",
  "validFor": {
      "start": 1742767526295,
      "end": 1745364099065
  }
})

# send PUT request
put_response = requests.put(f"{put_request_url}",
                        headers=bearer_token_headers,
                        data=payload,
                        )

if put_response.status_code == 200:

    response_json = put_response.json()
    print("put response json details : ", response_json)

    # Add a timestamp
    timestamp_now = datetime.datetime.now()
    response_json['Response timestamp'] = timestamp_now.strftime("%Y-%m-%d  %H-%M-%S")

    # Write the response json details to .json
    write_response_details(response_json)

else:
   print(f'Failed to put request, status code: {put_response.status_code}')
   print(f'Details: {put_response.text}')







