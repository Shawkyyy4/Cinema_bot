import requests, json, os

URL = "https://egy.voxcinemas.com/showtimes?c=city-centre-almaza&d=20261225"
TOKEN = os.environ["TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
FILE = "seen.json"


def send(text):
    requests.get(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        params={"chat_id": CHAT_ID, "text": text},
        timeout=20,
    )


if os.environ.get("GITHUB_EVENT_NAME") == "workflow_dispatch":
    send("البوت شغال ✅")

state = json.load(open(FILE)) if os.path.exists(FILE) else {}

r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
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
