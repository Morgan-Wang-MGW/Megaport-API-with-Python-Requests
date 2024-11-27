import json
import requests
from requests.auth import HTTPBasicAuth

# Function to read the config file
def read_config():
    with open('config.json', 'r') as config_file:
        return json.load(config_file)

# Function to write to the config file
def write_config(config):
    with open('config.json', 'w') as config_file:
        json.dump(config, config_file, indent=4)

# Read the existing config
config = read_config()

# export API_Key and API_Key_Secret from config file
API_Key = config['API_Key']
API_Key_Secret = config['API_Key_Secret']


print(f"API Key: {API_Key}")
print(f"API Key Secret: {API_Key_Secret}")

####### Get Access Token ###########
# token_url = "https://oauth-m2m.auth.ap-southeast-2.amazoncognito.com/oauth2/token"
token_url = "https://auth-m2m.megaport.com/oauth2/token"
requests.packages.urllib3.disable_warnings()

headers = {'Content-Type': 'application/x-www-form-urlencoded'}
payload = {'grant_type': 'client_credentials'}

# response = requests.post(token_url, auth=HTTPBasicAuth(API_Key, API_Key_Secret), headers={'Content-Type': 'application/x-www-form-urlencoded'}, data={'grant_type': 'client_credentials'})
# response = requests.post(token_url, auth=HTTPBasicAuth(API_Key, API_Key_Secret), headers={'Content-Type': 'application/x-www-form-urlencoded'}, data={'grant_type': 'client_credentials'}, verify=False)
response = requests.request("POST", token_url, auth=HTTPBasicAuth(API_Key, API_Key_Secret), headers=headers, data=payload)


print("megaport_staging_GenAccessToken(): HtmlResponse.status_code = ", response.status_code)


if response.status_code == 200:

   access_token = response.json()['access_token']
   print(f"Get JWT token: {access_token}")

   # Add or update a value
   config['access_token'] = access_token

   # Write the updated config back to the file
   write_config(config)

else:
   print(f'Failed to get token, status code: {response.status_code}')




