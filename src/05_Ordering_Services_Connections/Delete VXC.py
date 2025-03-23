import json
import requests
import datetime


# Function to read the config file
def read_config():
    with open('../../config/config.json', 'r') as config_file:
        return json.load(config_file)

# Function to read the config file
def read_existing_vxc_service_details():
    with open('vxc_service_details.json', 'r') as existing_vxc_service_details_file:
        return json.load(existing_vxc_service_details_file)


# Read the existing config file for current access token
config = read_config()
access_token = config['access_token']

# Carry current access token in request header
bearer_token_headers = {
   'Content-Type': 'application/json',
   'Authorization': f'Bearer {access_token}'
}

current_vxc_detail = read_existing_vxc_service_details()
print("current_vxc_detail : ", current_vxc_detail)

technicalServiceUid = current_vxc_detail["data"][0]["vxcJTechnicalServiceUid"]
print("vxcJTechnicalServiceUid : ", technicalServiceUid)

technicalServiceId = current_vxc_detail["data"][0]["vxcJTechnicalServiceId"]
print("technicalServiceId : ", technicalServiceId)

name = current_vxc_detail["data"][0]["vxc"]["name"]
print("name : ", name)

costCentre = current_vxc_detail["data"][0]["costCentre"]
print("costCentre : ", costCentre)

first_part = technicalServiceUid.split('-')[0]
print("technicalServiceUid_first_part : ", first_part)


####### VXC delete Port request ###########
vxc_delete_url = "https://api.megaport.com/v3/product/"
# Full URL for Port cancellation is
# https://api.megaport.com/v3/product/{productUid}/action/{action}

action = "CANCEL_NOW"
# The action is a required string that indicates the change in the service. Accepted values are:
# CANCEL - Cancels service on a Port at the end of the contract term. You can restore the Port before the contract ends.
# UN_CANCEL - Restores a Port that has been canceled but not reached the end of the contract term.
# CANCEL_NOW - Stops the service on the Port immediately. You will still be billed for the remainder of your contract and early termination fees apply. The Port cannot be restored.
#
#information for Port ordering
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
      #Specify free text (max. 400 characters) with an additional explanation for the reason the service was terminated.

  }
)

# validate order details and get price
order_response = requests.post(f"{vxc_delete_url}/{technicalServiceUid}/action/{action}",
                        headers=bearer_token_headers,
                        data=payload,
                        )

if order_response.status_code == 200:

    print("VXC", first_part, "(" , technicalServiceId, ") name : ", name, "delete successfully!")


else:
    print("VXC", first_part, "(", technicalServiceId, ") name : ", name, "delete failed!")
    print(f'Status code: {order_response.status_code}')
    print(f'Details: {order_response.text}')







