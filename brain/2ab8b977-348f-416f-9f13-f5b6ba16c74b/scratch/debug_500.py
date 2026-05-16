import requests

# Assuming a user exists, if not this will fail with 401
LOGIN_URL = 'http://127.0.0.1:8001/api/users/login/'
BANNERS_URL = 'http://127.0.0.1:8001/api/banners/'

# I need a real user to login.
# I'll try to find a user in the database or just use the admin if I know the password.
# Since I don't know the password, I'll try to hit the endpoint without auth first to see if it gives 401 (expected).

print("Fetching without auth...")
r = requests.get(BANNERS_URL)
print(f"Status: {r.status_code}")
print(f"Content: {r.text[:500]}")

# If the user is getting 500, they ARE authenticated.
