import requests
import os

BASE_URL = "http://127.0.0.1:5000/api/v1"

def test_image_flow():
    # 1. Login to get token
    print("1. Logging in...")
    auth_data = {
        "email": "admin@hbnb.io",
        "password": "admin"
    }
    # Ensure admin user exists or use a new one
    # Note: validation will fail if user doesn't exist, handle that
    try:
        login_resp = requests.post(f"{BASE_URL}/auth/login", json=auth_data)
        if login_resp.status_code == 401:
            # Register if login fails
            print("   Login failed, registering new user...")
            reg_data = {
                "email": "admin@hbnb.io",
                "password": "admin",
                "first_name": "Admin",
                "last_name": "User"
            }
            requests.post(f"{BASE_URL}/users", json=reg_data)
            login_resp = requests.post(f"{BASE_URL}/auth/login", json=auth_data)
        
        token = login_resp.json()['access_token']
        headers = {"Authorization": f"Bearer {token}"}
        print("   ✅ Login successful")

        # 2. Create a Place
        print("\n2. Creating a Place...")
        place_data = {
            "title": "Image Test Hotel",
            "description": "A place to test image uploads",
            "price": 100.0,
            "latitude": 10.0,
            "longitude": 20.0,
            "status": "available"
        }
        create_resp = requests.post(f"{BASE_URL}/places", json=place_data, headers=headers)
        if create_resp.status_code != 201:
            print(f"   ❌ Create failed: {create_resp.text}")
            return
        
        place_id = create_resp.json()['id']
        print(f"   ✅ Place created: {place_id}")

        # 3. Upload an Image
        print("\n3. Uploading an Image...")
        # Create a dummy image file
        with open("test_image.png", "wb") as f:
            f.write(os.urandom(1024)) # 1KB dummy file
        
        files = {
            'images': ('test_image.png', open('test_image.png', 'rb'), 'image/png')
        }
        
        upload_resp = requests.post(f"{BASE_URL}/places/{place_id}/images", files=files, headers=headers)
        
        if upload_resp.status_code == 200:
            print("   ✅ Upload successful")
            print(f"   Response: {upload_resp.json()}")
            
            uploaded_urls = upload_resp.json()['images']
            # 4. Verify persistence
            print("\n4. Verifying Persistence...")
            get_resp = requests.get(f"{BASE_URL}/places/{place_id}")
            place_info = get_resp.json()
            
            if 'images' in place_info and len(place_info['images']) > 0:
                print(f"   ✅ Images found in Place info: {place_info['images']}")
                
                # Check if file serves correctly
                img_url = place_info['images'][0] # e.g. /uploads/places/...
                # Remove leading slash if present for requests
                full_img_url = f"http://127.0.0.1:5000{img_url}"
                print(f"   Testing URL: {full_img_url}")
                img_resp = requests.get(full_img_url)
                if img_resp.status_code == 200:
                     print("   ✅ Image file is serving correctly (HTTP 200)")
                else:
                     print(f"   ❌ Image file failed to serve: {img_resp.status_code}")

            else:
                print("   ❌ Images NOT found in Place info")
        else:
            print(f"   ❌ Upload failed: {upload_resp.text}")

        # Cleanup
        os.remove("test_image.png")

    except Exception as e:
        print(f"❌ Test failed with error: {e}")

if __name__ == "__main__":
    test_image_flow()
