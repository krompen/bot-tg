import sqlite3
import datetime
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

TOKEN = "8788493131:AAHEW8w-57mb1o_ogMMlWBl_QzJI62VG4FQ"
ADMIN_ID = 8032626504
ADMIN_USERNAME = "ciwige"
DB_NAME = "garant.db"

# ========== БАЗА ДАННЫХ ==========
def init_db():
    conn = sqlite3.connect(DB_NAME, timeout=10)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        full_name TEXT,
        registered_at TEXT,
        total_deals INTEGER DEFAULT 0
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS deals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        creator_id INTEGER,
        partner_id INTEGER,
        type TEXT,
        give_amount TEXT,
        give_currency TEXT,
        receive_amount TEXT,
        receive_currency TEXT,
        status TEXT DEFAULT 'waiting',
        created_at TEXT,
        confirmed_at TEXT,
        completed_at TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS deal_chats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        deal_id INTEGER,
        user_id INTEGER,
        username TEXT,
        message TEXT,
        created_at TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        text TEXT,
        created_at TEXT
    )''')
    conn.commit()
    conn.close()

init_db()

# ========== ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ==========
def add_user(user_id, username, full_name):
    try:
        conn = sqlite3.connect(DB_NAME, timeout=10)
        c = conn.cursor()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute('INSERT OR IGNORE INTO users (user_id, username, full_name, registered_at) VALUES (?, ?, ?, ?)',
                  (user_id, username, full_name, now))
        conn.commit()
        conn.close()
        return True
    except:
        return False

def get_user(user_id):
    conn = sqlite3.connect(DB_NAME, timeout=10)
    c = conn.cursor()
    c.execute('SELECT user_id, username, full_name, registered_at, total_deals FROM users WHERE user_id = ?', (user_id,))
    user = c.fetchone()
    conn.close()
    return user

def get_deal(deal_id):
    conn = sqlite3.connect(DB_NAME, timeout=10)
    c = conn.cursor()
    c.execute('SELECT id, creator_id, partner_id, type, give_amount, give_currency, receive_amount, receive_currency, status, created_at, confirmed_at, completed_at FROM deals WHERE id = ?', (deal_id,))
    deal = c.fetchone()
    conn.close()
    return deal

def get_user_deals(user_id):
    conn = sqlite3.connect(DB_NAME, timeout=10)
    c = conn.cursor()
    c.execute('SELECT id, type, give_amount, give_currency, receive_amount, receive_currency, status FROM deals WHERE creator_id = ? OR partner_id = ? ORDER BY id DESC', (user_id, user_id))
    deals = c.fetchall()
    conn.close()
    return deals

def create_deal(creator_id, deal_type, give_amount, give_currency, receive_amount, receive_currency):
    try:
        conn = sqlite3.connect(DB_NAME, timeout=10)
        c = conn.cursor()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute('INSERT INTO deals (creator_id, type, give_amount, give_currency, receive_amount, receive_currency, status, created_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                  (creator_id, deal_type, give_amount, give_currency, receive_amount, receive_currency, 'waiting', now))
        deal_id = c.lastrowid
        conn.commit()
        conn.close()
        return deal_id
    except:
        return None

def update_deal_status(deal_id, status, partner_id=None):
    try:
        conn = sqlite3.connect(DB_NAME, timeout=10)
        c = conn.cursor()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if partner_id:
            c.execute('UPDATE deals SET status = ?, partner_id = ?, confirmed_at = ? WHERE id = ?', (status, partner_id, now, deal_id))
        else:
            c.execute('UPDATE deals SET status = ?, completed_at = ? WHERE id = ?', (status, now, deal_id))
        conn.commit()
        conn.close()
        return True
    except:
        return False

def add_chat_message(deal_id, user_id, username, message):
    try:
        conn = sqlite3.connect(DB_NAME, timeout=10)
        c = conn.cursor()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute('INSERT INTO deal_chats (deal_id, user_id, username, message, created_at) VALUES (?, ?, ?, ?, ?)',
                  (deal_id, user_id, username, message, now))
        conn.commit()
        conn.close()
        return True
    except:
        return False

def get_chat_messages(deal_id, limit=30):
    conn = sqlite3.connect(DB_NAME, timeout=10)
    c = conn.cursor()
    c.execute('SELECT user_id, username, message, created_at FROM deal_chats WHERE deal_id = ? ORDER BY id DESC LIMIT ?', (deal_id, limit))
    messages = c.fetchall()
    conn.close()
    return messages[::-1]

def add_broadcast_message(user_id, text):
    try:
        conn = sqlite3.connect(DB_NAME, timeout=10)
        c = conn.cursor()
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute('INSERT INTO messages (user_id, text, created_at) VALUES (?, ?, ?)', (user_id, text, now))
        conn.commit()
        conn.close()
        return True
    except:
        return False

def get_all_users():
    conn = sqlite3.connect(DB_NAME, timeout=10)
    c = conn.cursor()
    users = c.execute('SELECT user_id FROM users').fetchall()
    conn.close()
    return users

# ========== КЛАВИАТУРЫ ==========
def main_keyboard():
    keyboard = [
        [InlineKeyboardButton("🆕 Новая сделка", callback_data="new_deal")],
        [InlineKeyboardButton("📋 Мои сделки", callback_data="my_deals")],
        [InlineKeyboardButton("💬 Поддержка", callback_data="support")],
        [InlineKeyboardButton("ℹ️ Инфо", callback_data="info")]
    ]
    return InlineKeyboardMarkup(keyboard)

def deal_type_keyboard():
    keyboard = [
        [InlineKeyboardButton("💰 Деньги → Деньги", callback_data="deal_type_money_money")],
        [InlineKeyboardButton("🖼️ Деньги → NFT", callback_data="deal_type_money_nft")],
        [InlineKeyboardButton("🖼️ NFT → Деньги", callback_data="deal_type_nft_money")],
        [InlineKeyboardButton("🖼️ NFT → NFT", callback_data="deal_type_nft_nft")],
        [InlineKeyboardButton("🎭 Услуга → Деньги", callback_data="deal_type_service_money")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back")]
    ]
    return InlineKeyboardMarkup(keyboard)

def currency_keyboard(prefix):
    keyboard = [
        [InlineKeyboardButton("⭐ Telegram Stars", callback_data=f"{prefix}_stars")],
        [InlineKeyboardButton("💎 TON", callback_data=f"{prefix}_ton")],
        [InlineKeyboardButton("💰 RUB", callback_data=f"{prefix}_rub")],
        [InlineKeyboardButton("💵 USD", callback_data=f"{prefix}_usd")],
        [InlineKeyboardButton("🔙 Назад", callback_data=f"{prefix}_back")]
    ]
    return InlineKeyboardMarkup(keyboard)

def admin_keyboard():
    keyboard = [
        [InlineKeyboardButton("📊 Статистика", callback_data="admin_stats")],
        [InlineKeyboardButton("📢 Рассылка", callback_data="admin_broadcast")],
        [InlineKeyboardButton("🆘 Тикеты", callback_data="admin_tickets")],
        [InlineKeyboardButton("🔧 Тестовые сделки", callback_data="admin_test")],
        [InlineKeyboardButton("🔙 Назад", callback_data="back")]
    ]
    return InlineKeyboardMarkup(keyboard)

def deal_actions_keyboard(deal_id, status):
    keyboard = []
    if status == "waiting":
        keyboard.append([InlineKeyboardButton("✅ Принять сделку", callback_data=f"accept_deal_{deal_id}")])
        keyboard.append([InlineKeyboardButton("❌ Отклонить", callback_data=f"reject_deal_{deal_id}")])
    elif status == "active":
        keyboard.append([InlineKeyboardButton("💰 Оплатил", callback_data=f"paid_deal_{deal_id}")])
        keyboard.append([InlineKeyboardButton("📦 Отправил", callback_data=f"sent_deal_{deal_id}")])
    elif status == "paid" or status == "sent":
        keyboard.append([InlineKeyboardButton("✅ Подтвердить получение", callback_data=f"confirm_receipt_{deal_id}")])
    keyboard.append([InlineKeyboardButton("💬 Чат сделки", callback_data=f"chat_{deal_id}")])
    keyboard.append([InlineKeyboardButton("⚠️ Спор", callback_data=f"dispute_{deal_id}")])
    keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data="back")])
    return InlineKeyboardMarkup(keyboard)

# ========== КОМАНДЫ ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    add_user(user.id, user.username, user.full_name)
    await update.message.reply_text(
        f"👋 Привет, {user.first_name}!\n\n"
        f"🔥 **Ciwige Garant Bot** — твой надёжный гарант для любых сделок!\n\n"
        f"📌 **Что я умею:**\n"
        f"• Безопасные сделки между людьми\n"
        f"• Поддержка крипты, звёзд и фиата\n"
        f"• Встроенный чат в каждой сделке\n"
        f"• Споры и их разрешение\n"
        f"• Админ @{ADMIN_USERNAME} всегда на связи\n\n"
        f"🔒 Все сделки защищены, деньги не уходят, пока обе стороны не подтвердят.\n\n"
        f"👇 **Начни с кнопки «Новая сделка»**",
        reply_markup=main_keyboard()
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer()
    user_id = query.from_user.id
    user = get_user(user_id)
    
    if data == "new_deal":
        await query.edit_message_text("📝 **Выбери тип сделки:**", reply_markup=deal_type_keyboard())
    
    elif data.startswith("deal_type_"):
        deal_type = data.replace("deal_type_", "")
        context.user_data["deal_type"] = deal_type
        await query.edit_message_text(f"📝 **Ты выбрал: {deal_type.replace('_', ' → ')}**\n\n💰 Что ты отдаёшь? (сумму и валюту через пробел)\nПример: `100 stars`", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Назад", callback_data="new_deal")]]))
        context.user_data["awaiting_give"] = True
    
    elif data == "my_deals":
        deals = get_user_deals(user_id)
        if not deals:
            await query.edit_message_text("📭 У тебя пока нет сделок.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Назад", callback_data="back")]]))
            return
        text = "📋 **Твои сделки:**\n\n"
        for deal in deals:
            status_emoji = {"waiting": "⏳", "active": "🔄", "paid": "💰", "sent": "📦", "completed": "✅", "disputed": "⚠️", "cancelled": "❌"}.get(deal[6], "❓")
            text += f"{status_emoji} **Сделка #{deal[0]}**\n{deal[1]} | {deal[2]} {deal[3]} → {deal[4]} {deal[5]}\n\n"
        keyboard = []
        for deal in deals:
            keyboard.append([InlineKeyboardButton(f"📦 Сделка #{deal[0]}", callback_data=f"deal_{deal[0]}")])
        keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data="back")])
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    
    elif data.startswith("deal_"):
        deal_id = int(data.split("_")[1])
        deal = get_deal(deal_id)
        if not deal:
            await query.edit_message_text("❌ Сделка не найдена.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Назад", callback_data="back")]]))
            return
        status_emoji = {"waiting": "⏳ Ожидает", "active": "🔄 Активна", "paid": "💰 Оплачено", "sent": "📦 Отправлено", "completed": "✅ Завершена", "disputed": "⚠️ Спор", "cancelled": "❌ Отменена"}.get(deal[8], "❓")
        text = (
            f"📦 **Сделка #{deal[0]}**\n\n"
            f"📝 Тип: {deal[3]}\n"
            f"📤 Отдаёт: {deal[4]} {deal[5]}\n"
            f"📥 Получает: {deal[6]} {deal[7]}\n"
            f"📅 Создана: {deal[9]}\n"
            f"🔹 Статус: {status_emoji}\n"
        )
        await query.edit_message_text(text, reply_markup=deal_actions_keyboard(deal_id, deal[8]))
    
    elif data.startswith("accept_deal_"):
        deal_id = int(data.split("_")[2])
        deal = get_deal(deal_id)
        if not deal or deal[8] != "waiting":
            await query.edit_message_text("❌ Сделка недоступна для принятия.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Назад", callback_data="back")]]))
            return
        update_deal_status(deal_id, "active", user_id)
        await query.edit_message_text("✅ Сделка принята! Теперь ожидайте оплаты/передачи от создателя.")
        await context.bot.send_message(chat_id=deal[1], text=f"✅ Пользователь @{query.from_user.username} принял вашу сделку #{deal_id}!")
    
    elif data == "support":
        await query.edit_message_text(
            f"🆘 **Поддержка**\n\n"
            f"По всем вопросам пиши админу: @{ADMIN_USERNAME}\n\n"
            f"✏️ Напиши сюда сообщение, я передам админу.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Назад", callback_data="back")]])
        )
        context.user_data["awaiting_ticket"] = True
    
    elif data == "info":
        await query.edit_message_text(
            f"ℹ️ **О боте**\n\n"
            f"🤖 **Ciwige Garant Bot** — твой надёжный гарант для любых сделок.\n\n"
            f"🔒 Как это работает:\n"
            f"1. Ты создаёшь сделку\n"
            f"2. Вторая сторона принимает\n"
            f"3. Ты передаёшь деньги/NFT/услугу\n"
            f"4. Вторая сторона подтверждает получение\n"
            f"5. Сделка завершена!\n\n"
            f"💎 Поддерживаются: Telegram Stars, TON, RUB, USD, NFT, услуги\n\n"
            f"👑 Админ: @{ADMIN_USERNAME}\n"
            f"📢 Канал: @Ciwige_search",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Назад", callback_data="back")]])
        )
    
    elif data == "admin":
        if user_id != ADMIN_ID:
            await query.edit_message_text("⛔ Нет доступа.")
            return
        await query.edit_message_text("👑 **Админ-панель**", reply_markup=admin_keyboard())
    
    elif data == "admin_stats":
        if user_id != ADMIN_ID:
            return
        conn = sqlite3.connect(DB_NAME, timeout=10)
        c = conn.cursor()
        total_users = c.execute('SELECT COUNT(*) FROM users').fetchone()[0]
        total_deals = c.execute('SELECT COUNT(*) FROM deals').fetchone()[0]
        completed_deals = c.execute('SELECT COUNT(*) FROM deals WHERE status = "completed"').fetchone()[0]
        active_deals = c.execute('SELECT COUNT(*) FROM deals WHERE status = "active"').fetchone()[0]
        conn.close()
        await query.edit_message_text(
            f"📊 **Статистика**\n\n"
            f"👥 Всего пользователей: {total_users}\n"
            f"📦 Всего сделок: {total_deals}\n"
            f"✅ Завершено: {completed_deals}\n"
            f"🔄 Активно: {active_deals}",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Назад", callback_data="admin")]])
        )
    
    elif data == "admin_broadcast":
        if user_id != ADMIN_ID:
            return
        await query.edit_message_text("📢 **Рассылка**\n\nВведи текст для рассылки всем пользователям:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Назад", callback_data="admin")]]))
        context.user_data["awaiting_broadcast"] = True
    
    elif data == "admin_tickets":
        if user_id != ADMIN_ID:
            return
        await query.edit_message_text("🆘 **Тикеты**\n\nСписок обращений будет здесь.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Назад", callback_data="admin")]]))
    
    elif data == "admin_test":
        if user_id != ADMIN_ID:
            return
        create_deal(ADMIN_ID, "test", "10", "stars", "Тестовый NFT", "nft")
        await query.edit_message_text("✅ Создана тестовая сделка для проверки.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Назад", callback_data="admin")]]))
    
    elif data.startswith("chat_"):
        deal_id = int(data.split("_")[1])
        deal = get_deal(deal_id)
        if not deal or (user_id != deal[1] and user_id != deal[2] and user_id != ADMIN_ID):
            await query.edit_message_text("❌ Нет доступа к этому чату.")
            return
        messages = get_chat_messages(deal_id)
        if messages:
            text = f"💬 **Чат сделки #{deal_id}**\n\n"
            for msg in messages:
                text += f"👤 @{msg[1]}: {msg[2]}\n📅 {msg[3]}\n\n"
        else:
            text = f"💬 **Чат сделки #{deal_id}**\n\nСообщений пока нет."
        await query.edit_message_text(text[:4000], reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📝 Написать", callback_data=f"write_chat_{deal_id}")], [InlineKeyboardButton("🔙 Назад", callback_data=f"deal_{deal_id}")]]))
    
    elif data.startswith("write_chat_"):
        deal_id = int(data.split("_")[2])
        context.user_data["chat_deal_id"] = deal_id
        await query.edit_message_text("✏️ Введи сообщение для чата сделки:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Назад", callback_data=f"chat_{deal_id}")]]))
        context.user_data["awaiting_chat_message"] = True
    
    elif data == "back":
        await start(update, context)

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    
    if context.user_data.get("awaiting_give"):
        try:
            parts = text.split()
            amount = parts[0]
            currency = parts[1]
            context.user_data["give_amount"] = amount
            context.user_data["give_currency"] = currency
            context.user_data["awaiting_give"] = False
            context.user_data["awaiting_receive"] = True
            await update.message.reply_text(f"📥 Что ты получаешь? (сумму и валюту через пробел)\nПример: `50 ton`")
        except:
            await update.message.reply_text("❌ Неверный формат. Введи сумму и валюту через пробел.\nПример: `100 stars`")
    
    elif context.user_data.get("awaiting_receive"):
        try:
            parts = text.split()
            amount = parts[0]
            currency = parts[1]
            deal_type = context.user_data.get("deal_type")
            give_amount = context.user_data.get("give_amount")
            give_currency = context.user_data.get("give_currency")
            deal_id = create_deal(user_id, deal_type, give_amount, give_currency, amount, currency)
            if deal_id:
                await update.message.reply_text(f"✅ Сделка #{deal_id} создана! Теперь нужно, чтобы вторая сторона приняла её.\n\nПоделись ID сделки с партнёром: `/deal_{deal_id}`", reply_markup=main_keyboard())
            else:
                await update.message.reply_text("❌ Ошибка при создании сделки.")
            context.user_data["awaiting_receive"] = False
            context.user_data["deal_type"] = None
            context.user_data["give_amount"] = None
            context.user_data["give_currency"] = None
        except:
            await update.message.reply_text("❌ Неверный формат.")
    
    elif context.user_data.get("awaiting_broadcast") and user_id == ADMIN_ID:
        users = get_all_users()
        sent = 0
        for user in users:
            try:
                await context.bot.send_message(chat_id=user[0], text=f"📢 **РАССЫЛКА ОТ АДМИНА**\n\n{text}")
                sent += 1
            except:
                pass
        await update.message.reply_text(f"✅ Рассылка отправлена {sent} пользователям.")
        context.user_data["awaiting_broadcast"] = False
    
    elif context.user_data.get("awaiting_ticket"):
        await update.message.reply_text("✅ Сообщение отправлено! Админ ответит в ближайшее время.")
        await context.bot.send_message(chat_id=ADMIN_ID, text=f"🆕 **Новое сообщение в поддержку**\n👤 @{update.effective_user.username} (ID: {user_id})\n📝 {text}")
        context.user_data["awaiting_ticket"] = False
    
    elif context.user_data.get("awaiting_chat_message"):
        deal_id = context.user_data.get("chat_deal_id")
        if deal_id:
            add_chat_message(deal_id, user_id, update.effective_user.username or str(user_id), text)
            await update.message.reply_text("✅ Сообщение отправлено в чат сделки.")
            # Уведомляем другого участника
            deal = get_deal(deal_id)
            if deal:
                other_id = deal[2] if deal[1] == user_id else deal[1]
                if other_id:
                    try:
                        await context.bot.send_message(chat_id=other_id, text=f"💬 Новое сообщение в чате сделки #{deal_id}\n👤 @{update.effective_user.username}: {text[:50]}...")
                    except:
                        pass
        context.user_data["awaiting_chat_message"] = False

async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("⛔ Нет прав.")
        return
    text = " ".join(context.args)
    if not text:
        await update.message.reply_text("❌ /broadcast <текст>")
        return
    users = get_all_users()
    sent = 0
    for user in users:
        try:
            await context.bot.send_message(chat_id=user[0], text=f"📢 **РАССЫЛКА ОТ АДМИНА**\n\n{text}")
            sent += 1
        except:
            pass
    await update.message.reply_text(f"✅ Рассылка отправлена {sent} пользователям.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("broadcast", broadcast_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("✅ Ciwige Garant Bot запущен")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()