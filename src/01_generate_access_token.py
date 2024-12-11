import json
import datetime

import requests
from requests.auth import HTTPBasicAuth

# Function to read the config file
def read_config():
    with open('../config/config.json', 'r') as config_file:
        return json.load(config_file)

# Function to write to the config file
def write_config(config):
    with open('../config/config.json', 'w') as config_file:
        json.dump(config, config_file, indent=4)

# Read the existing config
config = read_config()

# export API_Key and API_Key_Secret from config file
API_Key = config['API_Key']
API_Key_Secret = config['API_Key_Secret']


####### Get Access Token ###########
token_url = "https://auth-m2m.megaport.com/oauth2/token"

headers = {'Content-Type': 'application/x-www-form-urlencoded'}
payload = {'grant_type': 'client_credentials'}

response = requests.request("POST", token_url, auth=HTTPBasicAuth(API_Key, API_Key_Secret), headers=headers, data=payload)


if response.status_code == 200:

   access_token = response.json()['access_token']

   # Add or update a value
   config['access_token'] = access_token
   timestamp_now = datetime.datetime.now()
   config['token_timestamp'] = timestamp_now.strftime("%Y-%m-%d  %H-%M-%S")

   # Write the updated config back to the file
   write_config(config)

else:
   print(f'Failed to get token, status code: {response.status_code}')




