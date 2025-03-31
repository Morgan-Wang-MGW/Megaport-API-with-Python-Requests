import json
import requests
import datetime


# Function to read the config file
def read_config():
    with open('../../config/config.json', 'r') as config_file:
        return json.load(config_file)

# Function to write to the config file
def write_response_details(response_json):
    try:
        with open('6Wind_MVE_order_details.json', 'w') as service_detials_json_file:
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


####### details for post request ###########

#information for Port ordering
payload = json.dumps([

{

      "vendorConfig": {

          "vendor": "6WIND",
          "imageId": 75,
          "product_size": "SMALL",
          "mveLabel": "MVE 8/32",
          "product" : "VSR",
          "sshPublicKey": "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCx6le2XvFheQvC7fNX0kkpSi1rjGbRmepPrjibJp9EcClMEDkDo26Uew4VB6a2DlTJpLtXloq7wpFkfQcWHSlAfahhUZ5ARGELPPi1lDkCaVt+ffVWrRyUZTjn3ilZ/5a08y5zBUsW3e+LlHIesBFHXePuXzZZaF5HaPAhRBEC4xszdwv93my9GeCBI4Ixx3D3MMJkn2ikjdsazohP/R1E3wmp63kzHicXazBx19iF0d18ymRt8DzOPOtA0MKTdNGMZSyMFJrGCJ4QSWPqB3Y2fU53a5zoYwZ5zEK82m/ziCepUucVHkAQM/H3ON/96FJ8ayW36HDwuGG1oafTF8m7 morganwang@DQNQDYQJT4",
      },


      "locationId": 4,
      # The ID of the data center where you are requesting the MCR. This value is from the response returned by the locations endpoint.

      "term": 1,
      # The minimum number of months in the committed term. Specify 1, 12, 24, or 36.

      "productName": "Python API Test MVE  20250331",
      # A descriptive name for the Port.

      "productType": "MVE",
      "config": {
          "diversityZone": "red"
      },
      "vnics": [
          {
              "description": "Control Plane 1"
          },
          {
              "description": "vNIC 3"
          },
          {
              "description": "vNIC 3"
          },
          {
              "description": "vNIC 4"
          },
          {
              "description": None
          }
      ],



      "market": "AU",

      "costCentre": "Optional finance reference"
      #(Optional) A finance reference to be used for billing purposes, such as a purchase order number.
  }
])


post_request_url = "https://api.megaport.com/v3/networkdesign/buy"


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







