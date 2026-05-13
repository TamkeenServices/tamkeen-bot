from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# التوكن الخاص بك مضاف هنا بشكل صحيح
TOKEN = "8671174334:AAGkOq0kDya9p382zxhiTLtuSrYj8BVRrtY"

services_keyboard = [
    ["تصميم مواقع", "تطوير تطبيقات"],
    ["تصميم إعلانات", "برمجة بوتات"],
    ["إدارة صفحات", "خدمات أخرى"]
]

reply_markup = ReplyKeyboardMarkup(
    services_keyboard,
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_message = """
مرحباً بك في تمكين للخدمات الإلكترونية 🚀

نقدم لك:
• تصميم مواقع
• تطوير تطبيقات
• تصميم إعلانات
• برمجة بوتات
• إدارة صفحات

اختر الخدمة المطلوبة للبدء 👇
"""
    if update.message:
        await update.message.reply_text(
            welcome_message,
            reply_markup=reply_markup
        )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    response = f"""
✅ تم استلام طلبك:
{user_message}

سيتم التواصل معك قريباً من فريق تمكين.
"""
    if update.message:
        await update.message.reply_text(response)

# بناء التطبيق - تأكد من وجود .build() في النهاية
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

if __name__ == "__main__":
    print("Bot is running...")
    app.run_polling()
