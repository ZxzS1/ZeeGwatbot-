import http.server
import socketserver
import json
import urllib.request
import os

BOT_TOKEN = "8930956292:AAHFWpit3gyqs8cCpvPAnyueb14hJwFwyAE"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"

PAYMENT_INFO = """
💳 **ငွေပေးချေမှု အကောင့်များ (09449490500)**
------------------------------------
• KBZPay: 09449490500 (Soe Pyae Sone)
• WavePay: 09449490500 (Soe Pyae Sone)
• AYA Pay: 09449490500 (Soe Pyae Sone)
• UAB Pay: 09449490500  (Soe Pyae Sone)
• Yoma Pay: 09449490500  (Soe Pyae Sone)

ငွေလွှဲပြီးပါက ရရှိလာသော Screenshot or Transaction ID (သို့မဟုတ် အနောက်ဆုံး ၆ လုံး) ကို အော်ဒါတင်သည့်အခါ ရိုက်ထည့်ပေးပါခင်ဗျာ။
"""

SUPPORT_INFO = """
📞 **Admin Contact & Support**
------------------------------------
• Phone: 09449490500
• Telegram Admin: @ZeeGwat0
• Website: https://myanplay.vercel.app

အော်ဒါများနှင့် ပတ်သက်၍ အကူအညီ လိုအပ်ပါက သို့မဟုတ် မေးမြန်းလိုပါက Admin ထံ တိုက်ရိုက် ဆက်သွယ်နိုင်ပါသည်ခင်ဗျာ။
"""

MAIN_MENU = {
    "inline_keyboard": [
        [{"text": "🛡️ Mobile Legends (Diamonds)", "callback_data": "game_mlbb"}],
        [{"text": "🎯 PUBG Mobile (UC)", "callback_data": "game_pubg"}],
        [{"text": "💳 ငွေပေးချေမှု အကောင့်များ", "callback_data": "menu_payment"}],
        [{"text": "📞 Admin Contact / Support", "callback_data": "menu_support"}]
    ]
}

# MLBB Packages categorized by supplier channel
MLBB_PKGS = {
    "inline_keyboard": [
        [{"text": "💎 86 Diamonds (5,600 Ks) [SmileOne]", "callback_data": "pkg_mlbb_86_smileone"}],
        [{"text": "💎 172 Diamonds (10,800 Ks) [SmileOne]", "callback_data": "pkg_mlbb_172_smileone"}],
        [{"text": "💎 257 Diamonds (16,800 Ks) [SmileOne]", "callback_data": "pkg_mlbb_257_smileone"}],
        [{"text": "💎 706 Diamonds (42,000 Ks) [SmileOne]", "callback_data": "pkg_mlbb_706_smileone"}],
        [{"text": "💎 Weekly Diamond Pass (6,600 Ks) [Codashop]", "callback_data": "pkg_mlbb_pass_coda"}],
        [{"text": "💎 202 Diamonds (12,000 Ks) [Codashop]", "callback_data": "pkg_mlbb_202_coda"}],
        [{"text": "💎 404 Diamonds (21,000 Ks) [Codashop]", "callback_data": "pkg_mlbb_404_coda"}],
        [{"text": "💎 829 Diamonds (40,500 Ks) [Codashop]", "callback_data": "pkg_mlbb_829_coda"}],
        [{"text": "💎 2,157 Diamonds (90,000 Ks) [Codashop]", "callback_data": "pkg_mlbb_2157_coda"}],
        [{"text": "⬅️ ပင်မစာမျက်နှာသို့", "callback_data": "menu_main"}]
    ]
}

# PUBG UC Packages (SmileOne Code -> Midasbuy Redeem Flow)
PUBG_PKGS = {
    "inline_keyboard": [
        [{"text": "🔫 60 UC (4,300 Ks) [SmileOne -> Midasbuy]", "callback_data": "pkg_pubg_60_midas"}],
        [{"text": "🔫 325 UC (22,000 Ks) [SmileOne -> Midasbuy]", "callback_data": "pkg_pubg_325_midas"}],
        [{"text": "🔫 660 UC (43,500 Ks) [SmileOne -> Midasbuy]", "callback_data": "pkg_pubg_660_midas"}],
        [{"text": "🔫 1,800 UC (108,000 Ks) [SmileOne -> Midasbuy]", "callback_data": "pkg_pubg_1800_midas"}],
        [{"text": "⬅️ ပင်မစာမျက်နှာသို့", "callback_data": "menu_main"}]
    ]
}

def send_telegram_request(method, payload):
    url = API_URL + method
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(
        url, 
        data=data, 
        headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"Error calling {method}: {e}")
        return None

def process_update(update):
    if "message" in update:
        msg = update["message"]
        chat_id = msg["chat"]["id"]
        welcome_text = "👋 **MyanPlay 24/7 Game Top-Up Bot မှ ကြိုဆိုပါသည်!**\n\nMobile Legends နှင့် PUBG Mobile စိန်/UC များကို ၂၄ နာရီ အလိုအလျောက် ဝယ်ယူနိုင်ပါသည်။\n\nဝယ်ယူလိုသည့် ဂိမ်းကို ရွေးချယ်ပါခင်ဗျာ -"
        send_telegram_request("sendMessage", {
            "chat_id": chat_id,
            "text": welcome_text,
            "parse_mode": "Markdown",
            "reply_markup": MAIN_MENU
        })

    elif "callback_query" in update:
        cq = update["callback_query"]
        cq_id = cq["id"]
        chat_id = cq["message"]["chat"]["id"]
        msg_id = cq["message"]["message_id"]
        data = cq["data"]

        send_telegram_request("answerCallbackQuery", {"callback_query_id": cq_id})

        if data == "menu_main":
            send_telegram_request("editMessageText", {
                "chat_id": chat_id,
                "message_id": msg_id,
                "text": "👋 **MyanPlay 24/7 Game Top-Up Bot - ပင်မစာမျက်နှာ**\n\nဝယ်ယူလိုသည့် ဂိမ်းကို ရွေးချယ်ပါ -",
                "parse_mode": "Markdown",
                "reply_markup": MAIN_MENU
            })
        elif data == "menu_payment":
            send_telegram_request("editMessageText", {
                "chat_id": chat_id,
                "message_id": msg_id,
                "text": PAYMENT_INFO,
                "parse_mode": "Markdown",
                "reply_markup": {"inline_keyboard": [[{"text": "⬅️ ပင်မစာမျက်နှာသို့", "callback_data": "menu_main"}]]}
            })
        elif data == "menu_support":
            send_telegram_request("editMessageText", {
                "chat_id": chat_id,
                "message_id": msg_id,
                "text": SUPPORT_INFO,
                "parse_mode": "Markdown",
                "reply_markup": {"inline_keyboard": [[{"text": "⬅️ ပင်မစာမျက်နှာသို့", "callback_data": "menu_main"}]]}
            })
        elif data == "game_mlbb":
            send_telegram_request("editMessageText", {
                "chat_id": chat_id,
                "message_id": msg_id,
                "text": "🛡️ **Mobile Legends Top-Up**\n\nဝယ်ယူလိုသည့် Diamond Package ပမာဏကို ရွေးချယ်ပါ -",
                "parse_mode": "Markdown",
                "reply_markup": MLBB_PKGS
            })
        elif data == "game_pubg":
            send_telegram_request("editMessageText", {
                "chat_id": chat_id,
                "message_id": msg_id,
                "text": "🎯 **PUBG Mobile Top-Up**\n\nဝယ်ယူလိုသည့် UC Package ပမာဏကို ရွေးချယ်ပါ -",
                "parse_mode": "Markdown",
                "reply_markup": PUBG_PKGS
            })
        elif data.startswith("pkg_"):
            pkg_title = data.replace("pkg_", "").replace("_", " ").title()
            
            supplier_note = "SmileOne Direct Channel"
            if "Coda" in data or "coda" in data:
                supplier_note = "Codashop (Visa Card) Channel"
            elif "Midas" in data or "midas" in data:
                supplier_note = "SmileOne Code -> Midasbuy Redeem Channel"

            pay_msg = f"💳 **ငွေပေးချေမှုနှင့် အော်ဒါတင်ရန် လမ်းညွှန်ချက်**\n------------------------------------\n• ရွေးချယ်ထားသော ပမာဏ: {pkg_title}\n• Supplier Channel: {supplier_note}\n• ငွေလွှဲရမည့် ဖုန်းနံပါတ်: `09449490500` (KBZPay, WavePay, AYAPay, UABPay, YomaPay)\n• Admin Contact: 09449490500 | TG: @ZeeGwat0\n\nငွေလွှဲပြီးပါက သင့် **Player ID + Server ID + Transaction ID (အနောက်ဆုံး ၆ လုံး)** ကို ဤ Chat ထဲတွင် ရိုက်ထည့်ပေးပါခင်ဗျာ။\n\nစနစ်မှ SmileOne / Codashop / Midasbuy ဖြင့် ၂၄ နာရီ အလိုအလျောက် စစ်ဆေးပြီး ဂိမ်းအကောင့်ထဲ တိုက်ရိုက် ဖြည့်သွင်းပေးပါမည်!"
            send_telegram_request("editMessageText", {
                "chat_id": chat_id,
                "message_id": msg_id,
                "text": pay_msg,
                "parse_mode": "Markdown",
                "reply_markup": {"inline_keyboard": [[{"text": "⬅️ ပင်မစာမျက်နှာသို့", "callback_data": "menu_main"}]]}
            })

class WebhookHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b"ZeeGwatbot Webhook Service is Live!")

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        try:
            update = json.loads(post_data.decode('utf-8'))
            process_update(update)
        except Exception as e:
            print(f"Error processing webhook: {e}")
        self.send_response(200)
        self.end_headers()

def set_webhook_on_render():
    render_url = os.environ.get("RENDER_EXTERNAL_URL", "https://zeegwatbot.onrender.com")
    webhook_url = f"{render_url}/webhook"
    print(f"Setting Telegram Webhook to: {webhook_url}")
    send_telegram_request("setWebhook", {"url": webhook_url})

if __name__ == "__main__":
    set_webhook_on_render()
    port = int(os.environ.get("PORT", 8080))
    print(f"Starting Webhook HTTP Server on port {port}...")
    server = socketserver.TCPServer(("", port), WebhookHandler)
    server.serve_forever()
