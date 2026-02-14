import urllib.request
import urllib.parse
import json
import base64
import sys

# Configuration
BASE_URL = "http://127.0.0.1:5000/api/v1"
EMAIL = "midoxp@gmail.com"
PASSWORD = "123456"

def login():
    """Simulate login to get token and user ID."""
    print(f"Logging in as {EMAIL}...")
    url = f"{BASE_URL}/auth/login"
    data = json.dumps({"email": EMAIL, "password": PASSWORD}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    
    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 200:
                response_body = response.read().decode('utf-8')
                data = json.loads(response_body)
                access_token = data.get('access_token')
                
                # Decode token to get user ID
                parts = access_token.split('.')
                # Add padding if needed
                padding = len(parts[1]) % 4
                if padding:
                    parts[1] += "=" * (4 - padding)
                
                payload = json.loads(base64.b64decode(parts[1]).decode('utf-8'))
                user_id = payload.get('sub') or payload.get('identity')
                
                print(f"Login successful. User ID: {user_id}")
                return access_token, user_id
            else:
                print(f"Login failed: {response.status}")
                return None, None
    except urllib.error.HTTPError as e:
        print(f"Login error: {e.code} - {e.read().decode('utf-8')}")
        return None, None
    except Exception as e:
        print(f"Login error: {e}")
        return None, None

def create_place(token, user_id):
    """Simulate creating a place via API."""
    print("Creating place...")
    
    url = f"{BASE_URL}/places"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    place_data = {
        "title": "Test Luxury Hotel via Python (Urllib)",
        "description": "A wonderful test hotel created to verify the admin API endpoint.",
        "price": 1200,
        "user_id": user_id,
        "latitude": 0,
        "longitude": 0,
        "status": "available"
    }

    data = json.dumps(place_data).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers)

    try:
        with urllib.request.urlopen(req) as response:
            if response.status == 201:
                print("Place created successfully!")
                response_body = response.read().decode('utf-8')
                print(f"Response: {json.dumps(json.loads(response_body), indent=2)}")
                return True
            else:
                print(f"Create place failed: {response.status}")
                return False
    except urllib.error.HTTPError as e:
        print(f"Create place error: {e.code} - {e.read().decode('utf-8')}")
        return False
    except Exception as e:
        print(f"Create place error: {e}")
        return False

if __name__ == "__main__":
    token, user_id = login()
    if token and user_id:
        create_place(token, user_id)
