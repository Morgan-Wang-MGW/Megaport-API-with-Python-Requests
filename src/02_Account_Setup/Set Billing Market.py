import json
import requests

# Function to read the config file
def read_config():
    with open('../../config/config.json', 'r') as config_file:
        return json.load(config_file)

# Read the existing config
config = read_config()

access_token = config['access_token']

request_url = "https://api.megaport.com/v2/market"

bearer_token_headers = {
   'Content-Type': 'application/json',
   'Authorization': f'Bearer {access_token}'
}

payload = json.dumps({
  "currencyEnum": "AUD",
  "language": "en",
  "billingContactName": "Market Contact",
  "billingContactPhone": "+61 7 12341234",
  "billingContactEmail": "support@megaport.com",
  "address1": "825 Ann Street",
  "address2": None,
  "city": "Fortitude Valley",
  "state": "QLD",
  "postcode": "4006",
  "country": "AU",
  "firstPartyId": 808
})


response = requests.request("POST", request_url, headers=bearer_token_headers, data=payload)


if response.status_code == 200:

   print(f'Successfully set Billing Market')

else:
   print(f'Failed to set Billing Markets, status code: {response.status_code}')




