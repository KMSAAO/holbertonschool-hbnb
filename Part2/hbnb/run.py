from app import create_app
from flask import url_for

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5050)
