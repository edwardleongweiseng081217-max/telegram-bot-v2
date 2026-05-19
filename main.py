from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import random
import os

TOKEN = os.getenv("TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

if not TOKEN:
    raise ValueError("TOKEN 没有在环境变量中找到")

if ADMIN_ID:
    ADMIN_ID = int(ADMIN_ID)

menu_keyboard = [
    ["🔗 Mega资源菜单链接"],
    ["💳 付款入口"],
    ["📩 我已付款（提交截图）"],
    ["💬 联系客服"]
]

reply_markup = ReplyKeyboardMarkup(menu_keyboard, resize_keyboard=True)

user_orders = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 欢迎使用系统\n请选择功能：",
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    print("运行目录:", os.getcwd())
    print("文件列表:", os.listdir())

    text = update.message.text
    user_id = update.message.from_user.id
    username = update.message.from_user.username

    if text == "🔗 Mega资源菜单链接":
        await update.message.reply_text(
            "🔗 Mega资源菜单链接\n"
            "一套只需 RM2 - RM5\n"
            "全场买三送一\n"
            "付款后自带收据和资源编号等待拿货\n\n"
            "https://drive.google.com/drive/folders/19BAUT4mxa8UiyZ1tN5tkc4WXf4cDS7j7"
        )

    elif text == "💳 付款入口":

        order_id = str(random.randint(10000, 99999))
        user_orders[user_id] = order_id

        qr_path = os.path.join(os.path.dirname(__file__), "qr.jpg")

        if not os.path.exists(qr_path):
            await update.message.reply_text("❌ 找不到 qr.jpg")
            return

        with open(qr_path, "rb") as photo:
            await update.message.reply_photo(
                photo=photo,
                caption=f"""
💳 付款入口

🧾 订单号：{order_id}
💰 金额：RM2 - RM100

付款后请点击：
📩 我已付款（提交截图）
"""
            )

    elif text == "📩 我已付款（提交截图）":
        await update.message.reply_text("📤 请发送付款截图")

    elif text == "💬 联系客服":
        await update.message.reply_text("💬 客服：@kaoyu_4ever")

    elif update.message.photo:

        order_id = user_orders.get(user_id, "未知订单")
        photo_file_id = update.message.photo[-1].file_id

        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=photo_file_id,
            caption=f"""
📥 新付款截图

👤 用户ID：{user_id}
📛 Username：@{username}
🧾 订单号：{order_id}
"""
        )

        await update.message.reply_text("✅ 已收到截图")

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL, handle_message))

    print("Bot 已启动...")
    app.run_polling()

if __name__ == "__main__":
    main()