"""
╔══════════════════════════════════════════════════╗
║   BLITEX GREET BOT — Smart Group Greeting Bot    ║
║   Railway Ready | 24/7 Online                    ║
║   pip install pyTelegramBotAPI schedule requests ║
╚══════════════════════════════════════════════════╝
"""

import telebot, json, os, time, logging, random, threading, schedule
from datetime import datetime

# ══════════════════════════════════════════
#  CONFIG
# ══════════════════════════════════════════
TOKEN        = "YOUR_BOT_TOKEN_HERE"   # ← From @BotFather
BOT_USERNAME = "YourBotUsername"        # ← Without @
OWNER_ID     = 8873676178
BRAND        = "BLITEX"
DATA_FILE    = "greet_data.json"
QUOTE_HOUR   = 8   # Send daily quote at 8 AM
QUOTE_MINUTE = 0

bot = telebot.TeleBot(TOKEN, parse_mode=None)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

# ══════════════════════════════════════════
#  TRIGGERS (English + Hindi)
# ══════════════════════════════════════════
MORNING_WORDS   = ["good morning","gm","good mrng","gud morning","gd morning",
                   "goodmorning","morning","subah","suprabhat","शुभ प्रभात","सुप्रभात"]
AFTERNOON_WORDS = ["good afternoon","afternoon","gud afternoon","goodafternoon"]
EVENING_WORDS   = ["good evening","evening","gud evening","goodevening","sham","शुभ संध्या"]
NIGHT_WORDS     = ["good night","gn","good nite","gud night","goodnight",
                   "night","shubh ratri","शुभ रात्रि","raat","गुड नाईट"]
BIRTHDAY_WORDS  = ["happy birthday","hbd","hb","birthday","bday",
                   "happy bday","janamdin","जन्मदिन मुबारक","bd"]

# ══════════════════════════════════════════
#  RESPONSES — multiple so it never repeats
# ══════════════════════════════════════════
MORNING_REPLIES = [
    "🌅 Good Morning {name}! ☀️\nWishing you a wonderful day ahead!\nStay positive, stay blessed! 💪",
    "🌄 Rise and shine {name}! 🌟\nGood Morning! May this day bring\nyou joy and success! 😊✨",
    "☀️ Good Morning {name}! 🌻\nA new day, a new chance to be amazing!\nGo crush it today! 🔥💯",
    "🌞 Wakey wakey {name}! 😄\nGood Morning! The world needs your\nenergy today! Let's go! 🚀",
    "🌅 Good Morning {name}! 🙏\nMay Allah bless your day with\nhappiness and health! Ameen 💫",
]
AFTERNOON_REPLIES = [
    "🌆 Good Afternoon {name}! ☀️\nHope your morning was productive!\nKeep the energy going! 💪",
    "🌤 Good Afternoon {name}! 😊\nHalfway through the day — you're doing great!\nStay focused! 🎯",
    "☀️ Good Afternoon {name}! 🌼\nTake a little break and recharge!\nYou've got this! 💯",
]
EVENING_REPLIES = [
    "🌇 Good Evening {name}! 🌙\nHope you had a great day!\nTime to relax and unwind! 😌✨",
    "🌆 Good Evening {name}! 🍵\nThe day is almost done — proud of you!\nEnjoy your evening! 🌟",
    "🌃 Good Evening {name}! 😊\nSit back, relax and enjoy\nthis beautiful evening! 🌸",
]
NIGHT_REPLIES = [
    "🌙 Good Night {name}! 😴⭐\nSweet dreams! Rest well and\nwake up refreshed tomorrow! 💤",
    "🌛 Good Night {name}! 🌟\nTime to recharge! Tomorrow is\nanother chance to shine! ✨😴",
    "💤 Good Night {name}! 🌙\nMay you have the most peaceful\nsleep tonight! Sweet dreams! 🌸",
    "🌙 Good Night {name}! 😊\nTake rest, you deserve it!\nSee you tomorrow! 💫",
]
BIRTHDAY_REPLIES = [
    "🎂 Happy Birthday {name}! 🎉🎊\n🎈🎈🎈🎈🎈🎈🎈🎈🎈\nMay this year bring you\njoy, success and love! 🥳🎁\n━━━━━━━━━━━━━━━\n🎶 HBD to you! 🎶",
    "🎉 HAPPY BIRTHDAY {name}! 🎂\n✨✨✨✨✨✨✨✨\nWishing you a day filled with\nlove, laughter and cake! 🎈🥳\nEnjoy your special day! 👑",
    "🥳 Many Many Happy Returns\nof the Day {name}! 🎂🎁🎊\nMay all your wishes come true!\nGod bless you! 🙏💫",
]
WELCOME_MSGS = [
    "👋 Welcome to the group {name}! 🎉\n\nWe're so happy to have you here! 😊\nFeel free to introduce yourself and\njoin the conversation! 🗣️\n\n━━━━━━━━━━━━━━━\n🤖 Powered by {brand} Greet Bot",
    "🌟 Hey {name}, Welcome! 👋🎊\n\nGreat to have a new friend here! 🥳\nDon't be shy — say hi to everyone! 😄\n\n━━━━━━━━━━━━━━━\n🤖 Powered by {brand} Greet Bot",
    "🎉 Welcome aboard {name}! 🚀\n\nYou just joined an amazing group! 🔥\nIntroduce yourself and enjoy! 💯\n\n━━━━━━━━━━━━━━━\n🤖 Powered by {brand} Greet Bot",
]
QUOTES = [
    "💡 \"The secret of getting ahead is getting started.\"\n— Mark Twain",
    "🔥 \"Believe you can and you're halfway there.\"\n— Theodore Roosevelt",
    "⚡ \"Your limitation — it's only your imagination.\"",
    "🌟 \"Push yourself, because no one else is going\nto do it for you.\"",
    "💪 \"Great things never come from comfort zones.\"",
    "🚀 \"Dream it. Wish it. Do it.\"",
    "🎯 \"Success doesn't just find you.\nYou have to go out and get it.\"",
    "✨ \"The harder you work for something,\nthe greater you'll feel when you achieve it.\"",
    "💫 \"Don't stop when you're tired.\nStop when you're done.\"",
    "🏆 \"Wake up with determination.\nGo to bed with satisfaction.\"",
    "🌈 \"Little things make big days.\"",
    "💎 \"It's going to be hard, but hard\ndoes not mean impossible.\"",
    "🔑 \"Don't wait for opportunity.\nCreate it.\"",
    "🌻 \"Sometimes we're tested not to show\nour weaknesses, but to discover our strengths.\"",
    "⭐ \"The key to success is to focus on\ngoals, not obstacles.\"",
]

# ══════════════════════════════════════════
#  DATABASE
# ══════════════════════════════════════════
def load_db():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f: return json.load(f)
    return {"groups": {}, "users": {}}

def save_db(db):
    with open(DATA_FILE, "w") as f: json.dump(db, f, indent=2)

def register_group(chat_id, title):
    db = load_db(); k = str(chat_id)
    if k not in db["groups"]:
        db["groups"][k] = {"title": title, "joined": datetime.now().strftime("%Y-%m-%d"), "quotes": True}
        save_db(db)

def register_user(uid, uname=""):
    db = load_db(); k = str(uid)
    if k not in db["users"]:
        db["users"][k] = {"username": uname, "joined": datetime.now().strftime("%Y-%m-%d")}
        save_db(db)

# ══════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════
def get_name(user):
    name = user.first_name or ""
    if user.last_name: name += f" {user.last_name}"
    return name.strip() or "Friend"

def contains(text, words):
    text = text.lower().strip()
    return any(w in text for w in words)

def reply(msg, template_list, name):
    text = random.choice(template_list).format(name=name, brand=BRAND)
    bot.reply_to(msg, text)

# ══════════════════════════════════════════
#  /start — Private chat
# ══════════════════════════════════════════
@bot.message_handler(commands=["start"])
def cmd_start(msg):
    uid = msg.from_user.id
    register_user(uid, msg.from_user.username or "")
    name = get_name(msg.from_user)
    # Get bot info for add link
    try:
        bot_info = bot.get_me()
        bot_un = bot_info.username
    except:
        bot_un = BOT_USERNAME
    kb = telebot.types.InlineKeyboardMarkup()
    kb.add(telebot.types.InlineKeyboardButton(
        "➕ Add me to your Group",
        url=f"https://t.me/{bot_un}?startgroup=start&admin=post_messages+delete_messages+restrict_members"
    ))
    kb.add(telebot.types.InlineKeyboardButton(
        "📊 My Stats", callback_data="stats"
    ))
    kb.add(telebot.types.InlineKeyboardButton(
        "ℹ️ Commands", callback_data="commands"
    ))
    bot.send_message(uid,
        f"👋 Hey {name}!\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"I'm {BRAND} Greet Bot 🤖\n\n"
        f"I make your group more lively\nand friendly every single day!\n\n"
        f"✅ What I do in groups:\n"
        f"• 🌅 Reply to Good Morning\n"
        f"• 🌆 Reply to Good Afternoon\n"
        f"• 🌇 Reply to Good Evening\n"
        f"• 🌙 Reply to Good Night\n"
        f"• 🎂 Wish on Birthdays\n"
        f"• 👋 Welcome new members\n"
        f"• 💡 Send daily motivation at 8 AM\n\n"
        f"➕ How to add me:\n"
        f"1️⃣ Tap button below\n"
        f"2️⃣ Select your group\n"
        f"3️⃣ Give admin rights\n"
        f"4️⃣ I start working instantly! ⚡\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🤖 {BRAND} Greet Bot",
        reply_markup=kb
    )

# ══════════════════════════════════════════
#  BOT ADDED TO GROUP
# ══════════════════════════════════════════
@bot.message_handler(content_types=["new_chat_members"])
def welcome_new_member(msg):
    chat_id = msg.chat.id
    register_group(chat_id, msg.chat.title or "Group")
    for member in msg.new_chat_members:
        # Bot itself added to group
        if member.id == bot.get_me().id:
            bot.send_message(chat_id,
                f"👋 Hello everyone!\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"I'm {BRAND} Greet Bot! 🤖🎉\n\n"
                f"I'm here to make this group\nmore warm, active and friendly! 🔥\n\n"
                f"I'll greet everyone's\nGood Morning / Night / Evening 🌅\nWelcome new members 👋\nWish on Birthdays 🎂\nSend daily motivation at 8 AM 💡\n\n"
                f"Let's make this group amazing! 🚀\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"🤖 Powered by {BRAND}"
            )
        else:
            # New human member joined
            name = get_name(member)
            text = random.choice(WELCOME_MSGS).format(name=name, brand=BRAND)
            bot.send_message(chat_id, text)

# ══════════════════════════════════════════
#  MESSAGE HANDLER — Greetings detector
# ══════════════════════════════════════════
@bot.message_handler(func=lambda m: m.text and m.chat.type in ["group","supergroup"])
def handle_group_msg(msg):
    text = msg.text.lower().strip()
    name = get_name(msg.from_user)
    register_group(msg.chat.id, msg.chat.title or "Group")

    # Check greetings (only if message is short — actual greeting, not a sentence)
    if len(text) < 40:
        if contains(text, MORNING_WORDS):
            reply(msg, MORNING_REPLIES, name); return
        if contains(text, AFTERNOON_WORDS):
            reply(msg, AFTERNOON_REPLIES, name); return
        if contains(text, EVENING_WORDS):
            reply(msg, EVENING_REPLIES, name); return
        if contains(text, NIGHT_WORDS):
            reply(msg, NIGHT_REPLIES, name); return
        if contains(text, BIRTHDAY_WORDS):
            reply(msg, BIRTHDAY_REPLIES, name); return

# ══════════════════════════════════════════
#  CALLBACKS
# ══════════════════════════════════════════
@bot.callback_query_handler(func=lambda c: True)
def callbacks(call):
    uid = call.from_user.id
    bot.answer_callback_query(call.id)
    db = load_db(); ud = db["users"].get(str(uid), {})

    if call.data == "stats":
        bot.edit_message_text(
            f"📊 YOUR STATS\n━━━━━━━━━━━━━━━━\n\n"
            f"👤 {get_name(call.from_user)}\n"
            f"📅 Joined: {ud.get('joined','N/A')}\n\n"
            f"🌍 Total Groups: {len(db['groups'])}\n"
            f"👥 Total Users: {len(db['users'])}\n\n"
            f"🤖 {BRAND} Greet Bot",
            uid, call.message.message_id,
            reply_markup=telebot.types.InlineKeyboardMarkup([[
                telebot.types.InlineKeyboardButton("🔙 Back", callback_data="back")
            ]])
        )
    elif call.data == "commands":
        bot.edit_message_text(
            f"📋 COMMANDS\n━━━━━━━━━━━━━━━━\n\n"
            f"Group Commands:\n"
            f"• Say 'Good Morning' → 🌅 Reply\n"
            f"• Say 'Good Night' → 🌙 Reply\n"
            f"• Say 'Good Evening' → 🌇 Reply\n"
            f"• Say 'Good Afternoon' → 🌆 Reply\n"
            f"• Say 'Happy Birthday' → 🎂 Reply\n"
            f"• New member joins → 👋 Welcome\n\n"
            f"Admin Commands:\n"
            f"/quote — Send quote now\n"
            f"/togglequote — On/Off daily quotes\n\n"
            f"🤖 {BRAND} Greet Bot",
            uid, call.message.message_id,
            reply_markup=telebot.types.InlineKeyboardMarkup([[
                telebot.types.InlineKeyboardButton("🔙 Back", callback_data="back")
            ]])
        )
    elif call.data == "back":
        try:
            bot_un = bot.get_me().username
        except:
            bot_un = BOT_USERNAME
        kb = telebot.types.InlineKeyboardMarkup()
        kb.add(telebot.types.InlineKeyboardButton("➕ Add me to your Group",
            url=f"https://t.me/{bot_un}?startgroup=start"))
        kb.add(telebot.types.InlineKeyboardButton("📊 My Stats", callback_data="stats"))
        kb.add(telebot.types.InlineKeyboardButton("ℹ️ Commands", callback_data="commands"))
        bot.edit_message_text(
            f"🤖 {BRAND} Greet Bot\n\nTap a button below! 👇",
            uid, call.message.message_id, reply_markup=kb)

# ══════════════════════════════════════════
#  GROUP COMMANDS
# ══════════════════════════════════════════
@bot.message_handler(commands=["quote"])
def cmd_quote(msg):
    if msg.chat.type in ["group","supergroup"]:
        quote = random.choice(QUOTES)
        bot.send_message(msg.chat.id,
            f"💡 DAILY MOTIVATION\n━━━━━━━━━━━━━━━━\n\n"
            f"{quote}\n\n"
            f"━━━━━━━━━━━━━━━━\n"
            f"🤖 {BRAND} Greet Bot | Have a great day! 🌟"
        )

@bot.message_handler(commands=["togglequote"])
def cmd_togglequote(msg):
    if msg.chat.type not in ["group","supergroup"]: return
    db = load_db(); k = str(msg.chat.id)
    if k not in db["groups"]: db["groups"][k] = {"title": msg.chat.title, "quotes": True}
    db["groups"][k]["quotes"] = not db["groups"][k].get("quotes", True)
    status = "ON ✅" if db["groups"][k]["quotes"] else "OFF ❌"
    save_db(db)
    bot.reply_to(msg, f"💡 Daily quotes turned {status}")

# ══════════════════════════════════════════
#  ADMIN COMMANDS
# ══════════════════════════════════════════
@bot.message_handler(commands=["admin"])
def cmd_admin(msg):
    if msg.from_user.id != OWNER_ID: return
    db = load_db()
    bot.reply_to(msg,
        f"🔧 ADMIN — {BRAND}\n\n"
        f"👥 Total Users: {len(db['users'])}\n"
        f"🏘️ Total Groups: {len(db['groups'])}\n\n"
        f"Groups:\n" +
        "\n".join([f"• {v.get('title','?')} ({k})" for k,v in list(db['groups'].items())[:10]])
    )

@bot.message_handler(commands=["broadcast"])
def cmd_broadcast(msg):
    if msg.from_user.id != OWNER_ID: return
    text = msg.text.replace("/broadcast","").strip()
    if not text: bot.reply_to(msg,"Usage: /broadcast message"); return
    db = load_db(); ok = fail = 0
    for gid in db["groups"]:
        try:
            bot.send_message(int(gid), f"📢 {BRAND} Announcement\n\n{text}")
            ok += 1; time.sleep(0.1)
        except: fail += 1
    bot.reply_to(msg, f"✅ Groups: {ok} ❌ Failed: {fail}")

# ══════════════════════════════════════════
#  DAILY QUOTE SCHEDULER
# ══════════════════════════════════════════
def send_daily_quotes():
    db = load_db()
    quote = random.choice(QUOTES)
    now = datetime.now().strftime("%A, %d %B %Y")
    msg_text = (
        f"🌅 Good Morning Everyone! ☀️\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📅 {now}\n\n"
        f"💡 Quote of the Day:\n\n"
        f"{quote}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Have an amazing day! 🚀✨\n"
        f"🤖 {BRAND} Greet Bot"
    )
    for gid, gdata in db["groups"].items():
        if gdata.get("quotes", True):
            try:
                bot.send_message(int(gid), msg_text)
                time.sleep(0.2)
            except Exception as e:
                logging.warning(f"Quote to {gid} failed: {e}")

def run_scheduler():
    schedule.every().day.at(f"{QUOTE_HOUR:02d}:{QUOTE_MINUTE:02d}").do(send_daily_quotes)
    logging.info(f"📅 Daily quotes scheduled at {QUOTE_HOUR:02d}:{QUOTE_MINUTE:02d}")
    while True:
        schedule.run_pending()
        time.sleep(30)

# ══════════════════════════════════════════
#  RUN
# ══════════════════════════════════════════
if __name__ == "__main__":
    print(f"🤖 {BRAND} Greet Bot is RUNNING!")
    print(f"📅 Daily quotes at {QUOTE_HOUR:02d}:{QUOTE_MINUTE:02d}")
    print("─" * 40)
    # Run scheduler in background thread
    t = threading.Thread(target=run_scheduler, daemon=True)
    t.start()
    # Start bot
    bot.infinity_polling(timeout=30, long_polling_timeout=30)
