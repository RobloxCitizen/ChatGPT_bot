import openai
from telegram import Update, BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes
import config

OPENAI_API_KEY = config.OPENAI_API_KEY
TELEGRAM_TOKEN = config.TELEGRAM_TOKEN

client = openai.OpenAI(api_key=OPENAI_API_KEY)

HELP_TEXT = """
<b>О боте</b>
Бот работает через официальный API ChatGPT от OpenAI последней версии.

https://openai.ru/terms
https://openai.ru/privacy
"""
START_TEXT = """
Это бот для работы с актуальной моделью нейросети в Telegram. Чтобы задать вопрос, просто напишите его.

<b>Команды</b>
/start - перезапуск
/help - помощь
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(START_TEXT, parse_mode="HTML")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HELP_TEXT, parse_mode="HTML")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.text and not update.message.text.startswith('/'):
        user_message = update.message.text
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": user_message}]
            )
            await update.message.reply_text(response.choices[0].message.content)
        except openai.PermissionDeniedError:
            await update.message.reply_text("Ошибка: API недоступен в вашем регионе. Используйте VPN или проверьте настройки OpenAI.", parse_mode="HTML")

async def set_menu(application: Application):
    commands = [
        BotCommand("start", "перезапуск"),
        BotCommand("help", "помощь")
    ]
    await application.bot.set_my_commands(commands)

if __name__ == "__main__":
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(None, handle_message))
    
    app.post_init = set_menu
    
    app.run_polling()