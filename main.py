import http.server
import socketserver
import json
import urllib.request
import os

BOT_TOKEN = "8930956292:AAHFWpit3gyqs8cCpvPAnyueb14hJwFwyAE"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"

# Admin Telegram Info
ADMIN_USERNAME = "@ZeeGwat0"
ADMIN_CHAT_ID = os.environ.get("ADMIN_CHAT_ID", None)

PAYMENT_INFO = """
💳 **ငွေပေးချေမှု အကောင့်များ (09449490500 - Soe Pyae Sone)**
------------------------------------
• KBZPay: 09449490500 (Soe Pyae Sone)
• WavePay: 09449490500 (Soe Pyae Sone)
• AYA Pay: 09449490500 (Soe Pyae Sone)
• UAB Pay: 09449490500 (Soe Pyae Sone)
• Yoma Pay: 09449490500 (Soe Pyae Sone)

ငွေလွှဲပြီးပါက ရရှိလာသော **ငွေလွှဲပြေစာ (Screenshot)** နှင့် **Player ID** ကို ဤ Chat ထဲတွင် တိုက်ရိုက် ပို့ပေးပါခင်ဗျာ။
"""

SUPPORT_INFO = f"""
📞 **Admin Contact & Support**
------------------------------------
• Phone: 09449490500 (Soe Pyae Sone)
• Telegram Admin: {@ZeeGwat0}
• Website: https://myanplay.vercel.app

အော်ဒါများနှင့် ပတ်သက်၍ အကူအညီ လိုအပ်ပါက သို့မဟုတ် မေးမြန်းလိုပါက Admin ({ADMIN_USERNAME}) ထံ တိုက်ရိုက် ဆက်သွယ်နိုင်ပါသည်ခင်ဗျာ။
"""

MAIN_MENU = {
    "inline_keyboard": [
        [{"text": "⚔️ Mobile Legends: Bang Bang", "callback_data": "game_mlbb"}],
        [{"text": "🪖 PUBG Mobile (UC)", "callback_data": "game_pubg"}],
        [{"text": "💳 ငွေပေးချေမှု အကောင့်များ", "callback_data": "menu_payment"}],
        [{"text": "📞 Admin Contact / Support", "callback_data": "menu_support"}]
    ]
}

MLBB_PKGS = {
    "inline_keyboard": [
        [{"text": "💎 Weekly Diamond Pass (6,600 Ks)", "callback_data": "pkg_Weekly_Pass_6600"}],
        [{"text": "💎 86 Diamonds (5,600 Ks)", "callback_data": "pkg_86_Diamonds_5600"}],
        [{"text": "💎 172 Diamonds (10,800 Ks)", "callback_data": "pkg_172_Diamonds_10800"}],
        [{"text": "💎 202 Diamonds (12,000 Ks)", "callback_data": "pkg_202_Diamonds_12000"}],
        [{"text": "💎 257 Diamonds (16,800 Ks)", "callback_data": "pkg_257_Diamonds_16800"}],
        [{"text": "💎 404 Diamonds (21,000 Ks)", "callback_data": "pkg_404_Diamonds_21000"}],
        [{"text": "💎 706 Diamonds (42,000 Ks)", "callback_data": "pkg_706_Diamonds_42000"}],
        [{"text": "💎 829 Diamonds (40,500 Ks)", "callback_data": "pkg_829_Diamonds_40500"}],
        [{"text": "💎 2,157 Diamonds (90,000 Ks)", "callback_data": "pkg_2157_Diamonds_90000"}],
        [{"text": "⬅️ ပင်မစာမျက်နှာသို့", "callback_data": "menu_main"}]
    ]
}

PUBG_PKGS = {
    "inline_keyboard": [
        [{"text": "🔫 60 UC (4,300 Ks)", "callback_data": "pkg_60_UC_4300"}],
        [{"text": "🔫 325 UC (22,000 Ks)", "callback_data": "pkg_325_UC_22000"}],
        [{"text": "🔫 660 UC (43,500 Ks)", "callback_data": "pkg_660_UC_43500"}],
        [{"text": "🔫 1,800 UC (108,000 Ks)", "callback_data": "pkg_1800_UC_108000"}],
        [{"text": "⬅️ ပင်မစာမျက်နှာသို့", "callback_data": "menu_main"}]
    ]
}

# Step-by-Step Order State Tracker
USER_ORDER_STATE = {}

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
    global ADMIN_CHAT_ID
    if "message" in update:
        msg = update["message"]
        chat_id = msg["chat"]["id"]
        from_user = msg.get("from", {})
        user_name = from_user.get("first_name", "Customer")
        username = from_user.get("username", "NoUsername")
        user_handle = f"@{username}" if username != "NoUsername" else user_name

        text = msg.get("text", "").strip()

        # Admin Setup Detection (If Admin sends /admin or /start)
        if username.lower() == "zeegwat0" or text == "/admin":
            ADMIN_CHAT_ID = chat_id
            print(f"👑 ADMIN CHAT ID DETECTED & SET TO: {ADMIN_CHAT_ID}")
            send_telegram_request("sendMessage", {
                "chat_id": chat_id,
                "text": f"👑 **Admin Account အဖြစ် အောင်မြင်စွာ ချိတ်ဆက်ပြီးပါပြီ!**\n------------------------------------\n• Admin Chat ID: `{chat_id}`\n• Admin Username: @{username}\n\nဝယ်ယူသူများ အော်ဒါနှင့် ငွေလွှဲပြေစာ ပို့လိုက်ပါက သင့်ထံသို့ ပေါင်းစည်းလျက် တိုက်ရိုက် ရောက်ရှိမည် ဖြစ်ပါသည်ခင်ဗျာ!",
                "parse_mode": "Markdown",
                "reply_markup": MAIN_MENU
            })
            return

        # Handle Start Command
        if text == "/start" or text.lower() == "start":
            USER_ORDER_STATE[chat_id] = {"step": "IDLE"}
            welcome_text = "👋 **MyanPlay Game Top-Up မှ ကြိုဆိုပါသည်!**\n\nMobile Legends နှင့် PUBG Mobile စိန်/UC များကို အလွယ်တကူ ဝယ်ယူနိုင်ပါသည်။\n\nဝယ်ယူလိုသည့် ဂိမ်းကို ရွေးချယ်ပါခင်ဗျာ -"
            send_telegram_request("sendMessage", {
                "chat_id": chat_id,
                "text": welcome_text,
                "parse_mode": "Markdown",
                "reply_markup": MAIN_MENU
            })
            return

        # Get Current Order State
        user_state = USER_ORDER_STATE.get(chat_id, {})
        step = user_state.get("step", "IDLE")

        if step == "WAITING_PLAYER_ID":
            # Step 2 Complete: Got Player ID -> Now Ask for Payment Screenshot
            USER_ORDER_STATE[chat_id]["player_id"] = text
            USER_ORDER_STATE[chat_id]["step"] = "WAITING_SCREENSHOT"

            current_pkg = USER_ORDER_STATE[chat_id].get("pkg", "မသိရှိပါ")

            pay_instructions = f"💳 **ငွေပေးချေရန် လမ်းညွှန်ချက်**\n------------------------------------\n• ဝယ်ယူသည့် ပစ္စည်း: **{current_pkg}**\n• Player ID: `{text}`\n• ငွေလွှဲရမည့် ဖုန်းနံပါတ်: `09449490500 (Soe Pyae Sone)`\n• ဘဏ်အကောင့်များ: KBZPay, WavePay, AYAPay, UABPay, YomaPay\n\n**အဆင့် ၃ (နောက်ဆုံးအဆင့်)**: ငွေလွှဲပြီးပါက သင့် **ငွေလွှဲပြေစာ Screenshot (ဓာတ်ပုံ)** ကို ဤ Chat ထဲသို့ ပို့ပေးပါခင်ဗျာ။"
            
            send_telegram_request("sendMessage", {
                "chat_id": chat_id,
                "text": pay_instructions,
                "parse_mode": "Markdown"
            })
            return

        elif step == "WAITING_SCREENSHOT" or "photo" in msg or "document" in msg:
            # Step 3 Complete: Got Screenshot -> Compile Everything into One Order Summary!
            current_pkg = USER_ORDER_STATE.get(chat_id, {}).get("pkg", "မသိရှိပါ")
            player_id = USER_ORDER_STATE.get(chat_id, {}).get("player_id", text if text else "မသိရှိပါ")

            # Reset State
            USER_ORDER_STATE[chat_id] = {"step": "IDLE"}

            # 1. Send Confirmation to Customer
            customer_confirm = f"✅ **အော်ဒါ ပေါင်းစည်းချက် အချက်အလက်များ လက်ခံရရှိပါသည်!**\n------------------------------------\n• ဝယ်ယူသည့် ပစ္စည်း: **{current_pkg}**\n• Game Player ID: `{player_id}`\n• ငွေလွှဲပြေစာ: **လက်ခံရရှိပါသည်**\n• ဝယ်ယူသူ: **{user_handle}**\n\nသင့်အော်ဒါ အချက်အလက် အပြည့်အစုံကို Admin (**{ADMIN_USERNAME}**) ထံသို့ တစ်ပေါင်းတည်း တိုက်ရိုက် ပေးပို့လိုက်ပါပြီခင်ဗျာ။ Admin မှ စစ်ဆေးပြီး ချက်ချင်း ဖြည့်သွင်းပေးပါမည်!"
            
            send_telegram_request("sendMessage", {
                "chat_id": chat_id,
                "text": customer_confirm,
                "parse_mode": "Markdown",
                "reply_markup": MAIN_MENU
            })

            # 2. Forward ONE Single Compiled Order Summary to Admin (@ZeeGwat0)
            admin_compiled_summary = f"📩 **အော်ဒါအသစ် ပေါင်းစည်း အချက်အလက် (New Order Summary)**\n------------------------------------\n👤 **ဝယ်ယူသူ**: {user_handle} (ID: `{chat_id}`)\n📦 **ဝယ်ယူသည့် ပစ္စည်း**: **{current_pkg}**\n🎮 **Game Player ID / Server ID**: `{player_id}`\n📸 **ငွေလွှဲပြေစာ**: (Attached Below)"

            target_admin = ADMIN_CHAT_ID if ADMIN_CHAT_ID else chat_id

            if "photo" in msg:
                photo_id = msg["photo"][-1]["file_id"]
                send_telegram_request("sendPhoto", {
                    "chat_id": target_admin,
                    "photo": photo_id,
                    "caption": admin_compiled_summary,
                    "parse_mode": "Markdown"
                })
            else:
                send_telegram_request("sendMessage", {
                    "chat_id": target_admin,
                    "text": admin_compiled_summary,
                    "parse_mode": "Markdown"
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
                "text": "👋 **MyanPlay Game Top-Up - ပင်မစာမျက်နှာ**\n\nဝယ်ယူလိုသည့် ဂိမ်းကို ရွေးချယ်ပါ -",
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
                "text": "⚔️ **Mobile Legends: Bang Bang Top-Up**\n\nဝယ်ယူလိုသည့် Diamond Package ပမာဏကို ရွေးချယ်ပါ -",
                "parse_mode": "Markdown",
                "reply_markup": MLBB_PKGS
            })
        elif data == "game_pubg":
            send_telegram_request("editMessageText", {
                "chat_id": chat_id,
                "message_id": msg_id,
                "text": "🪖 **PUBG Mobile Top-Up**\n\nဝယ်ယူလိုသည့် UC Package ပမာဏကို ရွေးချယ်ပါ -",
                "parse_mode": "Markdown",
                "reply_markup": PUBG_PKGS
            })
        elif data.startswith("pkg_"):
            pkg_title = data.replace("pkg_", "").replace("_", " ").title()
            
            # Initiate Step 1 -> Step 2
            if chat_id not in USER_ORDER_STATE:
                USER_ORDER_STATE[chat_id] = {}
            USER_ORDER_STATE[chat_id]["pkg"] = pkg_title
            USER_ORDER_STATE[chat_id]["step"] = "WAITING_PLAYER_ID"

            step2_msg = f"🎮 **{pkg_title}** ကို ရွေးချယ်ထားပါသည်။\n------------------------------------\n**အဆင့် ၂**: ကျေးဇူးပြု၍ သင့် **Player ID (+ Zone/Server ID)** ကို ရိုက်ထည့်ပေးပါခင်ဗျာ။\n(ဥပမာ - `123456789 (1234)`)"
            
            send_telegram_request("editMessageText", {
                "chat_id": chat_id,
                "message_id": msg_id,
                "text": step2_msg,
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
