import requests

token = "token"
user_id = 6....
gift_id = "50...."

url = f"https://api.telegram.org/bot{token}/sendGift"

r = requests.post(url, json={"user_id": user_id, "gift_id": gift_id}, timeout=5)
print(r.text)