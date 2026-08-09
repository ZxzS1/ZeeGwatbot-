import http.server
import socketserver
import json
import threading
import urllib.request
import time
import os

BOT_TOKEN = "8930956292:AAGGF0mGfjFUUpOyOhBoIftyYeuYNLJzx90"
API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/"

PAYMENT_INFO = """
💳 **ငွေပေးချေမှု အကောင့်များ (09449490500)**
------------------------------------
• KBZPay: 09449490500 (MyanPlay TopUp)
• WavePay: 09449490500 (MyanPlay TopUp)
• AYA Pay: 09449490500
• UAB Pay: 09449490500
• Yoma Pay: 09449490500

ငွေလွှဲပြီးပါက ရရှိလာသော Transaction ID (သို့မဟုတ် အနောက်ဆုံး ၆ လုံး) ကို အော်ဒါတင်သည့်အခါ ရိုက်ထည့်ပေးပါခင်ဗျာ။
"""

MAIN_MENU = {
    "inline_keyboard": [
        [{"text": "🎮 Direct Player ID Top-Up", "callback_data": "menu_direct"}],
        [{"text": "🎁 Voucher & Gift Cards (24/7 Auto)", "callback_data": "menu_voucher"}],
        [{"text": "💳 ငွေပေးချေမှု အကောင့်များ", "callback_data": "menu_payment"}],
        [{"text": "📞 Admin Contact / Support", "callback_data": "menu_support"}]
    ]
}

DIRECT_GAMES_MENU = {
    "inline_keyboard": [
        [{"text": "🛡️ Mobile Legends", "callback_data": "game_mlbb"}, {"text": "🎯 PUBG Mobile", "callback_data": "game_pubg"}],
        [{"text": "🔥 Free Fire", "callback_data": "game_freefire"}, {"text": "👑 Honor of Kings", "callback_data": "game_hok"}],
        [{"text": "⬅️ ပင်မစာမျက်နှာသို့", "callback_data": "menu_main"}]
    ]
}

VOUCHER_GAMES_MENU = {
    "inline_keyboard": [
        [{"text": "🎁 Roblox Gift Card", "callback_data": "vgame_roblox"}],
        [{"text": "🎮 Steam Wallet Card", "callback_data": "vgame_steam"}],
        [{"text": "⭐ Telegram Stars", "callback_data": "vgame_stars"}],
        [{"text": "⬅️ ပင်မစာမျက်နှာသို့", "callback_data": "menu_main"}]
    ]
}

def send_telegram_request(method, payload):
    url = API_URL + method
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode('utf-8'))
    except Exception as e:
        print(f"Error calling {method}: {e}")
        return None

def process_update(update):
    if "message" in update:
        msg = update["message"]
        chat_id = msg["chat"]["id"]
        text = msg.get("text", "")

        if text == "/start":
            welcome_text = "👋 **MyanPlay 24/7 Game Top-Up Bot မှ ကြိုဆိုပါသည်!**\n\n၂၄ နာရီ ပိတ်ရက်မရှိ ဂိမ်းစိန်/UC နှင့် Gift Card များကို အလိုအလျောက် ဝယ်ယူနိုင်ပါသည်။\n\nအောက်ပါ Menu များမှ စတင် ရွေးချယ်နိုင်ပါသည်ခင်ဗျာ -"
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
                "text": "👋 **MyanPlay 24/7 Game Top-Up Bot - ပင်မစာမျက်နှာ**\n\nဝယ်ယူလိုသည့် ဝန်ဆောင်မှုကို ရွေးချယ်ပါ -",
                "parse_mode": "Markdown",
                "reply_markup": MAIN_MENU
            })
        elif data == "menu_direct":
            send_telegram_request("editMessageText", {
                "chat_id": chat_id,
                "message_id": msg_id,
                "text": "🎮 **Direct Player ID Top-Up**\n\nဂိမ်းအကောင့်ထဲသို့ တိုက်ရိုက် ဖြည့်သွင်းလိုသည့် ဂိမ်းကို ရွေးချယ်ပါ -",
                "parse_mode": "Markdown",
                "reply_markup": DIRECT_GAMES_MENU
            })
        elif data == "menu_voucher":
            send_telegram_request("editMessageText", {
                "chat_id": chat_id,
                "message_id": msg_id,
                "text": "🎁 **24/7 Instant Voucher & Gift Cards**\n\nဝယ်ယူလိုသည့် Gift Card / Digital Code အမျိုးအစားကို ရွေးချယ်ပါ -",
                "parse_mode": "Markdown",
                "reply_markup": VOUCHER_GAMES_MENU
            })
        elif data == "menu_payment":
            send_telegram_request("editMessageText", {
                "chat_id": chat_id,
                "message_id": msg_id,
                "text": PAYMENT_INFO,
                "parse_mode": "Markdown",
                "reply_markup": {"inline_keyboard": [[{"text": "⬅️ ပင်မစာမျက်နှာသို့", "callback_data": "menu_main"}]]}
            })

def start_bot_polling():
    offset = 0
    print("🤖 MyanPlay Telegram Bot Agent Running...")
    while True:
        try:
            res = send_telegram_request("getUpdates", {"offset": offset, "timeout": 30})
            if res and res.get("ok"):
                for update in res.get("result", []):
                    offset = update["update_id"] + 1
                    process_update(update)
        except Exception as e:
            print(f"Polling error: {e}")
        time.sleep(1)

def run_dummy_http_server():
    port = int(os.environ.get("PORT", 8080))
    class SimpleHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"MyanPlay Telegram Bot is Live 24/7")

    with socketserver.TCPServer(("", port), SimpleHandler) as httpd:
        print(f"HTTP Server listening on port {port}")
        httpd.serve_forever()

if __name__ == "__main__":
    t = threading.Thread(target=run_dummy_http_server, daemon=True)
    t.start()
    start_bot_polling()
            
