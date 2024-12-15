import json
import requests

# Function to read the config file
def read_config():
    with open('../../config/config.json', 'r') as config_file:
        return json.load(config_file)

# Function to write to the location dictionary file
def write_locations(location_dictionary):
    try:
        with open('location_dictionary.json', 'w') as location_file:
            json.dump(location_dictionary, location_file, indent=4)
        print("Successfully wrote locations to location_dictionary.json")
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

####### Get Location ###########
status = "Active"
metro = "Melbourne"
location_url = f"https://api.megaport.com/v2/locations?locationStatuses={status}&metro={metro}"

response = requests.get(location_url, headers=bearer_token_headers, verify=False)

if response.status_code == 200:

    print('Successfully get location dictionary')
    location_dictionary = response.json()
    # Write the location data to json file
    write_locations(location_dictionary)

else:
   print(f'Failed to get location dictionary, status code: {response.status_code}')




