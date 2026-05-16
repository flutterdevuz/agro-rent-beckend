import requests
try:
    r = requests.get('http://127.0.0.1:8000/api/docs/')
    print(f"Status Code: {r.status_code}")
    print(f"Headers: {r.headers}")
except Exception as e:
    print(f"Error: {e}")
