"""
GREETINGS & QUOTES BOT — Clean Final Version
Railway Ready | 24/7
pip install pyTelegramBotAPI schedule
IMPORTANT: @BotFather → /setprivacy → DISABLE
"""
import telebot, json, os, time, logging, random, threading, schedule
from collections import defaultdict
from datetime import datetime
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ChatPermissions

TOKEN        = os.getenv("TOKEN", "YOUR_BOT_TOKEN_HERE")
BOT_USERNAME = "Greetings122_bot"
OWNER_ID     = 8873676178
BRAND        = "Greetings & Quotes"
BRAND_TAG    = "@Greetings122_bot"
QUOTE_TIME   = "08:00"
DATA_FILE    = "greet_data.json"

bot = telebot.TeleBot(TOKEN, parse_mode=None)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

# ── ANTI-SPAM ────────────────────────────
spam_tracker = defaultdict(lambda: defaultdict(list))
warn_tracker  = defaultdict(lambda: defaultdict(int))
SPAM_LIMIT   = 5
SPAM_WINDOW  = 5

def is_spam(cid, uid):
    now = time.time()
    msgs = [t for t in spam_tracker[cid][uid] if now - t < SPAM_WINDOW]
    msgs.append(now)
    spam_tracker[cid][uid] = msgs
    return len(msgs) >= SPAM_LIMIT

def is_admin(cid, uid):
    try:
        m = bot.get_chat_member(cid, uid)
        return m.status in ["administrator","creator"]
    except: return False

def mute(cid, uid, secs=300):
    try:
        bot.restrict_chat_member(cid, uid,
            permissions=ChatPermissions(can_send_messages=False),
            until_date=int(time.time())+secs)
        return True
    except: return False

def unmute_perms(cid, uid):
    try:
        bot.restrict_chat_member(cid, uid,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_polls=True,
                can_send_other_messages=True))
        return True
    except: return False

# ── TRIGGERS ────────────────────────────
MORNING   = ["good morning","gm","good mrng","gud morning","goodmorning","morning","gm everyone","gm all"]
AFTERNOON = ["good afternoon","afternoon","gud afternoon","goodafternoon","good aftn"]
EVENING   = ["good evening","evening","gud evening","goodevening","good evng"]
NIGHT     = ["good night","gn","good nite","gud night","goodnight","nite","gn everyone","gn all","sweet dreams"]
BIRTHDAY  = ["happy birthday","hbd","hb","birthday","bday","happy bday","many happy returns","happybirthday"]

# ── REPLIES ──────────────────────────────
MORNING_R = [
    "🌅 Good Morning {m}! ☀️\nHave an amazing day! 😊",
    "☀️ Good Morning {m}! 🌻\nRise & shine — make it count! 💪",
    "🌄 Good Morning {m}! 😄\nNew day, fresh start! Go crush it! 🔥",
    "🌞 Good Morning {m}! ✨\nThe world needs your energy today! 🚀",
    "🌅 Good Morning {m}! 🌈\nSmile — it's a beautiful day! 😁",
]
AFTERNOON_R = [
    "🌆 Good Afternoon {m}! ☀️\nHope your day is going great! 😊",
    "🌤 Good Afternoon {m}! 💪\nHalfway done — keep going! 🔥",
    "☀️ Good Afternoon {m}! 😄\nTime for a quick break! ☕",
]
EVENING_R = [
    "🌇 Good Evening {m}! 🌙\nTime to relax and unwind! 😌✨",
    "🌆 Good Evening {m}! 🌃\nHope you had a great day! 💪",
    "🌇 Good Evening {m}! 😊\nSit back, chill and enjoy! 🎵",
]
NIGHT_R = [
    "🌙 Good Night {m}! 😴\nSweet dreams! Rest well! 💤⭐",
    "🌛 Good Night {m}! 🌟\nRecharge! See you tomorrow! 😊",
    "💤 Good Night {m}! 🌙\nYou did great today! Sleep tight! ✨",
    "🌙 Night Night {m}! 😴💫\nTomorrow will be amazing! 🌅",
]
BIRTHDAY_R = [
    "🎂 Happy Birthday {m}! 🎉🎊\n🎈🎈🎈🎈🎈🎈🎈\nWishing you an amazing day! 🥳🎁",
    "🥳 Happy Birthday {m}! 🎂✨\nMany many happy returns! 🎊🎈",
    "🎉 HBD {m}! 🎂🎁\nToday is YOUR day! Celebrate big! 🥳",
]
WELCOME_R = [
    "👋 Welcome {m} to the group! 🎉\nHappy to have you here! 😊",
    "🌟 Welcome {m}! 🎊\nGreat to have you! Don't be shy! 😄",
    "🎉 Welcome aboard {m}! 🚀\nYou joined an amazing group! Say hello! 💬",
]
QUOTES = [
    ("The secret of getting ahead is getting started.","Mark Twain"),
    ("Believe you can and you're halfway there.","Theodore Roosevelt"),
    ("Push yourself, no one else will do it for you.","Unknown"),
    ("Great things never come from comfort zones.","Unknown"),
    ("Dream it. Wish it. Do it.","Unknown"),
    ("Don't stop when you're tired. Stop when done.","Unknown"),
    ("Wake up determined. Go to bed satisfied.","Unknown"),
    ("Hard does not mean impossible.","Unknown"),
    ("Don't wait for opportunity. Create it.","Unknown"),
    ("Every day is a second chance.","Unknown"),
]
JOKES = [
    "😂 Why don't scientists trust atoms?\nBecause they make up everything! 🤣",
    "😄 What do you call a fake noodle?\nAn impasta! 🍝😂",
    "🤣 Why did the math book look sad?\nToo many problems! 📚",
    "😂 What did the ocean say to the beach?\nNothing, it just waved! 🌊😄",
]
FACTS = [
    "🧠 Honey never spoils! 3000yr old honey from Egypt was still edible! 🍯",
    "🌍 A day on Venus is longer than a year on Venus! ☄️",
    "🐬 Dolphins sleep with one eye open! 👁️",
    "🐙 Octopuses have 3 hearts and blue blood! 💙",
]

# ── DB ───────────────────────────────────
def load_db():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f: return json.load(f)
    return {"groups":{},"users":{},"greets":0}

def save_db(db):
    with open(DATA_FILE,"w") as f: json.dump(db,f,indent=2)

def reg_group(cid, title):
    db=load_db(); k=str(cid)
    if k not in db["groups"]:
        db["groups"][k]={"title":title,"joined":datetime.now().strftime("%Y-%m-%d"),"quotes":True,"welcome":True}
        save_db(db)

def reg_user(uid, uname=""):
    db=load_db(); k=str(uid)
    if k not in db["users"]:
        db["users"][k]={"username":uname,"joined":datetime.now().strftime("%Y-%m-%d")}
        save_db(db)

def count_greet():
    db=load_db(); db["greets"]=db.get("greets",0)+1; save_db(db)

# ── HELPERS ──────────────────────────────
def name(user): return (user.first_name or "Friend").strip()
def mention(user): return f"[{name(user)}](tg://user?id={user.id})"
def has(text, words): return any(w in text.lower() for w in words)

def react_kb():
    kb = InlineKeyboardMarkup(row_width=4)
    kb.add(
        InlineKeyboardButton("👍",callback_data="r_👍"),
        InlineKeyboardButton("❤️",callback_data="r_❤️"),
        InlineKeyboardButton("🔥",callback_data="r_🔥"),
        InlineKeyboardButton("😂",callback_data="r_😂"),
    )
    return kb

def greet(msg, replies, user):
    m = mention(user)
    text = random.choice(replies).format(m=m)
    bot.reply_to(msg, text, parse_mode="Markdown", reply_markup=react_kb())
    count_greet()

# ── /start ───────────────────────────────
@bot.message_handler(commands=["start"])
def cmd_start(msg):
    if msg.chat.type != "private": return
    uid = msg.from_user.id
    reg_user(uid, msg.from_user.username or "")
    n = name(msg.from_user)
    try: bot_un = bot.get_me().username
    except: bot_un = BOT_USERNAME
    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("➕ Add me to your Group",
            url=f"https://t.me/{bot_un}?startgroup=start&admin=post_messages"),
        InlineKeyboardButton("📋 Commands", callback_data="commands"),
        InlineKeyboardButton("📊 Statistics", callback_data="stats"),
        InlineKeyboardButton("ℹ️ How it works", callback_data="howworks"),
    )
    caption = (
        f"👋 Hey *{n}!*\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"I'm *{BRAND} Bot* 🤖\n\n"
        f"Making groups *warm & friendly!* 🔥\n\n"
        f"✅ *What I Do:*\n"
        f"🌅 Good Morning replies\n"
        f"🌆 Good Afternoon replies\n"
        f"🌇 Good Evening replies\n"
        f"🌙 Good Night replies\n"
        f"🎂 Birthday wishes\n"
        f"👋 Welcome new members + photo\n"
        f"💡 Daily quote at 8 AM\n"
        f"🚫 Anti-spam protection\n"
        f"😂 /joke • 🧠 /fact • 🗳️ /poll\n\n"
        f"⚡ *Instant! No delay!*\n\n"
        f"👇 *Tap below to add me!*\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🤖 {BRAND_TAG}"
    )
    try:
        bot_chat = bot.get_chat(bot.get_me().id)
        if bot_chat.photo:
            file_info = bot.get_file(bot_chat.photo.big_file_id)
            downloaded = bot.download_file(file_info.file_path)
            import io
            photo_buf = io.BytesIO(downloaded)
            photo_buf.name = "photo.jpg"
            bot.send_photo(uid, photo_buf,
                caption=caption, reply_markup=kb, parse_mode="Markdown")
        else:
            bot.send_message(uid, caption, reply_markup=kb, parse_mode="Markdown")
    except Exception as e:
        logging.warning(f"Start photo: {e}")
        bot.send_message(uid, caption, reply_markup=kb, parse_mode="Markdown")

# ── NEW MEMBERS ──────────────────────────
@bot.message_handler(content_types=["new_chat_members"])
def new_member(msg):
    cid = msg.chat.id
    reg_group(cid, msg.chat.title or "Group")
    db = load_db(); gd = db["groups"].get(str(cid),{})
    for member in msg.new_chat_members:
        if member.id == bot.get_me().id:
            kb = InlineKeyboardMarkup()
            kb.add(InlineKeyboardButton("📋 Commands",callback_data="commands"))
            bot.send_message(cid,
                f"👋 Hello everyone!\n━━━━━━━━━━━━━━━━━━━━\n\n"
                f"I'm *{BRAND} Bot!* 🤖\n\n"
                f"I'll make this group *warm & fun!* 🔥\n\n"
                f"🌅 Greet Good Morning/Night\n"
                f"👋 Welcome new members\n"
                f"🎂 Wish birthdays\n"
                f"🚫 Anti-spam protection\n"
                f"💡 Daily quote at 8 AM\n\n"
                f"⚡ *Ready! Let's go!* 🚀\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"🤖 {BRAND_TAG}",
                reply_markup=kb, parse_mode="Markdown")
        else:
            if not gd.get("welcome",True): continue
            m = mention(member)
            text = random.choice(WELCOME_R).format(m=m)
            kb = InlineKeyboardMarkup()
            kb.add(InlineKeyboardButton("👋 Say Hi!",
                callback_data=f"hi_{member.id}_{name(member)}"))
            try:
                mc = bot.get_chat(member.id)
                if mc.photo:
                    file_info = bot.get_file(mc.photo.big_file_id)
                    downloaded = bot.download_file(file_info.file_path)
                    import io
                    photo_buf = io.BytesIO(downloaded)
                    photo_buf.name = "photo.jpg"
                    bot.send_photo(cid, photo_buf,
                        caption=text, parse_mode="Markdown", reply_markup=kb)
                else:
                    bot.send_message(cid, text, parse_mode="Markdown", reply_markup=kb)
            except Exception as e:
                logging.warning(f"Welcome photo: {e}")
                bot.send_message(cid, text, parse_mode="Markdown", reply_markup=kb)

# ── GROUP MESSAGES ───────────────────────
@bot.message_handler(func=lambda m: m.text and m.chat.type in ["group","supergroup"])
def handle_group(msg):
    txt  = msg.text.lower().strip()
    user = msg.from_user
    cid  = msg.chat.id
    uid  = user.id
    reg_group(cid, msg.chat.title or "Group")

    # Anti-spam (skip admins & bot commands)
    if not txt.startswith("/") and not is_admin(cid, uid):
        if is_spam(cid, uid):
            try: bot.delete_message(cid, msg.message_id)
            except: pass
            warn_tracker[cid][uid] += 1
            warns = warn_tracker[cid][uid]
            m = mention(user)
            if warns >= 3:
                if mute(cid, uid, 300):
                    warn_tracker[cid][uid] = 0
                    bot.send_message(cid,
                        f"🔇 {m} muted *5 minutes* for spamming!",
                        parse_mode="Markdown")
            else:
                bot.send_message(cid,
                    f"⚠️ {m} stop spamming! Warning *{warns}/3*",
                    parse_mode="Markdown")
            return

    if len(txt) <= 50:
        if has(txt, MORNING):   greet(msg, MORNING_R,   user); return
        if has(txt, AFTERNOON): greet(msg, AFTERNOON_R, user); return
        if has(txt, EVENING):   greet(msg, EVENING_R,   user); return
        if has(txt, NIGHT):     greet(msg, NIGHT_R,     user); return
        if has(txt, BIRTHDAY):  greet(msg, BIRTHDAY_R,  user); return

# ── COMMANDS ─────────────────────────────
@bot.message_handler(commands=["quote"])
def cmd_quote(msg):
    q, a = random.choice(QUOTES)
    now  = datetime.now().strftime("%A, %d %B %Y")
    bot.send_message(msg.chat.id,
        f"💡 *Quote of the Day*\n━━━━━━━━━━━━━━━━━━━━\n📅 _{now}_\n\n"
        f"*\"{q}\"*\n— _{a}_\n━━━━━━━━━━━━━━━━━━━━\n🤖 {BRAND_TAG}",
        reply_markup=react_kb(), parse_mode="Markdown")

@bot.message_handler(commands=["joke"])
def cmd_joke(msg):
    bot.send_message(msg.chat.id,
        f"😂 *Joke Time!*\n━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{random.choice(JOKES)}\n━━━━━━━━━━━━━━━━━━━━\n🤖 {BRAND_TAG}",
        reply_markup=react_kb(), parse_mode="Markdown")

@bot.message_handler(commands=["fact"])
def cmd_fact(msg):
    bot.send_message(msg.chat.id,
        f"🧠 *Fun Fact!*\n━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{random.choice(FACTS)}\n━━━━━━━━━━━━━━━━━━━━\n🤖 {BRAND_TAG}",
        reply_markup=react_kb(), parse_mode="Markdown")

@bot.message_handler(commands=["poll"])
def cmd_poll(msg):
    if msg.chat.type not in ["group","supergroup"]: return
    polls = [
        ("What's your mood today?",["😄 Happy","😐 Okay","😔 Sad","🔥 Excited"]),
        ("Best time of day?",["🌅 Morning","🌆 Afternoon","🌇 Evening","🌙 Night"]),
        ("How was your day?",["🌟 Amazing!","👍 Good","😐 Average","😴 Tired"]),
    ]
    q, opts = random.choice(polls)
    bot.send_poll(msg.chat.id, q, opts, is_anonymous=False)

@bot.message_handler(commands=["warn"])
def cmd_warn(msg):
    if msg.chat.type not in ["group","supergroup"]: return
    if not is_admin(msg.chat.id, msg.from_user.id):
        bot.reply_to(msg,"❌ Admins only!"); return
    if not msg.reply_to_message:
        bot.reply_to(msg,"⚠️ Reply to a message to warn!"); return
    target = msg.reply_to_message.from_user
    if is_admin(msg.chat.id, target.id):
        bot.reply_to(msg,"❌ Can't warn an admin!"); return
    warn_tracker[msg.chat.id][target.id] += 1
    warns = warn_tracker[msg.chat.id][target.id]
    m = mention(target)
    if warns >= 3:
        mute(msg.chat.id, target.id, 300)
        warn_tracker[msg.chat.id][target.id] = 0
        bot.send_message(msg.chat.id,
            f"🔇 {m} muted *5 minutes!* (3 warnings reached)",
            parse_mode="Markdown")
    else:
        bot.send_message(msg.chat.id,
            f"⚠️ Warning {m} — *{warns}/3* ({3-warns} left before mute)",
            parse_mode="Markdown")

@bot.message_handler(commands=["unwarn"])
def cmd_unwarn(msg):
    if msg.chat.type not in ["group","supergroup"]: return
    if not is_admin(msg.chat.id, msg.from_user.id):
        bot.reply_to(msg,"❌ Admins only!"); return
    if not msg.reply_to_message:
        bot.reply_to(msg,"⚠️ Reply to remove warning!"); return
    target = msg.reply_to_message.from_user
    warn_tracker[msg.chat.id][target.id] = 0
    bot.send_message(msg.chat.id,
        f"✅ Warnings cleared for {mention(target)}!", parse_mode="Markdown")

@bot.message_handler(commands=["mute"])
def cmd_mute(msg):
    if msg.chat.type not in ["group","supergroup"]: return
    if not is_admin(msg.chat.id, msg.from_user.id):
        bot.reply_to(msg,"❌ Admins only!"); return
    if not msg.reply_to_message:
        bot.reply_to(msg,"⚠️ Reply to mute!"); return
    target = msg.reply_to_message.from_user
    if is_admin(msg.chat.id, target.id):
        bot.reply_to(msg,"❌ Can't mute an admin!"); return
    if mute(msg.chat.id, target.id, 3600):
        bot.send_message(msg.chat.id,
            f"🔇 {mention(target)} muted *1 hour!*", parse_mode="Markdown")
    else:
        bot.reply_to(msg,"❌ Failed! Make me admin with restrict permissions.")

@bot.message_handler(commands=["unmute"])
def cmd_unmute(msg):
    if msg.chat.type not in ["group","supergroup"]: return
    if not is_admin(msg.chat.id, msg.from_user.id):
        bot.reply_to(msg,"❌ Admins only!"); return
    if not msg.reply_to_message:
        bot.reply_to(msg,"⚠️ Reply to unmute!"); return
    target = msg.reply_to_message.from_user
    if unmute_perms(msg.chat.id, target.id):
        bot.send_message(msg.chat.id,
            f"✅ {mention(target)} unmuted!", parse_mode="Markdown")

@bot.message_handler(commands=["togglequote"])
def cmd_tq(msg):
    if msg.chat.type not in ["group","supergroup"]: return
    db=load_db(); k=str(msg.chat.id)
    if k not in db["groups"]: db["groups"][k]={"title":msg.chat.title,"quotes":True}
    db["groups"][k]["quotes"] = not db["groups"][k].get("quotes",True)
    status = "ON ✅" if db["groups"][k]["quotes"] else "OFF ❌"
    save_db(db)
    bot.reply_to(msg, f"💡 Daily quotes: *{status}*", parse_mode="Markdown")

@bot.message_handler(commands=["togglewelcome"])
def cmd_tw(msg):
    if msg.chat.type not in ["group","supergroup"]: return
    db=load_db(); k=str(msg.chat.id)
    if k not in db["groups"]: db["groups"][k]={"title":msg.chat.title,"welcome":True}
    db["groups"][k]["welcome"] = not db["groups"][k].get("welcome",True)
    status = "ON ✅" if db["groups"][k]["welcome"] else "OFF ❌"
    save_db(db)
    bot.reply_to(msg, f"👋 Welcome messages: *{status}*", parse_mode="Markdown")

@bot.message_handler(commands=["help"])
def cmd_help(msg):
    bot.reply_to(msg,
        f"📋 *{BRAND} Commands*\n━━━━━━━━━━━━━━━━━━━━\n\n"
        f"/quote — Motivation 💡\n/joke — Funny joke 😂\n"
        f"/fact — Fun fact 🧠\n/poll — Quick poll 🗳️\n"
        f"/warn — Warn user (reply)\n/unwarn — Clear warning (reply)\n"
        f"/mute — Mute 1hr (reply)\n/unmute — Unmute (reply)\n"
        f"/togglequote — ON/OFF daily quotes\n"
        f"/togglewelcome — ON/OFF welcome\n\n"
        f"*Auto triggers:* gm • gn • good morning\ngood night • hbd • good evening\n"
        f"━━━━━━━━━━━━━━━━━━━━\n🤖 {BRAND_TAG}",
        parse_mode="Markdown")

# ── CALLBACKS ─────────────────────────────
@bot.callback_query_handler(func=lambda c: True)
def cb(call):
    uid = call.from_user.id; d = call.data
    if d.startswith("r_"):
        bot.answer_callback_query(call.id, f"{d[2:]} Reacted!"); return
    if d.startswith("hi_"):
        parts = d.split("_")
        reactor = call.from_user.first_name or "Someone"
        try:
            tid = int(parts[1]); tname = parts[2]
            bot.send_message(call.message.chat.id,
                f"👋 [{reactor}](tg://user?id={uid}) says hi to [{tname}](tg://user?id={tid})! 😊",
                parse_mode="Markdown")
        except: pass
        bot.answer_callback_query(call.id, "👋 Said hi!"); return

    bot.answer_callback_query(call.id)
    back_kb = InlineKeyboardMarkup()
    back_kb.add(InlineKeyboardButton("🔙 Back",callback_data="back"))

    if d == "commands":
        try:
            bot.edit_message_text(
                f"📋 *Commands*\n━━━━━━━━━━━━━━━━━━━━\n\n"
                f"/quote /joke /fact /poll\n"
                f"/warn /unwarn /mute /unmute\n"
                f"/togglequote /togglewelcome /help\n\n"
                f"*Auto:* gm • gn • good morning\nhbd • good evening • birthday\n"
                f"━━━━━━━━━━━━━━━━━━━━\n🤖 {BRAND_TAG}",
                uid,call.message.message_id,reply_markup=back_kb,parse_mode="Markdown")
        except: pass
    elif d == "stats":
        db=load_db()
        try:
            bot.edit_message_text(
                f"📊 *Statistics*\n━━━━━━━━━━━━━━━━━━━━\n\n"
                f"🏘️ Groups: *{len(db['groups'])}*\n"
                f"👥 Users: *{len(db['users'])}*\n"
                f"💬 Greetings: *{db.get('greets',0)}*\n"
                f"━━━━━━━━━━━━━━━━━━━━\n🤖 {BRAND_TAG}",
                uid,call.message.message_id,reply_markup=back_kb,parse_mode="Markdown")
        except: pass
    elif d == "howworks":
        try:
            bot.edit_message_text(
                f"ℹ️ *How it Works*\n━━━━━━━━━━━━━━━━━━━━\n\n"
                f"1️⃣ Add me to your group\n"
                f"2️⃣ Make me admin\n"
                f"3️⃣ I start working instantly!\n\n"
                f"⚠️ *IMPORTANT:*\n"
                f"@BotFather → /setprivacy\n→ your bot → *DISABLE*\n\n"
                f"━━━━━━━━━━━━━━━━━━━━\n🤖 {BRAND_TAG}",
                uid,call.message.message_id,reply_markup=back_kb,parse_mode="Markdown")
        except: pass
    elif d == "back":
        try:
            try: bot_un = bot.get_me().username
            except: bot_un = BOT_USERNAME
            kb = InlineKeyboardMarkup(row_width=1)
            kb.add(
                InlineKeyboardButton("➕ Add me to your Group",
                    url=f"https://t.me/{bot_un}?startgroup=start&admin=post_messages"),
                InlineKeyboardButton("📋 Commands",callback_data="commands"),
                InlineKeyboardButton("📊 Statistics",callback_data="stats"),
                InlineKeyboardButton("ℹ️ How it works",callback_data="howworks"),
            )
            bot.edit_message_caption(
                f"👋 *{BRAND} Bot*\n━━━━━━━━━━━━━━━━━━━━\n\n"
                f"Making groups warm & friendly! 🔥\n👇 Tap below!\n"
                f"━━━━━━━━━━━━━━━━━━━━\n🤖 {BRAND_TAG}",
                uid,call.message.message_id,reply_markup=kb,parse_mode="Markdown")
        except:
            try:
                bot.edit_message_text(
                    f"🤖 *{BRAND} Bot*\n\nTap below! 👇",
                    uid,call.message.message_id,reply_markup=back_kb,parse_mode="Markdown")
            except: pass

# ── ADMIN ─────────────────────────────────
@bot.message_handler(commands=["admin"])
def cmd_admin(msg):
    if msg.from_user.id != OWNER_ID: return
    db=load_db()
    bot.reply_to(msg,
        f"🔧 *ADMIN*\n\n"
        f"🏘️ Groups: {len(db['groups'])}\n"
        f"👥 Users: {len(db['users'])}\n"
        f"💬 Greetings: {db.get('greets',0)}", parse_mode="Markdown")

@bot.message_handler(commands=["broadcast"])
def cmd_broadcast(msg):
    if msg.from_user.id != OWNER_ID: return
    text=msg.text.replace("/broadcast","").strip()
    if not text: bot.reply_to(msg,"Usage: /broadcast msg"); return
    db=load_db(); ok=fail=0
    for gid in db["groups"]:
        try: bot.send_message(int(gid),f"📢 *Announcement*\n\n{text}",parse_mode="Markdown"); ok+=1; time.sleep(0.1)
        except: fail+=1
    bot.reply_to(msg,f"✅ Sent:{ok} ❌ Failed:{fail}")

# ── DAILY QUOTES ──────────────────────────
def send_daily():
    db=load_db(); q,a=random.choice(QUOTES)
    now=datetime.now().strftime("%A, %d %B %Y")
    text=(f"🌅 *Good Morning Everyone!* ☀️\n━━━━━━━━━━━━━━━━━━━━\n"
          f"📅 _{now}_\n\n*\"{q}\"*\n— _{a}_\n\n"
          f"🚀 Have an amazing day! ✨\n━━━━━━━━━━━━━━━━━━━━\n🤖 {BRAND_TAG}")
    for gid,gd in db["groups"].items():
        if gd.get("quotes",True):
            try: bot.send_message(int(gid),text,parse_mode="Markdown"); time.sleep(0.2)
            except Exception as e: logging.warning(f"Quote {gid}: {e}")

def scheduler():
    schedule.every().day.at(QUOTE_TIME).do(send_daily)
    while True: schedule.run_pending(); time.sleep(30)

# ── RUN ───────────────────────────────────
if __name__=="__main__":
    print(f"🤖 {BRAND} Bot RUNNING!")
    print(f"⏰ Daily quotes at {QUOTE_TIME}")
    print("─"*40)
    threading.Thread(target=scheduler, daemon=True).start()
    bot.infinity_polling(timeout=30, long_polling_timeout=30)
