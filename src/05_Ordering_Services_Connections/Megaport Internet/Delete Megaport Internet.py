import json
import requests
import datetime


# Function to read the config file
def read_config():
    with open('../../../config/config.json', 'r') as config_file:
        return json.load(config_file)

# Function to read the config file
def read_existing_service_details():
    with open('Megaport_Internet_VXC_details.json', 'r') as existing_service_details_file:
        return json.load(existing_service_details_file)

# Function to write to the config file
def write_response_details(response_json):
    try:
        with open('Megaport_Internet_VXC_Deleted_details.json', 'w') as service_detials_json_file:
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


current_service_detail = read_existing_service_details()
print("current_service_detail : ", current_service_detail)

technicalServiceUid = current_service_detail["data"][0]["vxcJTechnicalServiceUid"]
print("vxcJTechnicalServiceUid : ", technicalServiceUid)

name = current_service_detail["data"][0]["vxc"]["name"]
print("name : ", name)


####### details for post request ###########

payload = json.dumps(
  {

    "cancellation_reason": "OTHER",
      # (Optional) The reason for deleting the service.
      # These options are available:
      # MOVED_TO_CLOUD_NATIVE_SOL
      # SERVICE_MOVED
      # SERVICE_ORDERED_IN_ERROR
      # PROOF_OF_CONCEPT
      # PROJECT_ENDED
      # SWITCHING_PROVIDER
      # PRICING
      # PRODUCT_PERFORMANCE
      # OTHER

    "cancellation_comment": "Service Ordered for API validations only",
      # Specify free text (max. 400 characters) with an additional explanation for the reason the service was terminated.

  }
)


post_request_url = f"https://api.megaport.com/v3/product/{technicalServiceUid}/action/CANCEL_NOW"

# validate order details and get price
post_response = requests.post(f"{post_request_url}",
                        headers=bearer_token_headers,
                        data=payload,
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







