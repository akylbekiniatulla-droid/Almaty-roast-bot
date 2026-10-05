import telebot, requests, base64, os
TOKEN = os.environ.get("BOT_TOKEN")
GROQ_KEY = os.environ.get("GROQ_KEY")
bot = telebot.TeleBot(TOKEN)
print("✅ 24/7 READY")

@bot.message_handler(content_types=['photo'])
def handle_photo(m):
    try:
        bot.reply_to(m, "👀 Қарап жатырмын...")
        f = bot.get_file(m.photo[-1].file_id)
        d = bot.download_file(f.file_path)
        b64 = base64.b64encode(d).decode('utf-8')
        headers = {"Authorization": f"Bearer {GROQ_KEY}", "Content-Type": "application/json"}
        payload = {
            "model": "qwen/qwen3.8-27b",
            "messages": [{
                "role": "user",
                "content": [
                    {"type": "text", "text": "Look at photo, describe clothes, location (bridge at night). Roast in simple everyday Kazakh, 2 sentences, funny. No complex words."},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}}
                ]
            }],
            "max_tokens": 400
        }
        r = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, timeout=40)
        j = r.json()
        if "choices" in j:
            bot.reply_to(m, f"🔥 {j['choices'][0]['message']['content']}")
    except Exception as e:
        print(e)

bot.infinity_polling()
