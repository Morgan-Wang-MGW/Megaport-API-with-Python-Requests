import json
import requests
import datetime


# Function to read the config file
def read_config():
    with open('../../config/config.json', 'r') as config_file:
        return json.load(config_file)

# Function to read the config file
def read_existing_mve_service_details():
    with open('6Wind_MVE_order_details.json', 'r') as existing_mve_service_details_file:
        return json.load(existing_mve_service_details_file)

# Function to write to the config file
def write_response_details(response_json):
    try:
        with open('6Wind_MVE_delete_results.json', 'w') as service_detials_json_file:
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



current_mve_detail = read_existing_mve_service_details()
print("current_mve_detail : ", current_mve_detail)

technicalServiceUid = current_mve_detail["data"][0]["technicalServiceUid"]
print("technicalServiceUid : ", technicalServiceUid)

name = current_mve_detail["data"][0]["name"]
print("MVE name : ", name)

action = "CANCEL_NOW"
# The action is a required string that indicates the change in the service. Accepted values are:
# CANCEL - Cancels service on a Port at the end of the contract term. You can restore the Port before the contract ends.
# UN_CANCEL - Restores a Port that has been canceled but not reached the end of the contract term.
# CANCEL_NOW - Stops the service on the Port immediately. You will still be billed for the remainder of your contract and early termination fees apply. The Port cannot be restored.
#

post_request_url = f"https://api.megaport.com/v3/product/{technicalServiceUid}/action/{action}"

print("post_request_url : ", post_request_url)
# post_request_url = "https://api.megaport.com/v2/product/mcr2/63ecb1b1-0433-4e17-add8-5bf4ad91dfff/prefixList"

# validate order details and get price
post_response = requests.post(f"{post_request_url}",
                        headers=bearer_token_headers,
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







