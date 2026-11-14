import requests, json, os, re, time

URL = "https://egy.voxcinemas.com/showtimes?c=city-centre-almaza&m=avengers-doomsday-infinity-vision"
TOKEN = os.environ["TOKEN"]
CHAT_IDS = [c.strip() for c in os.environ["CHAT_ID"].split(",") if c.strip()]
FILE = "seen.json"
TEST = True
HEADERS = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
}


def send(text):
    for cid in CHAT_IDS:
        try:
            requests.get(
                f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                params={"chat_id": cid, "text": text},
                timeout=20,
            )
        except Exception as e:
            print("فشل الإرسال:", type(e).__name__)


def alert(text, times=5, gap=15):
    for i in range(times):
        send(f"🚨 ({i + 1}/{times}) {text}\n{URL}")
        if i < times - 1:
            time.sleep(gap)


is_manual = os.environ.get("GITHUB_EVENT_NAME") == "workflow_dispatch"

if is_manual:
    send("البوت شغال ✅")

if TEST and is_manual:
    alert("ده اختبار بس، متقلقش")

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
    print("الموقع مش بيرد")
    raise SystemExit(0)

clean = re.sub(r"<[^>]+>", " ", r.text)
clean = re.sub(r"\s+", " ", clean).lower()

pattern = r"(?:mon|tue|wed|thu|fri|sat|sun)\s*\d{1,2}\s*(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)"
days = list(dict.fromkeys(re.findall(pattern, clean)))
day_open = re.search(r"fri\s*25\s*dec", clean) is not None

print("status", r.status_code)
print("الأيام اللي لقيتها:", days)
print("يوم 25 ظهر:", day_open)

if day_open and not state.get("day25"):
    state["day25"] = True
    json.dump(state, open(FILE, "w"))
    alert("حفلات Doomsday Infinity Vision يوم الجمعة 25 ديسمبر نزلت، الحق احجز")

json.dump(state, open(FILE, "w"))
