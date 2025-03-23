import json
import requests
import datetime


# Function to read the config file
def read_config():
    with open('../../../config/config.json', 'r') as config_file:
        return json.load(config_file)

# Function to read the config file
def read_existing_vxc_service_details():
    with open('vxc_service_details.json', 'r') as existing_service_details_file:
        return json.load(existing_service_details_file)


# Function to write to the config file
def write_service_details(vxc_service_details):
    try:
        with open('updated_vxc_service_details.json', 'w') as vxc_service_detials_file:
            json.dump(vxc_service_details, vxc_service_detials_file, indent=4)
        print("Successfully wrote to updated_vxc_service_details.json")
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

current_vxc_detail = read_existing_vxc_service_details()
print("current_vxc_detail : ", current_vxc_detail)

technicalServiceUid = current_vxc_detail["data"][0]["vxcJTechnicalServiceUid"]
print("vxcJTechnicalServiceUid : ", technicalServiceUid)

name = current_vxc_detail["data"][0]["vxc"]["name"]
print("name : ", name)

costCentre = current_vxc_detail["data"][0]["costCentre"]
print("costCentre : ", costCentre)


####### Send VXC update details ###########
vxc_update_url = "https://api.megaport.com/v3/product/vxc/"


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
        # bEndVlan - A unique VLAN ID for this connection. Values can range from 2 to 4093. If this value is 0, the system allocates a valid VLAN.
        #
        # term - Set up a term for this VXC. Note that there are rules for terms. See VXC Terms below for more information.
        #
        # costCentre - A customer reference number to be included in billing information and invoices
        #
        # aEndProductUid - When moving a VXC, this is the new A-End for the connection.
        #
        # bEndProductUid - When moving a VXC, this is the new B-End for the connection.
        #
        # aVnicIndex - When moving a VXC for an MVE, this is the new A-End vNIC for the connection.
        #
        # bVnicIndex - When moving a VXC for an MVE, this is the new B-End vNIC for the connection.
        #
        # isApproved - Define whether the VXC is approved or rejected via the Megaport Marketplace. Set to true (Approved) or false (Rejected).
        # Note: Valid only if there is an order pending approval (either new marketplace request or speed change). If there are no orders pending approval and isApproved is sent in the request, the API will return an error.
        #
        # shutdown - Temporarily shut down and re-enable the VXC. Valid values are true (shut down) and false (enabled). If not provided, it defaults to false (enabled).

        "name": "Python API Test VXC 202503232210",
        "rateLimit": 100,

        "aEndVlan": 101,
        "bEndVlan": 202,

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

# validate order details and get price
order_response = requests.put(f"{vxc_update_url}/{technicalServiceUid}",
                        headers=bearer_token_headers,
                        data=payload,
                        )

if order_response.status_code == 200:

    vxc_service_details = order_response.json()
    print("VXC update order service details : ", vxc_service_details)

    # Add a timestamp
    timestamp_now = datetime.datetime.now()
    vxc_service_details['VXC Update order timestamp'] = timestamp_now.strftime("%Y-%m-%d  %H-%M-%S")

    # Write the VXC service details to vxc_service_details.json
    write_service_details(vxc_service_details)

else:
   print(f'Failed to update, status code: {order_response.status_code}')
   print(f'Failed to update, details: {order_response.text}')







