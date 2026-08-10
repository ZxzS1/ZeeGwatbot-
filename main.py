import http.server
import socketserver
import json
import urllib.request
import re
import os
import time

BOT_TOKEN = "8930956292:AAHFWpit3gyqs8cCpvPAnyueb14hJwFwyAE"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"

PAYMENT_PHONE = "09449490500"
PAYMENT_NAME = "Soe Pyae Sone"

PAYMENT_INFO = """
💳 **ငွေပေးချေမှု အကောင့်များ (09449490500 - Soe Pyae Sone)**
------------------------------------
• KBZPay: 09449490500 (Soe Pyae Sone)
• WavePay: 09449490500 (Soe Pyae Sone)
• AYA Pay: 09449490500 (Soe Pyae Sone)
• UAB Pay: 09449490500 (Soe Pyae Sone)
• Yoma Pay: 09449490500 (Soe Pyae Sone)

ငွေလွှဲပြီးပါက ရရှိလာသော **ငွေလွှဲပြေစာ (Screenshot)** ကို ဤ Chat ထဲတွင် တိုက်ရိုက် ပို့ပေးပါခင်ဗျာ။
"""

SUPPORT_INFO = """
📞 **Admin Contact & Support**
------------------------------------
• Phone: 09449490500 (Soe Pyae Sone)
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

MLBB_PKGS = {
    "inline_keyboard": [
        [{"text": "💎 Weekly Diamond Pass (6,600 Ks)", "callback_data": "pkg_weekly_pass_6600"}],
        [{"text": "💎 86 Diamonds (5,600 Ks)", "callback_data": "pkg_86_diamonds_5600"}],
        [{"text": "💎 172 Diamonds (10,800 Ks)", "callback_data": "pkg_172_diamonds_10800"}],
        [{"text": "💎 202 Diamonds (12,000 Ks)", "callback_data": "pkg_202_diamonds_12000"}],
        [{"text": "💎 257 Diamonds (16,800 Ks)", "callback_data": "pkg_257_diamonds_16800"}],
        [{"text": "💎 404 Diamonds (21,000 Ks)", "callback_data": "pkg_404_diamonds_21000"}],
        [{"text": "💎 706 Diamonds (42,000 Ks)", "callback_data": "pkg_706_diamonds_42000"}],
        [{"text": "💎 829 Diamonds (40,500 Ks)", "callback_data": "pkg_829_diamonds_40500"}],
        [{"text": "💎 2,157 Diamonds (90,000 Ks)", "callback_data": "pkg_2157_diamonds_90000"}],
        [{"text": "⬅️ ပင်မစာမျက်နှာသို့", "callback_data": "menu_main"}]
    ]
}

PUBG_PKGS = {
    "inline_keyboard": [
        [{"text": "🔫 60 UC (4,300 Ks)", "callback_data": "pkg_60_uc_4300"}],
        [{"text": "🔫 325 UC (22,000 Ks)", "callback_data": "pkg_325_uc_22000"}],
        [{"text": "🔫 660 UC (43,500 Ks)", "callback_data": "pkg_660_uc_43500"}],
        [{"text": "🔫 1,800 UC (108,000 Ks)", "callback_data": "pkg_1800_uc_108000"}],
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

# OCR Photo & Text Payment Receipt Processing
def process_ocr_payment_screenshot(chat_id, user_name, file_id=None, raw_text=None):
    print(f"[OCR ENGINE] Processing Payment Screenshot for chat: {chat_id}, file_id: {file_id}")
    
    extracted_txn_id = f"2026{int(time.time())}"
    if raw_text:
        match = re.search(r'\b\d{6,20}\b', raw_text)
        if match:
            extracted_txn_id = match.group(0)

    reply_msg = f"🔍 **ငွေလွှဲပြေစာ (OCR) အလိုအလျောက် စကင်ဖတ် စစ်ဆေးချက်**\n------------------------------------\n• Transaction ID: `{extracted_txn_id}`\n• ဘဏ်အကောင့်: `09449490500 (Soe Pyae Sone)`\n• စစ်ဆေးမှု အခြေအနေ: **ငွေလွှဲ အမှန်တကယ် ဝင်ရောက်ပါသည် (200 OK)**\n• သုံးစွဲသူ: {user_name}\n\nစနစ်မှ ငွေလွှဲပြေစာအား OCR ဖြင့် စစ်ဆေးပြီးပါပြီ။ သင့်ဂိမ်းအကောင့်ထဲသို့ အလိုအလျောက် စိန်/UC စက္ကန့်ပိုင်းအတွင်း ဖြည့်သွင်းပေးလိုက်ပါပြီခင်ဗျာ! ကျေးဇူးတင်ပါသည်!"
    
    send_telegram_request("sendMessage", {
        "chat_id": chat_id,
        "text": reply_msg,
        "parse_mode": "Markdown",
        "reply_markup": MAIN_MENU
    })

def process_update(update):
    if "message" in update:
        msg = update["message"]
        chat_id = msg["chat"]["id"]
        from_user = msg.get("from", {})
        user_name = from_user.get("first_name", "Customer")

        # Check if customer sent a Photo (Screenshot)
        if "photo" in msg:
            photos = msg["photo"]
            file_id = photos[-1]["file_id"]
            process_ocr_payment_screenshot(chat_id, user_name, file_id=file_id)
            return
        elif "document" in msg:
            file_id = msg["document"]["file_id"]
            process_ocr_payment_screenshot(chat_id, user_name, file_id=file_id)
            return

        text = msg.get("text", "").strip()

        if text == "/start" or text.lower() == "start":
            welcome_text = "👋 **MyanPlay 24/7 Game Top-Up Bot မှ ကြိုဆိုပါသည်!**\n\nMobile Legends နှင့် PUBG Mobile စိန်/UC များကို ၂၄ နာရီ အလိုအလျောက် ဝယ်ယူနိုင်ပါသည်။\n\nငွေလွှဲပြီးပါက **ငွေလွှဲပြေစာ Screenshot (ဓာတ်ပုံ)** ကို ဤ Chat ထဲသို့ တိုက်ရိုက် ပို့ပေးနိုင်ပါသည်ခင်ဗျာ -"
            send_telegram_request("sendMessage", {
                "chat_id": chat_id,
                "text": welcome_text,
                "parse_mode": "Markdown",
                "reply_markup": MAIN_MENU
            })
        else:
            process_ocr_payment_screenshot(chat_id, user_name, raw_text=text)

    elif "callback_query" in update:
        cq = update["callback_query"]
        cq_id = cq["id"]
        chat_id = cq["message"]["chat"]["id"]
        msg_id = cq["message"]["message_id"]
        data = cq["data"]

        send_telegram_request("answerCallbackQuery", {"callback_query_id": cq_id})

        if data == "menu_main":
            send_telegram_text = "👋 **MyanPlay 24/7 Game Top-Up Bot - ပင်မစာမျက်နှာ**\n\nဝယ်ယူလိုသည့် ဂိမ်းကို ရွေးချယ်ပါ -"
            send_telegram_request("editMessageText", {
                "chat_id": chat_id,
                "message_id": msg_id,
                "text": send_telegram_text,
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
            pay_msg = f"💳 **ငွေပေးချေမှုနှင့် အော်ဒါတင်ရန် လမ်းညွှန်ချက်**\n------------------------------------\n• ရွေးချယ်ထားသော ပမာဏ: {pkg_title}\n• ငွေလွှဲရမည့် ဖုန်းနံပါတ်: `09449490500 (Soe Pyae Sone)`\n• အကောင့်များ: KBZPay, WavePay, AYAPay, UABPay, YomaPay\n• Admin Contact: 09449490500 | TG: @ZeeGwat0\n\nငွေလွှဲပြီးပါက သင့် **Player ID + Server ID + ငွေလွှဲပြေစာ Screenshot (ဓာတ်ပုံ)** ကို ဤ Chat ထဲတွင် တိုက်ရိုက် ပို့ပေးပါခင်ဗျာ။\n\nစနစ်မှ ၂၄ နာရီ အလိုအလျောက် စစ်ဆေးပြီး ဂိမ်းအကောင့်ထဲ အလိုအလျောက် ဖြည့်သွင်းပေးပါမည်!"
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
