import requests

headers = {"Content-Type": "application/json"}
#generate access token
def get_token(username, passwd, fqdn):
    generate_url = f"https://{fqdn}/auth/generate/token"
    generate_payload = {
        "username": username,
        "password": passwd,
        "returnSecureToken": True
    }

    response = requests.post(generate_url, json=generate_payload, headers=headers)
    response.raise_for_status()

    data = response.json()
    assert data.get("message") == "Authentication successful", "Auth message mismatch"
    assert "success" in data, "'success' field missing in response"
    assert "token" in data, "'token' field missing in response"

    access_token = data["token"]
    print(f"Access Token: {access_token}")

    return access_token

#verify token
def verify_token(username, passwd, fqdn):
    access_token = get_token(username, passwd, fqdn)
    verify_url = f"https://{fqdn}/auth/verify"
    verify_payload = {
        "token": access_token
    }

    verify_response = requests.post(verify_url, json=verify_payload, headers=headers)
    verify_response.raise_for_status()

    verify_data = verify_response.json()
    assert verify_data.get("message") == "verification successful", "Verification message mismatch"
    assert "token" in verify_data, "'token' field missing in verification response"

    jwt_token = verify_data["token"]
    print(f"JWT Token: {jwt_token}")

    return jwt_token
