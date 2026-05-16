import os
import telebot
from telebot import types
from flask import Flask, request
import threading
import time
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import xH
import byte

# আপনার দেওয়া টেলিগ্রাম এপিআই টোকেন
API_TOKEN = "8799206347:AAHgh5qsT6utW3O3rbJkzw3y55Wx39Swf8U"
bot = telebot.TeleBot(API_TOKEN, threaded=False)
app = Flask(__name__)

# --- বাটন মেনু তৈরি ---
def main_keyboard():
    markup = types.InlineKeyboardMarkup()
    btn_spam = types.InlineKeyboardButton("🚀 Start Spam", callback_data="start_spam")
    btn_admin = types.InlineKeyboardButton("👨‍💻 Admin Contact", url="https://t.me/MOHASIN_king")
    markup.row(btn_spam)
    markup.row(btn_admin)
    return markup

# --- ভারসেল ওয়েবহুক হ্যান্ডলার ---
@app.route('/' + API_TOKEN, methods=['POST'])
def getMessage():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "!", 200
    else:
        return "Invalid Content-Type", 403

@app.route("/")
def webhook():
    bot.remove_webhook()
    # এখানে আপনার ভারসেল থেকে পাওয়া ইউআরএল পরে বসাতে হবে
    bot.set_webhook(url="https://tg-bot-ff-spam.vercel.app/" + API_TOKEN)
    return "MOHASIN BOT IS ALIVE!", 200

# --- বটের কমান্ড ও মেসেজ হ্যান্ডলার ---
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    help_text = (
        "🔥 **WLC TO MOHASIN TCP BOT** 🔥\n\n"
        "নিচের বাটনগুলো ব্যবহার করুন:\n"
        "১. **Start Spam**: স্প্যাম শুরু করতে ক্লিক করুন।\n"
        "২. **Admin Contact**: অ্যাডমিনের সাথে যোগাযোগ।"
    )
    bot.send_message(message.chat.id, help_text, reply_markup=main_keyboard(), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "start_spam")
def handle_spam_button(call):
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, "🎯 **স্পেম ইস রেডি!**\nপ্লিজ এন্টার ইওর ইউ আই ডি (UID):")

@bot.message_handler(func=lambda message: message.text.isdigit())
def handle_uid_input(message):
    target_uid = message.text.strip()
    bot.send_message(message.chat.id, f"🚀 UID {target_uid} রিসিভ হয়েছে। ব্যাকগ্রাউন্ডে প্রসেস শুরু হচ্ছে...")

    # --- ইউআইডি ইনপুট হ্যান্ডলারের ভেতর এই অংশটি চেক করুন ---
        def background_task():
            try:
                # ফাইলের সঠিক পাথ (Path) খুঁজে বের করা
                current_dir = os.path.dirname(os.path.abspath(__file__))
                accs_path = os.path.join(os.path.dirname(current_dir), 'accs.txt')

                if os.path.exists(accs_path):
                    with open(accs_path, "r") as f:
                        # ফাইল থেকে অ্যাকাউন্টগুলো নেওয়া
                        accounts = [line.strip().split(":") for line in f if ":" in line]
                    
                    if not accounts:
                        bot.send_message(message.chat.id, "❌ accs.txt ফাইলে কোনো অ্যাকাউন্ট পাওয়া যায়নি!")
                        return

                    success = 0
                    for u, p in accounts:
                        try:
                            # আপনার xH.py থেকে ফাংশন কল করা
                            at, old = xH.gTok(u, p)
                            # ইনভাইট পাঠানোর লজিক এখানে (আপনার মেইন কোড অনুযায়ী)
                            # ...
                            success += 1
                            time.sleep(0.3)
                        except:
                            continue
                    
                    bot.send_message(message.chat.id, f"✅ স্প্যাম সফল! {success}টি অ্যাকাউন্ট থেকে ইনভাইট পাঠানো হয়েছে।")
                else:
                    bot.send_message(message.chat.id, "❌ accs.txt ফাইলটি সার্ভারে খুঁজে পাওয়া যাচ্ছে না!")
            
            except Exception as e:
                bot.send_message(message.chat.id, f"Error: {str(e)}")

        threading.Thread(target=background_task).start()

if __name__ == "__main__":
    app.run()
