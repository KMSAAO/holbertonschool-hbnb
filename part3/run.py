# filename: run.py
from app import create_app

app = create_app()

if __name__ == "__main__":
    # هذا الأمر يشغل السيرفر على المنفذ 5000
    print("Starting HBnB Server on port 5000...")
    app.run(debug=True, host='0.0.0.0', port=5000)