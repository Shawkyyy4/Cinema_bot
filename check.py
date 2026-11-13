import requests, json, os, time

URL = "https://egy.voxcinemas.com/showtimes?c=city-centre-almaza&d=20261225"
TOKEN = os.environ["TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
FILE = "seen.json"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
}


def send(text):
    requests.get(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        params={"chat_id": CHAT_ID, "text": text},
        timeout=20,
    )


if os.environ.get("GITHUB_EVENT_NAME") == "workflow_dispatch":
    send("البوت شغال ✅")

state = json.load(open(FILE)) if os.path.exists(FILE) else {}

r = None
for attempt in range(3):
    try:
        r = requests.get(URL, headers=HEADERS, timeout=45)
        break
    except Exception as e:
        print("محاولة", attempt + 1, "فشلت:", type(e).__name__)
        time.sleep(5)

if r is None:
    print("الموقع مش بيرد على سيرفر GitHub")
    raise SystemExit(0)

text = r.text.lower()
has_doom = "doomsday" in text
has_inf = has_doom and "infinity" in text
print("status", r.status_code, "size", len(r.text), "doomsday", has_doom, "infinity", has_inf)

if has_doom and not state.get("doomsday"):
    send(f"🎬 نزلت حفلات Avengers: Doomsday في الماظة يوم 25 ديسمبر\n{URL}")
    state["doomsday"] = True

if has_inf and not state.get("infinity"):
    send(f"✨ ظهرت كلمة Infinity جنب Doomsday يوم 25 ديسمبر، افحص الحفلات\n{URL}")
    state["infinity"] = True

json.dump(state, open(FILE, "w"))
