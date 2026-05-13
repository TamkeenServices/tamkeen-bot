import os
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# 🔐 المتغيرات
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 8648717626  # رقمك (الإدمن)

PORT = int(os.environ.get("PORT", 8080))

# 🧠 إعدادات الأداء (توفير موارد)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.WARNING
)

# 📋 لوحة الخدمات
services_keyboard = [
    ["تصميم مواقع", "تطوير تطبيقات"],
    ["تصميم إعلانات", "برمجة بوتات"],
    ["إدارة صفحات", "خدمات أخرى"]
]

reply_markup = ReplyKeyboardMarkup(
    services_keyboard,
    resize_keyboard=True
)

# 🚀 /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        """
مرحباً بك في تمكين للخدمات الإلكترونية 🚀

اختر الخدمة المطلوبة 👇
        """,
        reply_markup=reply_markup
    )

# 📩 استقبال الطلبات
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text

    # ✅ رد للعميل
    await update.message.reply_text(
        "✅ تم استلام طلبك، سيتم التواصل معك قريباً من فريق تمكين."
    )

    # 📢 إشعار للإدمن
    admin_message = f"""
🆕 طلب جديد - تمكين

👤 الاسم: @{user.username if user.username else 'بدون يوزر'}
🆔 ID: {user.id}

🧾 الخدمة:
{text}
"""

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=admin_message
    )

# 📊 لوحة إدمن بسيطة
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.chat_id != ADMIN_ID:
        return

    await update.message.reply_text(
        """
📊 لوحة تمكين للإدارة

الأوامر:
- /admin → لوحة التحكم
- /start → اختبار البوت

🚀 النظام يعمل بشكل طبيعي
        """
    )

# 🧠 تشغيل Webhook
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_panel))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=os.environ.get("WEBHOOK_URL")
    )

    print("Bot is running (Webhook Mode)...")

if __name__ == "__main__":
    main()