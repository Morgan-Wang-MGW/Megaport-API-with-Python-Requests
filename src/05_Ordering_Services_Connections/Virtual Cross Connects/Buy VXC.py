import json
import requests
import datetime


# Function to read the config file
def read_config():
    with open('../../../config/config.json', 'r') as config_file:
        return json.load(config_file)

# Function to write to the config file
def write_service_details(vxc_service_details):
    try:
        with open('vxc_service_details.json', 'w') as vxc_service_detials_file:
            json.dump(vxc_service_details, vxc_service_detials_file, indent=4)
        print("Successfully wrote to vxc_service_details.json")
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


####### Send VXC order details for validate ###########

vxc_order_url = "https://api.megaport.com/v3/networkdesign"


#information for Port ordering
payload = json.dumps([
  {
      "productUid": "012fb924-cd54-4a9e-8812-d05f27be420b",
      # A-End Access service product UID. This value is from the response returned by the /products endpoint.

      "associatedVxcs": [
          {
              "productName": "Python API Test VXC 202503232205",
              "rateLimit": 500,
              "aEnd": {
                  "vlan": 2001
              },
              "bEnd": {
                  "productUid": "a3cb9e0c-edcb-4d2d-9743-b0ea84610486",
                  "vlan": 2002
              }
          }
      ],

      "term": 24,
      # The minimum number of months in the committed term. Specify 1, 12, 24, or 36.
      # If term is not provided when ordering a VXC, it defaults to 1 (No Minimum Term).

      #"promoCode": "promox3mnthfree2",
      # (Optional) A promotional code to apply to the VXC order.
      # The code must be active and valid for the selected product.

      "shutdown": False,
      # shutdown will temporarily shut down and re-enable the VXC.
      # Valid values are true (shut down) and false (enabled). If not provided, it defaults to false (enabled).

      "market": "AU",

      "costCentre": "Optional finance reference"
      #(Optional) A finance reference to be used for billing purposes, such as a purchase order number.
  }
])

# validate order details and get price
order_response = requests.post(f"{vxc_order_url}/buy",
                        headers=bearer_token_headers,
                        data=payload,
                        )

if order_response.status_code == 200:

    vxc_service_details = order_response.json()
    print("VXC order service details : ", vxc_service_details)

    # Add a timestamp
    timestamp_now = datetime.datetime.now()
    vxc_service_details['VXC order timestamp'] = timestamp_now.strftime("%Y-%m-%d  %H-%M-%S")

    # Write the validate details to vxc_service_details.json
    write_service_details(vxc_service_details)

else:
   print(f'Failed to order, status code: {order_response.status_code}')







