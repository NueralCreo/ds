import telebot
import openai
from openai import OpenAI
import requests

# Telegram Bot Token
TELEGRAM_TOKEN = '7940180798:AAGgwnho4J4Pw53SKm_SvqwhrbjWIrgxu0w'

# NeuralCore API Config
client = OpenAI(
    api_key="NeuralCoreUNLIMITED1T",
    base_url="https://api.neuralcore.org/api/openai/n"
)

bot = telebot.TeleBot(TELEGRAM_TOKEN)

user_histories = {}

@bot.message_handler(commands=['start', 'hello'])
def welcome(message):
    bot.reply_to(message, "Hey jaan 💖 I'm Neura. Type anything and I’ll talk back — in my voice too 😘")

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    user_id = message.chat.id
    user_msg = message.text.strip()

    history = user_histories.get(user_id, [])
    history.append({"role": "user", "content": user_msg})

    try:
        # Send chat completion request with voice
        response = client.chat.completions.create(
            model="neura-3.5-aala",
            messages=history[-10:],
            temperature=0.7,
            max_tokens=300,
            extra_body={
                "voice": "luna"
            }
        )

        choice = response.choices[0]
        neura_reply = choice.message.content

        # ✅ Get audio URL correctly
        audio_url = getattr(choice, "audio_url", None)
        if not audio_url:
            audio_url = getattr(response, "audio_url", None)  # just in case it’s returned at top level

        history.append({"role": "assistant", "content": neura_reply})
        user_histories[user_id] = history

        # Send reply
        bot.send_message(user_id, neura_reply)

        # Send voice note if available
        if audio_url:
            audio_data = requests.get(audio_url)
            if audio_data.status_code == 200:
                with open("voice_note.ogg", "wb") as f:
                    f.write(audio_data.content)
                with open("voice_note.ogg", "rb") as voice_file:
                    bot.send_voice(user_id, voice_file)
            else:
                bot.send_message(user_id, "🎤 Voice note couldn’t load right now, but I’m here typing 🫶")

    except Exception as e:
        bot.send_message(user_id, f"❌ Oops! Something broke:\n{str(e)}")

# Let the magic happen
print("🎙️ Neura is online, speaking and vibing...")
bot.infinity_polling()
