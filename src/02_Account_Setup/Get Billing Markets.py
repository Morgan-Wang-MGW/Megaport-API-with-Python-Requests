import json

import requests

# Function to read the config file
def read_config():
    with open('../../config/config.json', 'r') as config_file:
        return json.load(config_file)

# Function to write to the billing markets file
def write_billing_market(billing_market):
    try:
        with open('billing_market.json', 'w') as billing_market_file:
            json.dump(billing_market, billing_market_file, indent=4)
        print("Successfully wrote billing market to billing_market.json")
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


request_url = "https://api.megaport.com/v2/market"

payload = {'grant_type': 'client_credentials'}

response = requests.request("GET", request_url, headers=bearer_token_headers, data=payload)


if response.status_code == 200:

   #Read json from response
   billing_market = response.json()

   # Write the data to json file
   write_billing_market(billing_market)


else:
   print(f'Failed to get Billing Markets, status code: {response.status_code}')




