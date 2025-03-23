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
        with open('Megaport_Internet_VXC_Updated_details.json', 'w') as service_detials_json_file:
            json.dump(response_json, service_detials_json_file, indent=4)
        print("Successfully wrote response details to", service_detials_json_file)
    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")
    except TypeError as e:
        print(f"The data is not JSON serializable: {e}")

# Read the existing config file for current access token
config = read_config()
access_token = config['access_token']

# Carry current access token in request header
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


####### PUT request details ###########


#information for Port ordering
payload = json.dumps(
    {
        #
        # The changes are defined in the Body of the request.
        # Only include the parameters that you want to update.
        # For a VXC, you can update the following parameters:
        #
        # name - Customer name for the connection - this name appears in the Portal.
        #
        # rateLimit - A new speed for the connection.
        #
        # aEndVlan - A unique VLAN ID for this connection. Values can range from 2 to 4093. If this value is 0, the system allocates a valid VLAN.
        #
       #
        # term - Set up a term for this VXC. Note that there are rules for terms. See VXC Terms below for more information.
        #
        # costCentre - A customer reference number to be included in billing information and invoices
        #
        # aEndProductUid - When moving a VXC, this is the new A-End for the connection.
        #
        # aVnicIndex - When moving a VXC for an MVE, this is the new A-End vNIC for the connection.
        #
        # isApproved - Define whether the VXC is approved or rejected via the Megaport Marketplace. Set to true (Approved) or false (Rejected).
        # Note: Valid only if there is an order pending approval (either new marketplace request or speed change). If there are no orders pending approval and isApproved is sent in the request, the API will return an error.
        #
        # shutdown - Temporarily shut down and re-enable the VXC. Valid values are true (shut down) and false (enabled). If not provided, it defaults to false (enabled).

        "name": "API Example Megaport Internet Connection Updated 202503241015",
        "rateLimit": 521,

        "aEndVlan": 333,

        # "term": 12,
        # The minimum number of months in the committed term. Specify 1, 12, 24, or 36.
        # If term is not provided when ordering a VXC, it defaults to 1 (No Minimum Term).

        # "promoCode": "promox3mnthfree2",
        # (Optional) A promotional code to apply to the VXC order.
        # The code must be active and valid for the selected product.

        "shutdown": True,
        # shutdown will temporarily shut down and re-enable the VXC.
        # Valid values are true (shut down) and false (enabled). If not provided, it defaults to false (enabled).

        "market": "AU",

        "costCentre": "Optional finance reference"
        # (Optional) A finance reference to be used for billing purposes, such as a purchase order number.
    }
)

put_request_url = f"https://api.megaport.com/v3/product/vxc/{technicalServiceUid}"


put_response = requests.put(f"{put_request_url}",
                        headers=bearer_token_headers,
                        data=payload,
                        )

if put_response.status_code == 200:

    response_json = put_response.json()
    print("PUT response json details : ", response_json)

    # Add a timestamp
    timestamp_now = datetime.datetime.now()
    response_json['Response timestamp'] = timestamp_now.strftime("%Y-%m-%d  %H-%M-%S")

    # Write the response json details to .json
    write_response_details(response_json)

else:
   print(f'Failed to PUT request, status code: {post_response.status_code}')
   print(f'Details: {post_response.text}')







