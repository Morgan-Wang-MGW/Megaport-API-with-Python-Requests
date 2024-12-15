import json
import requests

# Function to read the config file
def read_config():
    with open('../../config/config.json', 'r') as config_file:
        return json.load(config_file)

# Function to write to the partner megaport dictionary file
def write_locations(partner_megaport_dictionary):
    try:
        with open('partner_megaport_dictionary.json', 'w') as partner_megaport_file:
            json.dump(partner_megaport_dictionary, partner_megaport_file, indent=4)
        print("Successfully wrote partner megaport to partner_megaport_dictionary.json")
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

####### Get Partner Megaport ###########
connectType = "AZURE"
# Filters the locations based on the cloud providers,
# such as AWS (for Hosted VIF), AWSHC (for Hosted Connection), AZURE, GOOGLE, ORACLE, OUTSCALE, and IBM.
# Use connectType=TRANSIT to display Ports that support a Megaport Internet connection.
# Use connectType=FRANCEIX to display Ports that you can create a VXC to in order to connect to France-IX.

vxcPermitted = "true" #boolean value true or false

partner_url = f"https://api.megaport.com/v2/dropdowns/partner/megaports?connectType={connectType}&vxcPermitted={vxcPermitted}"

response = requests.get(partner_url, headers=bearer_token_headers, verify=False)

if response.status_code == 200:

    print('Successfully get partner megaport dictionary')
    partner_megaport_dictionary = response.json()
    # Write the partner megaport data to json file
    write_locations(partner_megaport_dictionary)

else:
   print(f'Failed to get partner megaport dictionary, status code: {response.status_code}')




