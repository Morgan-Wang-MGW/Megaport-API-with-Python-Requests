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
        with open('MCR_VXC_Purchase_details.json', 'w') as service_detials_json_file:
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

#information for MCR VXC validate

payload = json.dumps([
  {
    "productUid": "c3648842-9b3b-43a2-b956-7b1d2581f804",
    # This productUid identifies the MCR in your Megaport location (A-End)
    # The bEnd: productUid identifies one of the four destination types: ports, CSPs, Marketplace, or IX.
    "associatedVxcs": [
      {
        "rateLimit": 500,
        # The rateLimit can be one of these preset values (in Mbps):
        # 50, 100, 200, 300, 400, 500, 1000, 2000, 5000, 10000

        "productName": "Test Connection 202503241700",

        "term": 1,
        # The minimum number of months in the committed term. Specify 1, 12, 24, or 36.
        # If term is not provided when ordering a VXC, it defaults to 1 (No Minimum Term).

        "shutdown": False,
        # shutdown will temporarily shut down and re-enable the VXC.
        # Valid values are true (shut down) and false (enabled). If not provided, it defaults to false (enabled).

        "productType": "VXC",

        "connectType": "VROUTER",

        "aEnd" : {
          "partnerConfig": {
            "connectType": "VROUTER",
            "interfaces": [
              {
                "vlan": None,
                "ipAddresses": [
                  "10.191.1.25/29"
                ],
                "bgpConnections": [
                  {
                    "peerAsn": "133937",
                    "localIpAddress": "10.191.1.25",
                    "peerIpAddress": "10.191.1.26",
                    "password": "",
                    "localAsn": 133937,
                    "shutdown": False,
                    "description": "BGP with MED and BFD enabled",
                    "medIn": 100,
                    "medOut": 100,
                    "bfdEnabled": True,
                    "txInterval": None,
                    "rxInterval": None,
                    "multiplier": None,
                    "importWhitelist": None,
                    "importBlacklist": None,
                    "exportWhitelist": None,
                    "exportBlacklist": None,
                    "exportPolicy": None,
                    "denyExportTo": [],
                    "permitExportTo": []
                  },
                  # {
                  #   "peerAsn": "62511",
                  #   "localIpAddress": "10.191.0.25",
                  #   "peerIpAddress": "10.191.0.27",
                  #   "password": "cnn23049asdkfj",
                  #   "localAsn": 133937,
                  #   "shutdown": False,
                  #   "description": "BGP without MED or BFD",
                  #   "medIn": None,
                  #   "medOut": None,
                  #   "bfdEnabled": False,
                  #   "txInterval": None,
                  #   "rxInterval": None,
                  #   "multiplier": None,
                  #   "importWhitelist": None,
                  #   "importBlacklist": None,
                  #   "exportWhitelist": None,
                  #   "exportBlacklist": None,
                  #   "exportPolicy": None,
                  #   "denyExportTo": [],
                  #   "permitExportTo": []
                  # }
                ],
                "ipRoutes": [
                  # {
                  #   "description": "test static route 1",
                  #   "nextHop": "10.191.0.26",
                  #   "prefix": "10.0.0.0/24"
                  # }
                ],
                "natIpAddresses": []
              }
            ]
          }
        },
        "bEnd": {
          "productUid": "c58328d4-5c9b-4b22-a53e-07da256271a1",
          # The bEnd: productUid identifies one of the four destination types: ports, CSPs, Marketplace, or IX.

          "partnerConfig": {
            "connectType": "VROUTER",
            "interfaces": [
              {
                "vlan": None,
                "ipAddresses": [
                  "10.191.1.26/29"
                ],
                "bgpConnections": [
                  {
                    "peerAsn": "133937",
                    "localIpAddress": "10.191.1.26",
                    "peerIpAddress": "10.191.1.25",
                    "password": "",
                    "localAsn": 133937,
                    "shutdown": False,
                    "description": "BGP with MED and BFD enabled",
                    "medIn": 100,
                    "medOut": 100,
                    "bfdEnabled": True,
                    "txInterval": None,
                    "rxInterval": None,
                    "multiplier": None,
                    "importWhitelist": None,
                    "importBlacklist": None,
                    "exportWhitelist": None,
                    "exportBlacklist": None,
                    "exportPolicy": None,
                    "denyExportTo": [],
                    "permitExportTo": []
                  },
                  # {
                  #   "peerAsn": "62511",
                  #   "localIpAddress": "10.191.0.25",
                  #   "peerIpAddress": "10.191.0.27",
                  #   "password": "cnn23049asdkfj",
                  #   "localAsn": 133937,
                  #   "shutdown": False,
                  #   "description": "BGP without MED or BFD",
                  #   "medIn": None,
                  #   "medOut": None,
                  #   "bfdEnabled": False,
                  #   "txInterval": None,
                  #   "rxInterval": None,
                  #   "multiplier": None,
                  #   "importWhitelist": None,
                  #   "importBlacklist": None,
                  #   "exportWhitelist": None,
                  #   "exportBlacklist": None,
                  #   "exportPolicy": None,
                  #   "denyExportTo": [],
                  #   "permitExportTo": []
                  # }
                ],
                "ipRoutes": [
                  # {
                  #   "description": "test static route 1",
                  #   "nextHop": "10.191.0.26",
                  #   "prefix": "10.0.0.0/24"
                  # }
                ],
                "natIpAddresses": []
              }
            ]
          }
        },

      }
    ]
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







