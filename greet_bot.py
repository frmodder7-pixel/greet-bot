"""
GREETINGS & QUOTES BOT — by BLITEX
Railway Ready | 24/7
pip install pyTelegramBotAPI schedule requests
IMPORTANT: @BotFather → /setprivacy → DISABLE
"""
import telebot, json, os, time, logging, random, threading, schedule
from datetime import datetime
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN        = "YOUR_BOT_TOKEN_HERE"
BOT_USERNAME = "Greetings122_bot"
OWNER_ID     = 8873676178
BRAND        = "Greetings & Quotes Bot"
BRAND_TAG    = "@Greetings122_bot"
QUOTE_TIME   = "08:00"
DATA_FILE    = "greet_data.json"

bot = telebot.TeleBot(TOKEN, parse_mode=None)
# ══════════════════════════════════════════
#  ANTI-SPAM SYSTEM
# ══════════════════════════════════════════
from collections import defaultdict
import time as time_module

# spam_data[chat_id][user_id] = [timestamps]
spam_data   = defaultdict(lambda: defaultdict(list))
warn_data   = defaultdict(lambda: defaultdict(int))  # warnings per user per group

SPAM_LIMIT    = 5    # messages in SPAM_WINDOW seconds = spam
SPAM_WINDOW   = 5    # seconds
MAX_WARNINGS  = 3    # warnings before mute

def check_spam(chat_id, user_id):
    now = time_module.time()
    timestamps = spam_data[chat_id][user_id]
    # Remove old timestamps outside window
    spam_data[chat_id][user_id] = [t for t in timestamps if now - t < SPAM_WINDOW]
    spam_data[chat_id][user_id].append(now)
    return len(spam_data[chat_id][user_id]) >= SPAM_LIMIT

def get_warnings(chat_id, user_id):
    return warn_data[chat_id][user_id]

def add_warning(chat_id, user_id):
    warn_data[chat_id][user_id] += 1
    return warn_data[chat_id][user_id]

def reset_warnings(chat_id, user_id):
    warn_data[chat_id][user_id] = 0

def is_admin(chat_id, user_id):
    try:
        member = bot.get_chat_member(chat_id, user_id)
        return member.status in ["administrator", "creator"]
    except: return False

def mute_user(chat_id, user_id, seconds=300):
    try:
        from telebot.types import ChatPermissions
        until = int(time_module.time()) + seconds
        bot.restrict_chat_member(chat_id, user_id,
            permissions=ChatPermissions(can_send_messages=False),
            until_date=until)
        return True
    except: return False


logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

# ── TRIGGERS ────────────────────────────
MORNING   = ["good morning","gm","good mrng","gud morning","gd mrng","goodmorning",
             "morning","gm everyone","gm all","good moring","goood morning"]
AFTERNOON = ["good afternoon","afternoon","gud afternoon","goodafternoon","good aftn"]
EVENING   = ["good evening","evening","gud evening","goodevening","good evng"]
NIGHT     = ["good night","gn","good nite","gud night","goodnight","nite",
             "gn everyone","gn all","good nyt","goodnyt","sweet dreams"]
BIRTHDAY  = ["happy birthday","hbd","hb","birthday","bday","happy bday",
             "many happy returns","happy b'day","h.b.d","happybirthday"]

# ── REPLIES (use {mention} to tag user) ─
MORNING_REPLIES = [
    "🌅 Good Morning {mention}! ☀️\nHave an amazing day ahead! 😊",
    "☀️ Good Morning {mention}! 🌻\nRise & shine — today will be great! 💪",
    "🌄 Good Morning {mention}! 😄\nA new day, a fresh start! Make it count! 🔥",
    "🌞 Good Morning {mention}! ✨\nThe world needs your energy today! 🚀",
    "🌅 Good Morning {mention}! 🌈\nSmile — it's a beautiful day! 😁",
    "☀️ Good Morning {mention}! 🌟\nStay positive & keep smiling today! 💯",
    "🌄 Good Morning {mention}! 🎯\nNew day = new opportunities! Go crush it! 💥",
]

AFTERNOON_REPLIES = [
    "🌆 Good Afternoon {mention}! ☀️\nHope your day is going great! 😊",
    "🌤 Good Afternoon {mention}! 💪\nHalfway done — keep the energy up! 🔥",
    "☀️ Good Afternoon {mention}! 😄\nTime for a quick break! You deserve it! ☕",
    "🌆 Good Afternoon {mention}! 🌟\nStay focused, you're doing amazing! 💯",
]

EVENING_REPLIES = [
    "🌇 Good Evening {mention}! 🌙\nTime to relax and unwind! 😌✨",
    "🌆 Good Evening {mention}! 🌃\nHope you had a productive day! 💪",
    "🌇 Good Evening {mention}! 😊\nSit back, chill and enjoy! 🎵",
    "🌆 Good Evening {mention}! ⭐\nThe day is almost done — great job! 🏆",
]

NIGHT_REPLIES = [
    "🌙 Good Night {mention}! 😴\nSweet dreams! Rest well! 💤⭐",
    "🌛 Good Night {mention}! 🌟\nTime to recharge! See you tomorrow! 😊",
    "💤 Good Night {mention}! 🌙\nYou did great today! Sleep tight! ✨",
    "🌙 Night Night {mention}! 😴💫\nTomorrow is going to be amazing! 🌅",
    "⭐ Good Night {mention}! 🌙\nRest well, wake up fresh! 💪",
]

BIRTHDAY_REPLIES = [
    "🎂 Happy Birthday {mention}! 🎉🎊\n🎈🎈🎈🎈🎈🎈🎈\nWishing you an amazing day\nfilled with joy & happiness! 🥳🎁",
    "🥳 Happy Birthday {mention}! 🎂✨\nMany many happy returns!\nEnjoy your special day! 🎊🎈",
    "🎉 HBD {mention}! 🎂🎁\nToday is YOUR day! Celebrate big! 🥳🎊",
]

WELCOME_MSGS = [
    "👋 Welcome {mention} to the group! 🎉\nHappy to have you here! 😊\nFeel free to say hi everyone!",
    "🌟 Welcome {mention}! 🎊\nGreat to have you here! Don't be shy! 😄",
    "🎉 Welcome aboard {mention}! 🚀\nYou just joined an amazing group! Say hello! 💬",
]

QUOTES = [
    ("The secret of getting ahead is getting started.", "Mark Twain"),
    ("Believe you can and you're halfway there.", "Theodore Roosevelt"),
    ("Push yourself, because no one else is going to do it for you.", "Unknown"),
    ("Great things never come from comfort zones.", "Unknown"),
    ("Dream it. Wish it. Do it.", "Unknown"),
    ("The harder you work, the greater you'll feel when you achieve it.", "Unknown"),
    ("Don't stop when you're tired. Stop when you're done.", "Unknown"),
    ("Wake up with determination. Go to bed with satisfaction.", "Unknown"),
    ("It's going to be hard, but hard does not mean impossible.", "Unknown"),
    ("Don't wait for opportunity. Create it.", "Unknown"),
    ("Success is not final, failure is not fatal.", "Winston Churchill"),
    ("Every day is a second chance.", "Unknown"),
    ("Believe in yourself. You are braver than you think.", "Unknown"),
    ("Act as if what you do makes a difference. It does.", "William James"),
    ("You are never too old to set a new goal.", "C.S. Lewis"),
]

JOKES = [
    "😂 Why don't scientists trust atoms?\nBecause they make up everything! 🤣",
    "😄 What do you call a fake noodle?\nAn impasta! 🍝😂",
    "🤣 Why did the math book look sad?\nBecause it had too many problems! 📚",
    "😂 What do you call cheese that isn't yours?\nNacho cheese! 🧀🤣",
    "😄 What did the ocean say to the beach?\nNothing, it just waved! 🌊😄",
    "🤣 Why did the scarecrow win an award?\nOutstanding in his field! 🌾😂",
]

FACTS = [
    "🧠 Honey never spoils! 3000-year-old honey from Egypt was still edible! 🍯",
    "🌍 A day on Venus is longer than a year on Venus! ☄️",
    "🐬 Dolphins sleep with one eye open! 👁️",
    "🌿 There are more trees on Earth than stars in the Milky Way! 🌳",
    "🐙 Octopuses have three hearts and blue blood! 💙",
    "🌙 The Moon moves away from Earth at 3.8 cm per year! 🚀",
]

# ── DATABASE ─────────────────────────────
def load_db():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f: return json.load(f)
    return {"groups": {}, "users": {}, "total_greets": 0}

def save_db(db):
    with open(DATA_FILE, "w") as f: json.dump(db, f, indent=2)

def register_group(cid, title):
    db = load_db(); k = str(cid)
    if k not in db["groups"]:
        db["groups"][k] = {"title": title, "joined": datetime.now().strftime("%Y-%m-%d"),
                           "quotes": True, "welcome": True}
        save_db(db)

def register_user(uid, uname=""):
    db = load_db(); k = str(uid)
    if k not in db["users"]:
        db["users"][k] = {"username": uname, "joined": datetime.now().strftime("%Y-%m-%d")}
        save_db(db)

def inc_greet():
    db = load_db()
    db["total_greets"] = db.get("total_greets", 0) + 1
    save_db(db)

# ── HELPERS ──────────────────────────────
def get_name(user):
    n = (user.first_name or "").strip()
    return n or "Friend"

def get_mention(user):
    """Returns clickable @mention that tags the user"""
    name = get_name(user)
    return f"[{name}](tg://user?id={user.id})"

def contains(text, words):
    t = text.lower().strip()
    return any(w in t for w in words)

def react_kb():
    kb = InlineKeyboardMarkup(row_width=4)
    kb.add(
        InlineKeyboardButton("👍", callback_data="react_👍"),
        InlineKeyboardButton("❤️", callback_data="react_❤️"),
        InlineKeyboardButton("🔥", callback_data="react_🔥"),
        InlineKeyboardButton("😂", callback_data="react_😂"),
    )
    return kb

def send_greet(msg, templates, user):
    mention = get_mention(user)
    text = random.choice(templates).format(mention=mention)
    bot.reply_to(msg, text, parse_mode="Markdown", reply_markup=react_kb())
    inc_greet()

# ── /start ───────────────────────────────
@bot.message_handler(commands=["start"])
def cmd_start(msg):
    if msg.chat.type != "private": return
    uid = msg.from_user.id
    register_user(uid, msg.from_user.username or "")
    name = get_name(msg.from_user)
    try: bot_un = bot.get_me().username
    except: bot_un = BOT_USERNAME
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("➕ Add me to your Group",
            url=f"https://t.me/{bot_un}?startgroup=start&admin=post_messages"),
        InlineKeyboardButton("📋 Commands", callback_data="commands"),
        InlineKeyboardButton("📊 Statistics", callback_data="botstats"),
        InlineKeyboardButton("ℹ️ How it works", callback_data="howworks"),
    )
    caption = (
        f"👋 Hey *{name}!*\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"I'm *{BRAND}* 🤖\n\n"
        f"Making your group *warm, active & friendly!* 🔥\n\n"
        f"✅ *What I Do:*\n"
        f"🌅 Good Morning replies\n"
        f"🌆 Good Afternoon replies\n"
        f"🌇 Good Evening replies\n"
        f"🌙 Good Night replies\n"
        f"🎂 Birthday wishes\n"
        f"👋 Welcome new members\n"
        f"💡 Daily quote at 8 AM\n"
        f"😂 /joke • 🧠 /fact • 🗳️ /poll\n\n"
        f"⚡ *Instant! No delay!*\n\n"
        f"👇 *Tap below to add me!*\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🤖 {BRAND_TAG}"
    )
    try:
        photos = bot.get_user_profile_photos(bot.get_me().id, limit=1)
        if photos.total_count > 0:
            fid = photos.photos[0][0].file_id
            bot.send_photo(uid, fid, caption=caption, reply_markup=kb, parse_mode="Markdown")
        else:
            bot.send_message(uid, caption, reply_markup=kb, parse_mode="Markdown")
    except:
        bot.send_message(uid, caption, reply_markup=kb, parse_mode="Markdown")

# ── BOT ADDED TO GROUP ───────────────────
@bot.message_handler(content_types=["new_chat_members"])
def new_member(msg):
    chat_id = msg.chat.id
    register_group(chat_id, msg.chat.title or "Group")
    db = load_db(); gdata = db["groups"].get(str(chat_id), {})

    for member in msg.new_chat_members:
        if member.id == bot.get_me().id:
            kb = InlineKeyboardMarkup()
            kb.add(InlineKeyboardButton("📋 Commands", callback_data="commands"))
            bot.send_message(chat_id,
                f"👋 Hello everyone!\n"
                f"━━━━━━━━━━━━━━━━━━━━\n\n"
                f"I'm *{BRAND}!* 🤖\n\n"
                f"I'll make this group more\n*warm, active & fun!* 🔥\n\n"
                f"🌅 Greet Good Morning/Night\n"
                f"👋 Welcome new members\n"
                f"🎂 Wish birthdays\n"
                f"💡 Daily quote at 8 AM\n"
                f"😂 Jokes & Fun facts\n\n"
                f"⚡ *Ready! Let's go!* 🚀\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"🤖 {BRAND_TAG}",
                reply_markup=kb, parse_mode="Markdown")
        else:
            if not gdata.get("welcome", True): continue
            mention = get_mention(member)
            text = random.choice(WELCOME_MSGS).format(mention=mention)
            kb = InlineKeyboardMarkup()
            kb.add(InlineKeyboardButton("👋 Say Hi!", callback_data=f"sayhi_{member.id}_{get_name(member)}"))
            # Try to send with user profile photo
            try:
                photos = bot.get_user_profile_photos(member.id, limit=1)
                if photos.total_count > 0:
                    fid = photos.photos[0][0].file_id
                    bot.send_photo(chat_id, fid, caption=text, parse_mode="Markdown", reply_markup=kb)
                else:
                    bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=kb)
            except:
                bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=kb)

# ── GROUP MESSAGES ───────────────────────
@bot.message_handler(func=lambda m: m.text and m.chat.type in ["group","supergroup"])
def handle_group(msg):
    text = msg.text.lower().strip()
    user = msg.from_user
    chat_id = msg.chat.id
    uid = user.id
    register_group(chat_id, msg.chat.title or "Group")

    # Anti-spam check (skip for admins)
    if not is_admin(chat_id, uid):
        if check_spam(chat_id, uid):
            try: bot.delete_message(chat_id, msg.message_id)
            except: pass
            warns = add_warning(chat_id, uid)
            mention = get_mention(user)
            remaining = MAX_WARNINGS - warns
            if warns >= MAX_WARNINGS:
                # Mute for 5 minutes
                if mute_user(chat_id, uid, 300):
                    reset_warnings(chat_id, uid)
                    bot.send_message(chat_id,
                        f"🔇 {mention} has been *muted for 5 minutes* due to spamming!\n"
                        f"Please follow the group rules. ⚠️",
                        parse_mode="Markdown")
            else:
                bot.send_message(chat_id,
                    f"⚠️ {mention} please stop spamming!\n"
                    f"*Warning {warns}/{MAX_WARNINGS}* — "
                    f"{remaining} more warning(s) before mute! 🔇",
                    parse_mode="Markdown")
            return

    if len(text) <= 50:
        if contains(text, MORNING):
            send_greet(msg, MORNING_REPLIES, user); return
        if contains(text, AFTERNOON):
            send_greet(msg, AFTERNOON_REPLIES, user); return
        if contains(text, EVENING):
            send_greet(msg, EVENING_REPLIES, user); return
        if contains(text, NIGHT):
            send_greet(msg, NIGHT_REPLIES, user); return
        if contains(text, BIRTHDAY):
            send_greet(msg, BIRTHDAY_REPLIES, user); return

# ── GROUP COMMANDS ────────────────────────
@bot.message_handler(commands=["quote"], func=lambda m: m.chat.type in ["group","supergroup","private"])
def cmd_quote(msg):
    q, a = random.choice(QUOTES)
    now = datetime.now().strftime("%A, %d %B %Y")
    bot.send_message(msg.chat.id,
        f"💡 *Quote of the Day*\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📅 _{now}_\n\n"
        f"*\"{q}\"*\n\n"
        f"— _{a}_\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🤖 {BRAND_TAG}",
        reply_markup=react_kb(), parse_mode="Markdown")

@bot.message_handler(commands=["joke"], func=lambda m: m.chat.type in ["group","supergroup","private"])
def cmd_joke(msg):
    bot.send_message(msg.chat.id,
        f"😂 *Joke Time!*\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{random.choice(JOKES)}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🤖 {BRAND_TAG}",
        reply_markup=react_kb(), parse_mode="Markdown")

@bot.message_handler(commands=["fact"], func=lambda m: m.chat.type in ["group","supergroup","private"])
def cmd_fact(msg):
    bot.send_message(msg.chat.id,
        f"🧠 *Fun Fact!*\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{random.choice(FACTS)}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🤖 {BRAND_TAG}",
        reply_markup=react_kb(), parse_mode="Markdown")

@bot.message_handler(commands=["poll"], func=lambda m: m.chat.type in ["group","supergroup"])
def cmd_poll(msg):
    polls = [
        ("What's your mood today? 😊", ["😄 Happy","😐 Okay","😔 Sad","🔥 Excited"]),
        ("Best time of day?", ["🌅 Morning","🌆 Afternoon","🌇 Evening","🌙 Night"]),
        ("How was your day?", ["🌟 Amazing!","👍 Good","😐 Average","😴 Tired"]),
        ("Favorite drink?", ["☕ Tea","☕ Coffee","🥤 Cold drink","💧 Water"]),
    ]
    q, opts = random.choice(polls)
    bot.send_poll(msg.chat.id, q, opts, is_anonymous=False)

@bot.message_handler(commands=["togglequote"], func=lambda m: m.chat.type in ["group","supergroup"])
def cmd_togglequote(msg):
    db = load_db(); k = str(msg.chat.id)
    if k not in db["groups"]: db["groups"][k] = {"title": msg.chat.title, "quotes": True}
    db["groups"][k]["quotes"] = not db["groups"][k].get("quotes", True)
    status = "ON ✅" if db["groups"][k]["quotes"] else "OFF ❌"
    save_db(db)
    bot.reply_to(msg, f"💡 Daily morning quotes: *{status}*", parse_mode="Markdown")

@bot.message_handler(commands=["togglewelcome"], func=lambda m: m.chat.type in ["group","supergroup"])
def cmd_togglewelcome(msg):
    db = load_db(); k = str(msg.chat.id)
    if k not in db["groups"]: db["groups"][k] = {"title": msg.chat.title, "welcome": True}
    db["groups"][k]["welcome"] = not db["groups"][k].get("welcome", True)
    status = "ON ✅" if db["groups"][k]["welcome"] else "OFF ❌"
    save_db(db)
    bot.reply_to(msg, f"👋 Welcome messages: *{status}*", parse_mode="Markdown")

@bot.message_handler(commands=["help"], func=lambda m: True)
def cmd_help_group(msg):
    bot.reply_to(msg,
        f"📋 *Commands*\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"/quote — Daily motivation 💡\n"
        f"/joke — Funny joke 😂\n"
        f"/fact — Fun fact 🧠\n"
        f"/poll — Quick poll 🗳️\n"
        f"/togglequote — ON/OFF daily quotes\n"
        f"/togglewelcome — ON/OFF welcome\n\n"
        f"*Auto Triggers:*\n"
        f"🌅 gm / good morning\n"
        f"🌆 good afternoon\n"
        f"🌇 good evening\n"
        f"🌙 gn / good night\n"
        f"🎂 hbd / happy birthday\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🤖 {BRAND_TAG}",
        parse_mode="Markdown")

# ── CALLBACKS ─────────────────────────────
@bot.callback_query_handler(func=lambda c: True)
def callbacks(call):
    uid = call.from_user.id; d = call.data

    if d.startswith("react_"):
        emoji = d.split("_")[1]
        bot.answer_callback_query(call.id, f"{emoji} Reacted!"); return

    if d.startswith("sayhi_"):
        parts = d.split("_")
        reactor = call.from_user.first_name or "Someone"
        bot.answer_callback_query(call.id, f"You said hi! 👋")
        try:
            target_id = int(parts[1])
            target_name = parts[2] if len(parts) > 2 else "them"
            mention_reactor = f"[{reactor}](tg://user?id={uid})"
            mention_target  = f"[{target_name}](tg://user?id={target_id})"
            bot.send_message(call.message.chat.id,
                f"👋 {mention_reactor} says hi to {mention_target}! 😊",
                parse_mode="Markdown")
        except: pass
        return

    bot.answer_callback_query(call.id)

    if d == "commands":
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton("🔙 Back", callback_data="back_start"))
        try:
            bot.edit_message_text(
                f"📋 *Commands*\n"
                f"━━━━━━━━━━━━━━━━━━━━\n\n"
                f"*In Groups:*\n"
                f"/quote — Motivation 💡\n"
                f"/joke — Funny joke 😂\n"
                f"/fact — Fun fact 🧠\n"
                f"/poll — Quick poll 🗳️\n"
                f"/togglequote — ON/OFF daily quotes\n"
                f"/togglewelcome — ON/OFF welcome msgs\n"
                f"/help — Show commands\n\n"
                f"*Auto Triggers (just type):*\n"
                f"🌅 gm / good morning\n"
                f"🌆 good afternoon\n"
                f"🌇 good evening\n"
                f"🌙 gn / good night\n"
                f"🎂 hbd / happy birthday\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"🤖 {BRAND_TAG}",
                uid, call.message.message_id,
                reply_markup=kb, parse_mode="Markdown")
        except: pass

    elif d == "botstats":
        db = load_db()
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton("🔙 Back", callback_data="back_start"))
        try:
            bot.edit_message_text(
                f"📊 *Statistics*\n"
                f"━━━━━━━━━━━━━━━━━━━━\n\n"
                f"🏘️ Groups: *{len(db['groups'])}*\n"
                f"👥 Users: *{len(db['users'])}*\n"
                f"💬 Greetings Sent: *{db.get('total_greets',0)}*\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"🤖 {BRAND_TAG}",
                uid, call.message.message_id,
                reply_markup=kb, parse_mode="Markdown")
        except: pass

    elif d == "howworks":
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton("🔙 Back", callback_data="back_start"))
        try:
            bot.edit_message_text(
                f"ℹ️ *How it Works*\n"
                f"━━━━━━━━━━━━━━━━━━━━\n\n"
                f"1️⃣ Add me to your group\n"
                f"2️⃣ Make me admin\n"
                f"3️⃣ I start working instantly!\n\n"
                f"⚡ *IMPORTANT:*\n"
                f"Go to @BotFather\n"
                f"→ /setprivacy\n"
                f"→ Select your bot\n"
                f"→ Click *DISABLE*\n\n"
                f"This lets me read all messages!\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"🤖 {BRAND_TAG}",
                uid, call.message.message_id,
                reply_markup=kb, parse_mode="Markdown")
        except: pass

    elif d == "back_start":
        try: bot_un = bot.get_me().username
        except: bot_un = BOT_USERNAME
        kb = InlineKeyboardMarkup(row_width=1)
        kb.add(
            InlineKeyboardButton("➕ Add me to your Group",
                url=f"https://t.me/{bot_un}?startgroup=start&admin=post_messages"),
            InlineKeyboardButton("📋 Commands", callback_data="commands"),
            InlineKeyboardButton("📊 Statistics", callback_data="botstats"),
            InlineKeyboardButton("ℹ️ How it works", callback_data="howworks"),
        )
        try:
            bot.edit_message_text(
                f"🤖 *{BRAND}*\n"
                f"━━━━━━━━━━━━━━━━━━━━\n\n"
                f"Making groups warm & friendly! 🔥\n\n"
                f"👇 Tap below!\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"🤖 {BRAND_TAG}",
                uid, call.message.message_id,
                reply_markup=kb, parse_mode="Markdown")
        except: pass


# ── WARN / UNWARN (Admin only) ───────────
@bot.message_handler(commands=["warn"], func=lambda m: m.chat.type in ["group","supergroup"])
def cmd_warn(msg):
    if not is_admin(msg.chat.id, msg.from_user.id):
        bot.reply_to(msg, "❌ Admins only!"); return
    if not msg.reply_to_message:
        bot.reply_to(msg, "⚠️ Reply to a message to warn that user!"); return
    target = msg.reply_to_message.from_user
    if is_admin(msg.chat.id, target.id):
        bot.reply_to(msg, "❌ Can\'t warn an admin!"); return
    warns = add_warning(msg.chat.id, target.id)
    mention = get_mention(target)
    remaining = MAX_WARNINGS - warns
    if warns >= MAX_WARNINGS:
        if mute_user(msg.chat.id, target.id, 300):
            reset_warnings(msg.chat.id, target.id)
            bot.send_message(msg.chat.id,
                f"🔇 {mention} has been *muted for 5 minutes!*\n"
                f"Reason: Too many warnings! ⚠️",
                parse_mode="Markdown")
    else:
        bot.send_message(msg.chat.id,
            f"⚠️ *Warning issued!*\n"
            f"User: {mention}\n"
            f"Warnings: *{warns}/{MAX_WARNINGS}*\n"
            f"{remaining} more = mute! 🔇",
            parse_mode="Markdown")

@bot.message_handler(commands=["unwarn"], func=lambda m: m.chat.type in ["group","supergroup"])
def cmd_unwarn(msg):
    if not is_admin(msg.chat.id, msg.from_user.id):
        bot.reply_to(msg, "❌ Admins only!"); return
    if not msg.reply_to_message:
        bot.reply_to(msg, "⚠️ Reply to a message to remove warning!"); return
    target = msg.reply_to_message.from_user
    reset_warnings(msg.chat.id, target.id)
    mention = get_mention(target)
    bot.send_message(msg.chat.id,
        f"✅ Warnings cleared for {mention}!", parse_mode="Markdown")

@bot.message_handler(commands=["warnings"], func=lambda m: m.chat.type in ["group","supergroup"])
def cmd_warnings(msg):
    if not msg.reply_to_message:
        bot.reply_to(msg, "⚠️ Reply to a message to check warnings!"); return
    target = msg.reply_to_message.from_user
    warns = get_warnings(msg.chat.id, target.id)
    mention = get_mention(target)
    bot.send_message(msg.chat.id,
        f"📋 {mention} has *{warns}/{MAX_WARNINGS}* warnings",
        parse_mode="Markdown")

@bot.message_handler(commands=["mute"], func=lambda m: m.chat.type in ["group","supergroup"])
def cmd_mute(msg):
    if not is_admin(msg.chat.id, msg.from_user.id):
        bot.reply_to(msg, "❌ Admins only!"); return
    if not msg.reply_to_message:
        bot.reply_to(msg, "⚠️ Reply to a message to mute that user!"); return
    target = msg.reply_to_message.from_user
    if is_admin(msg.chat.id, target.id):
        bot.reply_to(msg, "❌ Can\'t mute an admin!"); return
    mention = get_mention(target)
    if mute_user(msg.chat.id, target.id, 3600):
        bot.send_message(msg.chat.id,
            f"🔇 {mention} has been *muted for 1 hour!*", parse_mode="Markdown")
    else:
        bot.reply_to(msg, "❌ Failed! Make sure I\'m an admin with restrict permissions.")

@bot.message_handler(commands=["unmute"], func=lambda m: m.chat.type in ["group","supergroup"])
def cmd_unmute(msg):
    if not is_admin(msg.chat.id, msg.from_user.id):
        bot.reply_to(msg, "❌ Admins only!"); return
    if not msg.reply_to_message:
        bot.reply_to(msg, "⚠️ Reply to unmute!"); return
    target = msg.reply_to_message.from_user
    try:
        from telebot.types import ChatPermissions
        bot.restrict_chat_member(msg.chat.id, target.id,
            permissions=ChatPermissions(
                can_send_messages=True, can_send_media_messages=True,
                can_send_polls=True, can_send_other_messages=True))
        mention = get_mention(target)
        bot.send_message(msg.chat.id,
            f"✅ {mention} has been *unmuted!*", parse_mode="Markdown")
    except:
        bot.reply_to(msg, "❌ Failed to unmute!")

# ── ADMIN ─────────────────────────────────
@bot.message_handler(commands=["admin"])
def cmd_admin(msg):
    if msg.from_user.id != OWNER_ID: return
    db = load_db(); today = datetime.now().strftime("%Y-%m-%d")
    new_g = sum(1 for g in db["groups"].values() if g.get("joined")==today)
    bot.reply_to(msg,
        f"🔧 *ADMIN*\n\n"
        f"🏘️ Groups: {len(db['groups'])}\n"
        f"🆕 New Today: {new_g}\n"
        f"👥 Users: {len(db['users'])}\n"
        f"💬 Greetings: {db.get('total_greets',0)}",
        parse_mode="Markdown")

@bot.message_handler(commands=["broadcast"])
def cmd_broadcast(msg):
    if msg.from_user.id != OWNER_ID: return
    text = msg.text.replace("/broadcast","").strip()
    if not text: bot.reply_to(msg,"Usage: /broadcast message"); return
    db = load_db(); ok = fail = 0
    for gid in db["groups"]:
        try:
            bot.send_message(int(gid), f"📢 *Announcement*\n\n{text}", parse_mode="Markdown")
            ok+=1; time.sleep(0.1)
        except: fail+=1
    bot.reply_to(msg, f"✅ Groups:{ok} ❌ Failed:{fail}")

# ── DAILY QUOTES ──────────────────────────
def send_morning_quotes():
    db = load_db(); q, a = random.choice(QUOTES)
    now = datetime.now().strftime("%A, %d %B %Y")
    text = (
        f"🌅 *Good Morning Everyone!* ☀️\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📅 _{now}_\n\n"
        f"💡 *Quote of the Day:*\n\n"
        f"*\"{q}\"*\n"
        f"— _{a}_\n\n"
        f"🚀 Have an amazing day! ✨\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🤖 {BRAND_TAG}"
    )
    for gid, gdata in db["groups"].items():
        if gdata.get("quotes", True):
            try: bot.send_message(int(gid), text, parse_mode="Markdown"); time.sleep(0.2)
            except Exception as e: logging.warning(f"Quote {gid}: {e}")

def run_scheduler():
    schedule.every().day.at(QUOTE_TIME).do(send_morning_quotes)
    logging.info(f"⏰ Quotes scheduled at {QUOTE_TIME}")
    while True: schedule.run_pending(); time.sleep(30)

# ── RUN ───────────────────────────────────
if __name__ == "__main__":
    print(f"🤖 {BRAND} RUNNING!")
    print(f"⏰ Daily quotes at {QUOTE_TIME}")
    print("─" * 42)
    threading.Thread(target=run_scheduler, daemon=True).start()
    bot.infinity_polling(timeout=30, long_polling_timeout=30)
