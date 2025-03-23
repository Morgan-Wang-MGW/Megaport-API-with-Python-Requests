import json
import requests

# Function to read the config file
def read_config():
    with open('../../../config/config.json', 'r') as config_file:
        return json.load(config_file)

# Function to write to the location dictionary file
def write_service_key(service_key_details):
    try:
        with open('service_key_details.json', 'w') as service_key_detail_file:
            json.dump(service_key_details, service_key_detail_file, indent=4)
        print("Successfully wrote service keys to service_key_details.json")
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

####### Get Service Keys ###########
#Uid of the product under which the service key is created
productIdOrUid = "012fb924-cd54-4a9e-8812-d05f27be420b"

#Service key value, optional, only if you want to get specific service key detail
keyValue = "d9ce6b4b-9e76-4e4d-b904-43bf2630a064"

# url to get specific service key detail under the product
list_service_key_url = f"https://api.megaport.com/v2/service/key?productIdOrUid={productIdOrUid}&key={keyValue}"

# url to get all service keys under the product
list_service_key_url = f"https://api.megaport.com/v2/service/key?productIdOrUid={productIdOrUid}"

response = requests.get(list_service_key_url, headers=bearer_token_headers)

if response.status_code == 200:

    print('Successfully get service keys')
    service_key_details = response.json()
    # Write the location data to json file
    write_service_key(service_key_details)

else:
   print(f'Failed to get service keys, status code: {response.status_code}')




