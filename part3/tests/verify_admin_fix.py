import json
import sys
import urllib.error
import urllib.request
import uuid

BASE_URL = "http://127.0.0.1:5000/api/v1"


def test_admin_creation_vulnerability():
    print("Testing admin creation vulnerability...")

    email = f"hacker_{uuid.uuid4().hex[:8]}@test.com"
    payload = {
        "first_name": "Hacker",
        "last_name": "One",
        "email": email,
        "password": "password123",
        "is_admin": True,
    }

    req = urllib.request.Request(
        f"{BASE_URL}/users/",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )

    try:
        with urllib.request.urlopen(req) as response:
            if response.status != 201:
                print(f"[FAIL] Unexpected status: {response.status}")
                sys.exit(1)

            user_data = json.loads(response.read())
            user_id = user_data.get("id")
            is_admin = user_data.get("is_admin")

            print(f"User created: id={user_id}")
            print(f"is_admin in response: {is_admin}")

            if is_admin is True:
                print("[FAIL] User was created with admin privileges.")
                sys.exit(1)
            if is_admin is False:
                print("[PASS] Public registration cannot set is_admin.")
                return

            print(f"[WARN] is_admin missing or unexpected value: {is_admin}")
            sys.exit(1)

    except urllib.error.HTTPError as e:
        print(f"[FAIL] HTTP error: {e.code}")
        print(e.read().decode())
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"[FAIL] Could not connect to API: {e.reason}")
        sys.exit(1)


if __name__ == "__main__":
    test_admin_creation_vulnerability()
