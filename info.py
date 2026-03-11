import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = "8156884296:AAFbjirMTKwuJMWf1wGc6tY9VherD2DTaGI"
CHANNEL = "@rose_x_07_bot"

user_state = {}

async def check_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.id
    try:
        member = await context.bot.get_chat_member(CHANNEL, user)
        if member.status in ["member", "administrator", "creator"]:
            return True
        else:
            return False
    except:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not await check_join(update, context):
        join_button = [[InlineKeyboardButton("Join Channel", url="https://t.me/rose_x_07_bot")]]
        await update.message.reply_text(
            "❌ First Join Our Channel",
            reply_markup=InlineKeyboardMarkup(join_button)
        )
        return

    keyboard = [
        [InlineKeyboardButton("1️⃣ Number Information", callback_data="number")],
        [InlineKeyboardButton("2️⃣ Vehicle Information", callback_data="vehicle")]
    ]

    await update.message.reply_text(
        "🔥 Welcome\n\nSelect Option",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "number":
        user_state[query.from_user.id] = "number"
        await query.message.reply_text("📱 Send Mobile Number")

    elif query.data == "vehicle":
        user_state[query.from_user.id] = "vehicle"
        await query.message.reply_text("🚗 Send Vehicle RC Number")

async def message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.effective_user.id
    text = update.message.text

    if user not in user_state:
        return

    mode = user_state[user]

    if mode == "number":
        api = f"https://number-to-owner.vercel.app/info?name={text}"

    elif mode == "vehicle":
        api = f"https://new-vehicle-api-eosin.vercel.app/vehicle?rc={text}"

    try:
        res = requests.get(api)
        data = res.json()

        await update.message.reply_text(f"✅ Result\n\n{data}")

    except:
        await update.message.reply_text("❌ API Error")

def main():

    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))

    app.run_polling()

if __name__ == "__main__":
    main()