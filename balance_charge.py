import requests, time, uuid

token = "توکن ربات خودت"
chat = "ایدی عددی خودت"
base = f"https://api.telegram.org/bot{token}"

s = requests.Session()

def api(m, **d):
    try:
        r = s.post(f"{base}/{m}", data=d, timeout=20)
        return r.json()
    except:
        return {}

api("getUpdates", offset=-1)

pay = "p" + uuid.uuid4().hex[:8]
print(pay)

res = api(
    "sendInvoice",
    chat_id=chat,
    title="hash",
    description="stars",
    payload=pay,
    provider_token="",
    currency="XTR",
    prices='[{"label":"stars","amount":50}]'
)

if not res.get("ok"):
    print("فاکتور نرفت")
    exit()

print("فاکتور رفت... پرداخت کن")

t_end = time.time() + 300

while time.time() < t_end:
    ups = api(
        "getUpdates",
        offset=-1,
        limit=3,
        timeout=15,
        allowed_updates='["pre_checkout_query","message"]'
    )

    if not ups.get("result"):
        time.sleep(1)
        continue

    for u in ups["result"]:
        if "pre_checkout_query" in u:
            q = u["pre_checkout_query"]
            if str(q["from"]["id"]) == chat and q["invoice_payload"] == pay:
                api("answerPreCheckoutQuery", pre_checkout_query_id=q["id"], ok=True)
                print("ok")

        if "message" in u and "successful_payment" in u["message"]:
            p = u["message"]["successful_payment"]
            if p["invoice_payload"] == pay:
                print("اومد", p["total_amount"])
                exit()

print("تموم شد")
