from flask import Flask, request, jsonify
import requests
import threading
from colorama import init, Fore

# Initialize colorama for colored output in terminal
init(autoreset=True)

# Define colors for output
red = Fore.RED
green = Fore.GREEN
white = Fore.WHITE
blue = Fore.BLUE
yellow = Fore.YELLOW
cyan = Fore.CYAN
background = white + green

# Initialize Flask app
app = Flask(__name__)

# Define the URL for the API request
url = 'https://login.microsoftonline.com/common/GetCredentialType?mkt=en-US'

# Define the payload template (without the username)
payload_template = {
    "isOtherIdpSupported": True,
    "checkPhones": False,
    "isRemoteNGCSupported": True,
    "isCookieBannerShown": False,
    "isFidoSupported": True,
    "country": "NG",
    "forceotclogin": False,
    "isExternalFederationDisallowed": False,
    "isRemoteConnectSupported": False,
    "federationFlags": 0,
    "isSignup": False,
    "flowToken": "AQABAAEAAAAtyolDObpQQ5VtlI4uGjEPmVTvB5eZTaL_xvRdNX8zoF_M9oCPfpR1_3-Wz9ETrDbl5ca9Avq0LYJkoyoMgY5LIhrw_zFYKZPKDynsKoHPZfgeKmWiIAs1DXbLOrj1FwddvGzTm1ABWqIWhpNkryjIGv9-pljgbUnhPWj9pTn9ffvUpp8V2MtaAhrj46pyDne0WQmgpo5yxrOcie6NRDmX-vIRN1MIuXjLJ27VP51D0OM2hEp1OD47P6dtU6fk3-n2oCqUh1nP1tJCP1Pr47Uw2d3Hx3uCPYHHQJ8S3DkYwNqi4ieYGWQoRIaGrswGKuHiQRsyIuf8jtXEVXyOGqJhVIrV13orhsMe8QFdNAQE95yTcr7oSV6cXL7EWJdelszMsPUosCWSNdpwVI3lFGrKkYHetSaT2PrQem5AJIKBpKpvdLzk4q_P1P5_HA5hrOLCjH451cW4GJ2aVLL8wejgiEdppAzICHiHJOAthyGUP1R7w0z62wD6Ml9QOrRuqGS1KRxOCycJSUhLQcXDX5yIL1PCokaNJIAca5y1wkJb4zMbwhsGoVaUnWZK8XjTWYovsLqEn1dvUW_GrQxdQzwyIAA",
    "isAccessPassSupported": True,
}

# Define headers for the API request
headers = {
    "Host": "login.microsoftonline.com",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "close"
}

# Function to process email and check its validity
def process_email(email):
    # Create a copy of the payload template
    payload = payload_template.copy()
    # Set the username in the payload
    payload["username"] = email

    # Make the API request
    response = requests.post(url, json=payload, headers=headers)

    # Check if the response status code is 200
    if response.status_code == 200:
        # Parse the JSON response
        response_json = response.json()

        # Check if "IfExistsResult" is present in the response JSON
        if "IfExistsResult" in response_json:
            # Extract the value of "IfExistsResult"
            if_exists_result = response_json["IfExistsResult"]

            # Check the value of "IfExistsResult"
            if if_exists_result == 5 or if_exists_result == 0:
                return {"status": "valid", "email": email}
            else:
                return {"status": "invalid", "email": email}
        else:
            return {"status": "error", "message": "Invalid input"}
    else:
        return {"status": "error", "message": f"API request failed with status code {response.status_code}"}

# Define the route to receive POST requests
@app.route('/check-email', methods=['POST'])
def check_email():
    data = request.json
    if 'email' in data:
        email = data['email']
        result = process_email(email)
        return jsonify(result)
    else:
        return jsonify({"status": "error", "message": "Email not provided"}), 400

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True) 