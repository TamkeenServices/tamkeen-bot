import os
import logging
import subprocess

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)

# ==============================
# 🔐 الإعدادات الأساسية
# ==============================

TOKEN = os.getenv("BOT_TOKEN")

# رقم الإدمن الخاص بك
ADMIN_ID = 8648717626

# رابط الـ Webhook من Railway
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

# المنفذ الخاص بـ Railway
PORT = int(os.environ.get("PORT", 8080))

# ==============================
# ⚡ تحسين الأداء وتقليل الاستهلاك
# ==============================

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.WARNING
)

# ==============================
# 📋 لوحة الخدمات
# ==============================

services_keyboard = [
    ["تصميم مواقع", "تطوير تطبيقات"],
    ["تصميم إعلانات", "برمجة بوتات"],
    ["إدارة صفحات", "خدمات أخرى"]
]

reply_markup = ReplyKeyboardMarkup(
    services_keyboard,
    resize_keyboard=True
)

# ==============================
# 🚀 رسالة البداية
# ==============================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    welcome_message = """
🚀 مرحباً بك في تمكين للخدمات الإلكترونية

نقدم لك خدمات احترافية تشمل:

• تصميم مواقع إلكترونية
• تطوير تطبيقات
• برمجة بوتات تيليجرام
• تصميم إعلانات احترافية
• إدارة صفحات السوشيال ميديا

📩 اختر الخدمة المطلوبة للبدء 👇
"""

    await update.message.reply_text(
        welcome_message,
        reply_markup=reply_markup
    )

# ==============================
# 📩 استقبال رسائل العملاء
# ==============================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.message.from_user
    text = update.message.text

    # ✅ رد تلقائي للعميل
    await update.message.reply_text(
        "✅ تم استلام طلبك بنجاح.\nسيتم التواصل معك قريباً من فريق تمكين."
    )

    # 📢 إرسال الطلب للإدمن
    admin_message = f"""
🆕 طلب جديد - تمكين

👤 الاسم:
{user.full_name}

📛 اليوزر:
@{user.username if user.username else 'لا يوجد'}

🆔 ID:
{user.id}

🧾 الطلب:
{text}
"""

    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=admin_message
    )

# ==============================
# 📊 لوحة الإدارة
# ==============================

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.chat_id != ADMIN_ID:
        return

    admin_text = """
📊 لوحة تحكم تمكين

الأوامر المتاحة:

/admin → لوحة الإدارة
/update → تحديث البوت
/restart → إعادة تشغيل البوت
/status → حالة النظام

✅ النظام يعمل بشكل طبيعي
"""

    await update.message.reply_text(admin_text)

# ==============================
# 🔄 تحديث البوت من GitHub
# ==============================

async def update_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.chat_id

    if user_id != ADMIN_ID:
        await update.message.reply_text(
            "❌ غير مصرح لك باستخدام هذا الأمر."
        )
        return

    await update.message.reply_text(
        "🔄 جاري تحديث النظام..."
    )

    try:

        result = subprocess.run(
            ["git", "pull"],
            capture_output=True,
            text=True
        )

        output = result.stdout + result.stderr

        await update.message.reply_text(
            f"✅ تم التحديث بنجاح:\n\n{output}"
        )

        # إعادة تشغيل
        os._exit(0)

    except Exception as e:

        await update.message.reply_text(
            f"❌ خطأ أثناء التحديث:\n{str(e)}"
        )

# ==============================
# 🔁 إعادة تشغيل البوت
# ==============================

async def restart_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.chat_id != ADMIN_ID:
        return

    await update.message.reply_text(
        "♻️ جاري إعادة تشغيل البوت..."
    )

    os._exit(0)

# ==============================
# 📡 حالة النظام
# ==============================

async def system_status(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.message.chat_id != ADMIN_ID:
        return

    status_text = """
🟢 حالة النظام

✅ البوت يعمل
✅ Webhook متصل
✅ Railway يعمل
✅ نظام تمكين نشط
"""

    await update.message.reply_text(status_text)

# ==============================
# 🚀 تشغيل النظام
# ==============================

def main():

    app = ApplicationBuilder().token(TOKEN).build()

    # الأوامر
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_panel))
    app.add_handler(CommandHandler("update", update_bot))
    app.add_handler(CommandHandler("restart", restart_bot))
    app.add_handler(CommandHandler("status", system_status))

    # استقبال الرسائل
    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    # تشغيل Webhook
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        webhook_url=WEBHOOK_URL
    )

# ==============================
# ▶️ بدء التشغيل
# ==============================

if __name__ == "__main__":
    print("🚀 Tamkeen Bot Running...")
    main()