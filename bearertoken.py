import requests


def get_api_key():
    api_key = "wTwjLTVdWNmtJMiuiZriH1fSSYCK5XnlNXR1mVjFvMIe"  # Replace with your actual API key
    token_url = "https://iam.cloud.ibm.com/identity/token"
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": api_key
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(token_url, headers=headers, data=data)
    bearer_token = response.json().get("access_token")

    if not bearer_token:
        raise Exception("Unable to get access token: " + str(response.text))

    print("Bearer Token:", bearer_token)
    return bearer_token