import json
import sys
import urllib.error
import urllib.request
import uuid

BASE_URL = "http://127.0.0.1:5000/api/v1"
AUTH_URL = "http://127.0.0.1:5000/api/v1/auth/login"


def login(email, password):
    req = urllib.request.Request(
        AUTH_URL,
        data=json.dumps({"email": email, "password": password}).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read())["access_token"]


def create_user(email):
    payload = {
        "first_name": "Test",
        "last_name": "Phase3",
        "email": email,
        "password": "password123",
    }
    req = urllib.request.Request(
        f"{BASE_URL}/users/",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    try:
        urllib.request.urlopen(req)
    except Exception:
        pass


def test_phase3_flow():
    print("Testing Phase 3 flow (rich data + delete)...")

    user_email = f"test_p3_{uuid.uuid4().hex[:8]}@test.com"
    create_user(user_email)
    token = login(user_email, "password123")
    print(f"[PASS] Logged in as {user_email}")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",
    }

    print("[1] Creating place with rich data...")
    create_payload = {
        "title": "Rich Data Hotel",
        "description": "A hotel with many new fields",
        "price": 100.0,
        "latitude": 10.0,
        "longitude": 20.0,
        "number_of_rooms": 5,
        "max_guests": 10,
        "tagline": "Best hotel ever",
        "rules": "No smoking",
        "details": [{"title": "About", "text": "Details here"}],
    }

    place_id = None
    try:
        req = urllib.request.Request(
            f"{BASE_URL}/places/",
            data=json.dumps(create_payload).encode("utf-8"),
            headers=headers,
        )
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read())
            place_id = data["id"]
            if data.get("number_of_rooms") != 5 or data.get("tagline") != "Best hotel ever":
                print("[FAIL] Rich data fields mismatch on create.")
                print(data)
                sys.exit(1)
            print(f"[PASS] Created place id={place_id}")
    except Exception as e:
        print(f"[FAIL] Create failed: {e}")
        if hasattr(e, "read"):
            print(e.read().decode())
        sys.exit(1)

    print("[2] Updating place...")
    update_payload = {"tagline": "Updated Tagline", "max_guests": 20}
    try:
        req = urllib.request.Request(
            f"{BASE_URL}/places/{place_id}",
            data=json.dumps(update_payload).encode("utf-8"),
            headers=headers,
            method="PUT",
        )
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read())
            if data.get("tagline") != "Updated Tagline" or data.get("max_guests") != 20:
                print("[FAIL] Update mismatch.")
                sys.exit(1)
            print("[PASS] Place updated.")
    except Exception as e:
        print(f"[FAIL] Update failed: {e}")
        sys.exit(1)

    print("[3] Deleting place...")
    try:
        req = urllib.request.Request(
            f"{BASE_URL}/places/{place_id}",
            headers=headers,
            method="DELETE",
        )
        with urllib.request.urlopen(req) as response:
            if response.status != 200:
                print(f"[FAIL] Delete returned status {response.status}")
                sys.exit(1)
            print("[PASS] Place deleted.")
    except Exception as e:
        print(f"[FAIL] Delete failed: {e}")
        sys.exit(1)

    print("[4] Verifying deletion...")
    try:
        urllib.request.urlopen(f"{BASE_URL}/places/{place_id}")
        print("[FAIL] Place still exists after deletion.")
        sys.exit(1)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print("[PASS] Place deletion confirmed (404).")
            return
        print(f"[FAIL] Unexpected status while verifying deletion: {e.code}")
        sys.exit(1)


if __name__ == "__main__":
    test_phase3_flow()
