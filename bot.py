import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
)

# إعدادات مراقبة الأخطاء
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# --- البيانات الخاصة بك ---
BOT_TOKEN = "8671174334:AAGkOq0kDya9p382zxhiTLtuSrYj8BVRrtY"
ADMIN_IDS = [8648717626, 8120387879]  # حسابك وحساب الأدمن الثاني

# مراحل المحادثة لتقديم الطلبات
CHOOSING_SERVICE, GETTING_DETAILS, GETTING_PHONE = range(3)

# --- دالة البداية /start ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        f"✨ **مرحباً بك في بوت شركة تمكين للخدمات الرقمية** ✨\n\n"
        f"نحن هنا لتلبية تطلعاتك التقنية وتطوير أعمالك.\n"
        f"فضلاً، اختر الخدمة التي ترغب بها من الأزرار أدناه للبدء:"
    )
    
    keyboard = [
        [InlineKeyboardButton("🌐 تصميم وتطوير المواقع", callback_data="service_web")],
        [InlineKeyboardButton("🤖 برمجة بوتات تليجرام الذكية", callback_data="service_bot")],
        [InlineKeyboardButton("🎨 التصميم الجرافيكي والهوية", callback_data="service_design")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

# --- بدء التفاعل عند اختيار خدمة ---
async def handle_services(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    services_map = {
        "service_web": "تصميم وتطوير المواقع",
        "service_bot": "برمجة بوتات تليجرام الذكية",
        "service_design": "التصميم الجرافيكي والهوية"
    }
    context.user_data['selected_service'] = services_map.get(query.data)
    
    await query.message.reply_text(
        f"لقد اخترت: **{context.user_data['selected_service']}**\n\n"
        f"الرجاء كتابة تفاصيل طلبك والمواصفات المطلوبة بدقة 👇:"
    )
    return CHOOSING_SERVICE

# --- استلام تفاصيل الخدمة ---
async def get_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['order_details'] = update.message.text
    await update.message.reply_text("🎯 ممتاز! الآن أرسل رقم هاتفك أو وسيلة التواصل المفضلة لديك:")
    return GETTING_PHONE

# --- إنهاء الطلب وإرساله للأدمنز مباشرة ---
async def get_phone_and_finish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['phone'] = update.message.text
    user = update.effective_user
    
    # رسالة للعميل
    await update.message.reply_text(
        "✅ **تم استلام طلبك بنجاح!**\n"
        "سيقوم فريق تمكين بمراجعة البيانات والتواصل معك سريعاً. شكراً لك! ✨"
    )

    # --- تحضير الإشعار الفوري للأدمنز ---
    admin_alert = (
        f"🚨 **طلب جديد لشركة تمكين**\n\n"
        f"👤 **العميل:** {user.full_name} (@{user.username})\n"
        f"🛠️ **الخدمة:** {context.user_data['selected_service']}\n"
        f"📝 **التفاصيل:** {context.user_data['order_details']}\n"
        f"📞 **التواصل:** {context.user_data['phone']}"
    )
    
    admin_buttons = [
        [
            InlineKeyboardButton("✅ قبول وتواصل", callback_data=f"approve_{user.id}"),
            InlineKeyboardButton("❌ رفض الطلب", callback_data=f"reject_{user.id}")
        ]
    ]
    
    # إرسال لكل الأدمنز (ستصلك بمجرد فتح الإنترنت في هاتفك)
    for admin_id in ADMIN_IDS:
        try:
            await context.bot.send_message(
                chat_id=admin_id, 
                text=admin_alert, 
                reply_markup=InlineKeyboardMarkup(admin_buttons),
                parse_mode="Markdown"
            )
        except Exception as e:
            logger.error(f"خطأ في الإرسال للأدمن {admin_id}: {e}")
    
    context.user_data.clear()
    return ConversationHandler.END

# --- التحكم بالطلبات (قبول/رفض) من قبل الأدمنز ---
async def handle_admin_actions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    action, client_id = query.data.split('_')

    if action == "approve":
        await query.edit_message_text(text=query.message.text + "\n\n🟢 **الإجراء الحالي:** تم قبول الطلب.")
        try:
            await context.bot.send_message(chat_id=int(client_id), text="🟢 **تحديث من تمكين:** تم قبول طلبك وجاري التواصل معك الآن.")
        except Exception:
            pass
            
    elif action == "reject":
        await query.edit_message_text(text=query.message.text + "\n\n🔴 **الإجراء الحالي:** تم رفض الطلب.")
        try:
            await context.bot.send_message(chat_id=int(client_id), text="🔴 **تحديث:** نعتذر منك، لم يتم قبول طلبك الحالي لعدم إمكانية التنفيذ حالياً.")
        except Exception:
            pass

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("تم إلغاء العملية.")
    context.user_data.clear()
    return ConversationHandler.END

def main():
    application = Application.builder().token(BOT_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(handle_services, pattern="^service_")] ,
        states={
            CHOOSING_SERVICE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_details)],
            GETTING_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone_and_finish)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(conv_handler)
    application.add_handler(CallbackQueryHandler(handle_admin_actions, pattern="^(approve_|reject_)"))

    application.run_polling()

if __name__ == '__main__':
    main()
