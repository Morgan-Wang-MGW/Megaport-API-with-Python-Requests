import json
import requests

# Function to read the config file
def read_config():
    with open('../../config/config.json', 'r') as config_file:
        return json.load(config_file)

# Function to write to the IX location dictionary file
def write_locations(ix_location_dictionary):
    try:
        with open('ix_location_dictionary.json', 'w') as ix_location_file:
            json.dump(ix_location_dictionary, ix_location_file, indent=4)
        print("Successfully wrote locations to ix_location_dictionary.json")
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

####### Get IX Location ###########
ixlocationid = "4"
# Location identifier. (Required - integer)

location_url = f"https://api.megaport.com/v2/product/ix/types?locationId={ixlocationid}"

response = requests.get(location_url, headers=bearer_token_headers)

if response.status_code == 200:

    print('Successfully get IX location dictionary')
    ix_location_dictionary = response.json()
    # Write the IX location data to json file
    write_locations(ix_location_dictionary)

else:
   print(f'Failed to get IX location dictionary, status code: {response.status_code}')




