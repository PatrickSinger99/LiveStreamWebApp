import json
import os
import time
import urllib3


def lambda_handler(event, context):

    # Get the state of the shelly plug. Returns "on" or "off"
    def get_state(uri, device_id, auth_key):
        try:
            http = urllib3.PoolManager()
            response = http.request('POST', uri + "/device/status", fields={"id": device_id, "auth_key": auth_key})

            print("Get state response:", response, response.data)
            print("Current light state:", json.loads(response.data)["data"]["device_status"]["switch:0"]["output"])

            # Returns False or True depending on if light is on
            return json.loads(response.data)["data"]["device_status"]["switch:0"]["output"]

        except Exception as e:
            print("ERROR:", e)

    # Toggle the smart plug on or off, depending on the current state
    def toggle_light(uri, device_id, auth_key):
        try:
            light_on = get_state(uri, device_id, auth_key)

            if light_on:
                command = "off"
            else:
                command = "on"

            time.sleep(2)

            http = urllib3.PoolManager()
            response = http.request('POST', uri + "/device/relay/control",
                                    fields={"id": device_id, "auth_key": auth_key, "channel": 0, "turn": command})

            print("Toggle light response:", response, response.data)

            return json.loads(response.data)

        except Exception as e:
            print("ERROR:", e)

    # Fix strig bug where the json body gets converted to a string when recieving a POST request
    recieved_passcode = eval(event["body"])["passcode"]

    # Before running the code, check if user entered the right passcode
    if os.environ["passcode"] == recieved_passcode:
        response = toggle_light(uri=os.environ['uri'], device_id=os.environ['device_id'],
                                auth_key=os.environ['auth_key'])
    else:
        response = json.dumps("Invalid passcode")

    return {
        'statusCode': 200,
        'body': response
    }
