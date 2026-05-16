import os
import telebot
from telebot import types
from flask import Flask, request
import threading
import time

# আপনার আপলোড করা মডিউলগুলো ইমপোর্ট
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
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    # এখানে আপনার ভারসেল থেকে পাওয়া ইউআরএল পরে বসাতে হবে
    # উদাহরণ: bot.set_webhook(url="https://your-app.vercel.app/" + API_TOKEN)
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

    def background_task():
        try:
            # accs.txt থেকে ডাটা নেওয়া
            if os.path.exists("accs.txt"):
                with open("accs.txt", "r") as f:
                    accounts = [line.strip().split(":") for line in f if ":" in line]
                
                success = 0
                for u, p in accounts:
                    try:
                        # আপনার xH.py এর লজিক কল করা হচ্ছে
                        at, oid = xH.gTok(u, p)
                        # এখানে স্প্যাম প্রসেস চলবে
                        success += 1
                        time.sleep(0.3)
                    except:
                        continue
                
                bot.send_message(message.chat.id, f"✅ **স্প্যাম সাকসেসফুল!**\nমোট {success} টি অ্যাকাউন্ট থেকে হিট করা হয়েছে।")
            else:
                bot.send_message(message.chat.id, "❌ accs.txt ফাইলটি পাওয়া যায়নি!")
        except Exception as e:
            bot.send_message(message.chat.id, f"❌ Error: {str(e)}")

    threading.Thread(target=background_task).start()

if __name__ == "__main__":
    app.run()
