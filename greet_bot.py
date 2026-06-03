"""
╔══════════════════════════════════════════════════════╗
║   GREETINGS & QUOTES BOT — Professional Edition     ║
║   Railway Ready | 24/7 | Smart & Fast               ║
║   pip install pyTelegramBotAPI schedule requests    ║
╚══════════════════════════════════════════════════════╝

IMPORTANT FIRST STEP:
→ Message @BotFather → /setprivacy → your bot → DISABLE
→ This allows bot to read all group messages!
"""

import telebot, json, os, time, logging, random, threading, schedule
from datetime import datetime
from telebot.types import (InlineKeyboardMarkup, InlineKeyboardButton,
                           ReplyKeyboardMarkup, KeyboardButton)

# ══════════════════════════════════════════
#  CONFIG — Edit these
# ══════════════════════════════════════════
TOKEN        = "8759110609:AAG2xRZ9bIm_Hp6PlavYWT8HmjrM_wqfq7g"
BOT_USERNAME = "Greetings122_bot"
OWNER_ID     = 8873676178
BRAND        = "Greetings & Quotes"
BRAND_TAG    = "@Greetings122_bot"
QUOTE_TIME   = "08:00"   # 24hr format
DATA_FILE    = "greet_data.json"

bot = telebot.TeleBot(TOKEN, parse_mode=None)
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")

# ══════════════════════════════════════════
#  TRIGGER WORDS
# ══════════════════════════════════════════
MORNING   = ["good morning","gm","good mrng","gud morning","gd mrng","goodmorning",
             "morning","subah","suprabhat","शुभ प्रभात","सुप्रभात","gm everyone",
             "gm all","good moring","goood morning","gooood morning"]
AFTERNOON = ["good afternoon","afternoon","gud afternoon","goodafternoon",
             "good aftn","gd afternoon","dopahar"]
EVENING   = ["good evening","evening","gud evening","goodevening",
             "good evng","gd evening","sham","शुभ संध्या"]
NIGHT     = ["good night","gn","good nite","gud night","goodnight","nite",
             "night","shubh ratri","शुभ रात्रि","gn everyone","gn all",
             "good nyt","goodnyt","sweet dreams"]
BIRTHDAY  = ["happy birthday","hbd","hb","birthday","bday","happy bday",
             "janamdin","जन्मदिन मुबारक","bd","many happy returns",
             "happy b'day","h.b.d","happybirthday"]

# ══════════════════════════════════════════
#  MORNING REPLIES
# ══════════════════════════════════════════
MORNING_REPLIES = [
    "🌅 *Good Morning {name}!* ☀️\n\n"
    "╭──────────────────╮\n"
    "│  🌸 New Day, New Blessings! │\n"
    "╰──────────────────╯\n\n"
    "💫 May this morning bring you\n"
    "joy, energy & positivity!\n\n"
    "📿 *Stay blessed, stay amazing!* ✨\n"
    "━━━━━━━━━━━━━━━━━━\n"
    "🤖 {brand}",

    "☀️ *Rise & Shine {name}!* 🌻\n\n"
    "🌈 Good Morning!\n\n"
    "Today is a brand new chance to:\n"
    "✅ Be better than yesterday\n"
    "✅ Chase your dreams\n"
    "✅ Spread good vibes\n\n"
    "💪 *You got this! Let's go!* 🔥\n"
    "━━━━━━━━━━━━━━━━━━\n"
    "🤖 {brand}",

    "🌄 *Good Morning {name}!* 🙏\n\n"
    "『 The sun is up, the sky is blue 』\n"
    "『 Beautiful day just for you! 』\n\n"
    "🫖 Grab your chai/coffee ☕\n"
    "Take a deep breath 🌬️\n"
    "And make today count! 💯\n\n"
    "━━━━━━━━━━━━━━━━━━\n"
    "🤖 {brand}",

    "🌞 *Subah Bakhair {name}!* 🌺\n\n"
    "🕌 May Allah bless your morning\n"
    "with happiness & health!\n\n"
    "🤲 *Ameen* 🤲\n\n"
    "Start your day with Bismillah! 📖\n"
    "Everything will be amazing! ✨\n"
    "━━━━━━━━━━━━━━━━━━\n"
    "🤖 {brand}",

    "🌅 *Wakey Wakey {name}!* 😄\n\n"
    "⚡ Good Morning!\n\n"
    "🔋 Battery Status:\n"
    "Energy ████████░░ 80%\n"
    "Mood   █████████░ 90%\n"
    "Vibe   ██████████ 100%\n\n"
    "*Fully charged for today!* 🚀\n"
    "━━━━━━━━━━━━━━━━━━\n"
    "🤖 {brand}",
]

# ══════════════════════════════════════════
#  AFTERNOON REPLIES
# ══════════════════════════════════════════
AFTERNOON_REPLIES = [
    "🌆 *Good Afternoon {name}!* ☀️\n\n"
    "╭────────────────╮\n"
    "│  Halfway through the day! │\n"
    "╰────────────────╯\n\n"
    "💪 You're doing great!\n"
    "Keep the energy going! 🔥\n"
    "The best is yet to come! 🌟\n"
    "━━━━━━━━━━━━━━━━━━\n"
    "🤖 {brand}",

    "☀️ *Good Afternoon {name}!* 🌼\n\n"
    "⏰ It's the middle of the day!\n\n"
    "🫖 Time for a little break:\n"
    "→ Drink some water 💧\n"
    "→ Stretch a little 🧘\n"
    "→ Take a deep breath 🌬️\n\n"
    "Then back to being awesome! 💯\n"
    "━━━━━━━━━━━━━━━━━━\n"
    "🤖 {brand}",

    "🌤 *Shubh Dopahar {name}!* 😊\n\n"
    "🍽️ Hope you had a great meal!\n"
    "Now recharge and conquer\n"
    "the rest of the day! 💪⚡\n\n"
    "*Keep smiling, keep shining!* ✨\n"
    "━━━━━━━━━━━━━━━━━━\n"
    "🤖 {brand}",
]

# ══════════════════════════════════════════
#  EVENING REPLIES
# ══════════════════════════════════════════
EVENING_REPLIES = [
    "🌇 *Good Evening {name}!* 🌙\n\n"
    "╭────────────────╮\n"
    "│   Day is wrapping up!    │\n"
    "╰────────────────╯\n\n"
    "🫖 Time to relax & unwind!\n"
    "You worked hard today! 💯\n\n"
    "🌸 *Enjoy your evening!* ✨\n"
    "━━━━━━━━━━━━━━━━━━\n"
    "🤖 {brand}",

    "🌆 *Shaam Bakhair {name}!* 🌃\n\n"
    "🌅 The golden hour is here!\n\n"
    "🎵 Put on your fav music\n"
    "☕ Make yourself a warm drink\n"
    "😌 And just breathe...\n\n"
    "You deserve this moment! 🙏\n"
    "━━━━━━━━━━━━━━━━━━\n"
    "🤖 {brand}",
]

# ══════════════════════════════════════════
#  NIGHT REPLIES
# ══════════════════════════════════════════
NIGHT_REPLIES = [
    "🌙 *Good Night {name}!* 😴\n\n"
    "╭────────────────╮\n"
    "│   Rest well, champ! 💤  │\n"
    "╰────────────────╯\n\n"
    "⭐ Today you:\n"
    "✨ Worked hard\n"
    "✨ Stayed strong\n"
    "✨ Made it through!\n\n"
    "🌟 *Sweet dreams!* 💫\n"
    "━━━━━━━━━━━━━━━━━━\n"
    "🤖 {brand}",

    "🌛 *Good Night {name}!* 🌟\n\n"
    "Tomorrow is a new adventure!\n\n"
    "🌙 As you rest tonight,\n"
    "let go of all worries 🍃\n"
    "and wake up refreshed! 🌅\n\n"
    "💤 *Sleep tight!* 😊\n"
    "━━━━━━━━━━━━━━━━━━\n"
    "🤖 {brand}",

    "💤 *Shubh Ratri {name}!* 🌙\n\n"
    "🕌 May Allah protect you\n"
    "while you sleep! 🤲\n\n"
    "📖 Read your duas before sleep\n"
    "🌸 *Ameen* 🌸\n\n"
    "See you tomorrow! ✨\n"
    "━━━━━━━━━━━━━━━━━━\n"
    "🤖 {brand}",

    "🌙 *Night Night {name}!* 😴⭐\n\n"
    "Today's report card:\n"
    "Hardwork  ████████ A+\n"
    "Attitude  ████████ A+\n"
    "Vibes     ████████ A+\n\n"
    "🏆 *You crushed it today!*\n"
    "Rest up for tomorrow! 💪\n"
    "━━━━━━━━━━━━━━━━━━\n"
    "🤖 {brand}",
]

# ══════════════════════════════════════════
#  BIRTHDAY REPLIES
# ══════════════════════════════════════════
BIRTHDAY_REPLIES = [
    "🎂 *HAPPY BIRTHDAY {name}!* 🎉\n\n"
    "🎈🎈🎈🎈🎈🎈🎈🎈🎈\n\n"
    "╭────────────────────╮\n"
    "│  🥳 It's Your Special Day! 🥳 │\n"
    "╰────────────────────╯\n\n"
    "🎁 May this year bring you:\n"
    "✨ Joy & happiness\n"
    "💪 Health & strength\n"
    "🏆 Success & wealth\n"
    "❤️ Love & laughter\n\n"
    "🎶 *HBD to you! HBD to you!* 🎶\n"
    "━━━━━━━━━━━━━━━━━━\n"
    "🤖 {brand}",

    "🥳 *Many Many Happy Returns* 🎊\n"
    "*of the Day {name}!!* 🎂\n\n"
    "🎈✨🎈✨🎈✨🎈✨\n\n"
    "👑 Today you are the KING/QUEEN!\n\n"
    "🙏 May Allah grant you:\n"
    "→ Long & healthy life\n"
    "→ All your wishes\n"
    "→ Infinite happiness\n\n"
    "💝 *Enjoy your day to the fullest!*\n"
    "━━━━━━━━━━━━━━━━━━\n"
    "🤖 {brand}",
]

# ══════════════════════════════════════════
#  WELCOME MESSAGES
# ══════════════════════════════════════════
WELCOME_MSGS = [
    "👋 *Welcome to the family, {name}!* 🎉\n\n"
    "╭────────────────────╮\n"
    "│  🌟 New Member Alert! 🌟  │\n"
    "╰────────────────────╯\n\n"
    "We're so happy to have you here! 😊\n\n"
    "📌 *Quick Tips:*\n"
    "→ Read the group rules\n"
    "→ Introduce yourself!\n"
    "→ Be kind & respectful 🙏\n\n"
    "Enjoy your stay! 🎊\n"
    "━━━━━━━━━━━━━━━━━━\n"
    "🤖 {brand}",

    "🌟 *Hey {name}, Welcome!* 👋\n\n"
    "🎊 You just joined an amazing\ncommunity! 🔥\n\n"
    "👀 Look around, say hello,\nand make yourself at home! 🏠\n\n"
    "💬 *Don't be shy — say hi!* 😄\n"
    "━━━━━━━━━━━━━━━━━━\n"
    "🤖 {brand}",

    "🚀 *Welcome Aboard {name}!* 🎉\n\n"
    "╭────────────────╮\n"
    "│  Member #{count} has joined! │\n"
    "╰────────────────╯\n\n"
    "We hope you enjoy your time here!\n\n"
    "✅ Introduce yourself\n"
    "✅ Follow the rules\n"
    "✅ Have fun! 🥳\n"
    "━━━━━━━━━━━━━━━━━━\n"
    "🤖 {brand}",
]

# ══════════════════════════════════════════
#  DAILY QUOTES
# ══════════════════════════════════════════
QUOTES = [
    ("The secret of getting ahead is getting started.", "Mark Twain"),
    ("Believe you can and you're halfway there.", "Theodore Roosevelt"),
    ("Your limitation — it's only your imagination.", "Unknown"),
    ("Push yourself, because no one else is going to do it for you.", "Unknown"),
    ("Great things never come from comfort zones.", "Unknown"),
    ("Dream it. Wish it. Do it.", "Unknown"),
    ("Success doesn't just find you. You have to go out and get it.", "Unknown"),
    ("The harder you work for something, the greater you'll feel when you achieve it.", "Unknown"),
    ("Don't stop when you're tired. Stop when you're done.", "Unknown"),
    ("Wake up with determination. Go to bed with satisfaction.", "Unknown"),
    ("It's going to be hard, but hard does not mean impossible.", "Unknown"),
    ("Don't wait for opportunity. Create it.", "Unknown"),
    ("Sometimes we're tested not to show our weaknesses, but to discover our strengths.", "Unknown"),
    ("The key to success is to focus on goals, not obstacles.", "Unknown"),
    ("You are never too old to set a new goal or dream a new dream.", "C.S. Lewis"),
    ("Act as if what you do makes a difference. It does.", "William James"),
    ("Success is not final, failure is not fatal: it is the courage to continue that counts.", "Winston Churchill"),
    ("Hardships often prepare ordinary people for an extraordinary destiny.", "C.S. Lewis"),
    ("Believe in yourself. You are braver than you think.", "Unknown"),
    ("Every day is a second chance.", "Unknown"),
]

JOKES = [
    "😂 Why don't scientists trust atoms?\nBecause they make up everything! 🤣",
    "😄 What do you call a fake noodle?\nAn impasta! 🍝😂",
    "🤣 Why did the math book look so sad?\nBecause it had too many problems! 📚",
    "😂 What do you call cheese that isn't yours?\nNacho cheese! 🧀🤣",
    "😄 Why can't you give Elsa a balloon?\nBecause she'll let it go! ❄️😂",
    "🤣 What did the ocean say to the beach?\nNothing, it just waved! 🌊😄",
    "😂 Why did the scarecrow win an award?\nBecause he was outstanding in his field! 🌾🤣",
    "😄 What do you call a sleeping dinosaur?\nA dino-snore! 🦕😂",
]

FACTS = [
    "🧠 Fact: Honey never spoils! Archaeologists found 3000-year-old honey in Egypt that was still edible! 🍯",
    "🌍 Fact: A day on Venus is longer than a year on Venus! ☄️",
    "🐬 Fact: Dolphins sleep with one eye open! 👁️",
    "🌿 Fact: There are more trees on Earth than stars in the Milky Way! 🌳",
    "🧊 Fact: Hot water can freeze faster than cold water! This is called the Mpemba effect! ❄️",
    "🐙 Fact: Octopuses have three hearts and blue blood! 💙",
    "🌙 Fact: The Moon is moving away from Earth at 3.8 cm per year! 🚀",
    "🦷 Fact: Teeth are the only part of the human body that can't heal themselves! 😬",
]

# ══════════════════════════════════════════
#  DATABASE
# ══════════════════════════════════════════
def load_db():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f: return json.load(f)
    return {"groups": {}, "users": {}, "total_greets": 0}

def save_db(db):
    with open(DATA_FILE, "w") as f: json.dump(db, f, indent=2)

def register_group(cid, title):
    db = load_db(); k = str(cid)
    if k not in db["groups"]:
        db["groups"][k] = {
            "title": title, "joined": datetime.now().strftime("%Y-%m-%d"),
            "quotes": True, "welcome": True, "member_count": 0
        }
        save_db(db)
    return db["groups"][k]

def register_user(uid, uname=""):
    db = load_db(); k = str(uid)
    if k not in db["users"]:
        db["users"][k] = {"username": uname, "joined": datetime.now().strftime("%Y-%m-%d")}
        save_db(db)

def inc_greet():
    db = load_db()
    db["total_greets"] = db.get("total_greets", 0) + 1
    save_db(db)

# ══════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════
def get_name(user):
    n = (user.first_name or "").strip()
    if user.last_name: n += f" {user.last_name}"
    return n or "Friend"

def contains(text, words):
    t = text.lower().strip()
    return any(w in t for w in words)

def react_kb(msg_type="greet"):
    kb = InlineKeyboardMarkup(row_width=3)
    kb.add(
        InlineKeyboardButton("👍", callback_data=f"react_👍_{msg_type}"),
        InlineKeyboardButton("❤️", callback_data=f"react_❤️_{msg_type}"),
        InlineKeyboardButton("🔥", callback_data=f"react_🔥_{msg_type}"),
    )
    return kb

def greet_reply(msg, templates, name):
    text = random.choice(templates).format(
        name=name, brand=BRAND, count=random.randint(100,999))
    sent = bot.reply_to(msg, text, reply_markup=react_kb())
    inc_greet()
    return sent

# ══════════════════════════════════════════
#  /start — Private
# ══════════════════════════════════════════
@bot.message_handler(commands=["start"])
def cmd_start(msg):
    uid = msg.from_user.id
    if msg.chat.type != "private":
        return
    register_user(uid, msg.from_user.username or "")
    name = get_name(msg.from_user)
    try: bot_un = bot.get_me().username
    except: bot_un = BOT_USERNAME

    kb = InlineKeyboardMarkup(row_width=1)
    kb.add(
        InlineKeyboardButton("➕ Add me to your Group",
            url=f"https://t.me/{bot_un}?startgroup=start&admin=post_messages"),
        InlineKeyboardButton("📋 Commands List", callback_data="commands"),
        InlineKeyboardButton("📊 Bot Statistics", callback_data="botstats"),
        InlineKeyboardButton("ℹ️ How it works", callback_data="howworks"),
    )
    bot.send_message(uid,
        f"🌟 *Welcome {name}!*\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"╭────────────────────╮\n"
        f"│   {BRAND}  │\n"
        f"│        Bot         │\n"
        f"╰────────────────────╯\n\n"
        f"I make your group *warm,\nactive & friendly* every day! 🔥\n\n"
        f"✅ *What I Do:*\n"
        f"🌅 Good Morning replies\n"
        f"🌆 Good Afternoon replies\n"
        f"🌇 Good Evening replies\n"
        f"🌙 Good Night replies\n"
        f"🎂 Birthday wishes\n"
        f"👋 Welcome new members\n"
        f"💡 Daily quote at 8 AM\n"
        f"😂 Jokes & Fun facts\n"
        f"🗳️ Quick polls\n\n"
        f"📌 *Works in Hindi + English!*\n\n"
        f"👇 *Tap below to add me!*\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🤖 {BRAND_TAG}",
        reply_markup=kb, parse_mode="Markdown"
    )

# ══════════════════════════════════════════
#  BOT ADDED TO GROUP
# ══════════════════════════════════════════
@bot.message_handler(content_types=["new_chat_members"])
def new_member(msg):
    chat_id = msg.chat.id
    register_group(chat_id, msg.chat.title or "Group")
    db = load_db(); gdata = db["groups"].get(str(chat_id), {})

    for member in msg.new_chat_members:
        # Bot itself added
        if member.id == bot.get_me().id:
            kb = InlineKeyboardMarkup()
            kb.add(InlineKeyboardButton("📋 Commands", callback_data="commands"),
                   InlineKeyboardButton("⚙️ Settings", callback_data=f"settings_{chat_id}"))
            bot.send_message(chat_id,
                f"👋 *Hello everyone!* 🎉\n"
                f"━━━━━━━━━━━━━━━━━━━━\n\n"
                f"I'm *{BRAND} Bot!* 🤖\n\n"
                f"I'm here to make this group\n"
                f"more *warm, active & fun!* 🔥\n\n"
                f"🌅 I'll greet Good Morning/Night\n"
                f"👋 Welcome every new member\n"
                f"🎂 Wish on birthdays\n"
                f"💡 Send daily motivation 8 AM\n"
                f"😂 Share jokes & fun facts\n\n"
                f"⚡ *I'm ready! Let's go!* 🚀\n\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"🤖 {BRAND_TAG}",
                reply_markup=kb, parse_mode="Markdown"
            )
        else:
            # Human joined
            if not gdata.get("welcome", True): continue
            name = get_name(member)
            db2 = load_db(); g = db2["groups"].get(str(chat_id), {})
            count = g.get("member_count", 0) + 1
            g["member_count"] = count
            save_db(db2)
            text = random.choice(WELCOME_MSGS).format(
                name=name, brand=BRAND, count=count)
            kb = InlineKeyboardMarkup()
            kb.add(InlineKeyboardButton(f"👋 Say Hi to {name.split()[0]}!",
                   callback_data=f"sayhi_{member.id}"))
            bot.send_message(chat_id, text, reply_markup=kb, parse_mode="Markdown")

# ══════════════════════════════════════════
#  GROUP MESSAGES — Smart greeting detector
# ══════════════════════════════════════════
@bot.message_handler(func=lambda m: m.text and m.chat.type in ["group","supergroup"])
def handle_group(msg):
    text = msg.text.lower().strip()
    name = get_name(msg.from_user)
    register_group(msg.chat.id, msg.chat.title or "Group")

    # Only trigger on short messages (actual greetings, not long sentences)
    if len(text) <= 50:
        if contains(text, MORNING):
            greet_reply(msg, MORNING_REPLIES, name); return
        if contains(text, AFTERNOON):
            greet_reply(msg, AFTERNOON_REPLIES, name); return
        if contains(text, EVENING):
            greet_reply(msg, EVENING_REPLIES, name); return
        if contains(text, NIGHT):
            greet_reply(msg, NIGHT_REPLIES, name); return
        if contains(text, BIRTHDAY):
            greet_reply(msg, BIRTHDAY_REPLIES, name); return

# ══════════════════════════════════════════
#  GROUP COMMANDS
# ══════════════════════════════════════════
@bot.message_handler(commands=["quote"], chat_types=["group","supergroup"])
def cmd_quote(msg):
    q, a = random.choice(QUOTES)
    now = datetime.now().strftime("%A, %d %B %Y")
    bot.send_message(msg.chat.id,
        f"💡 *Quote of the Day*\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📅 {now}\n\n"
        f"『 *{q}* 』\n\n"
        f"— _{a}_\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🤖 {BRAND_TAG}",
        reply_markup=react_kb("quote"), parse_mode="Markdown")

@bot.message_handler(commands=["joke"], chat_types=["group","supergroup"])
def cmd_joke(msg):
    bot.send_message(msg.chat.id,
        f"😂 *Joke Time!*\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{random.choice(JOKES)}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🤖 {BRAND_TAG}",
        reply_markup=react_kb("joke"), parse_mode="Markdown")

@bot.message_handler(commands=["fact"], chat_types=["group","supergroup"])
def cmd_fact(msg):
    bot.send_message(msg.chat.id,
        f"🧠 *Fun Fact!*\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"{random.choice(FACTS)}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🤖 {BRAND_TAG}",
        reply_markup=react_kb("fact"), parse_mode="Markdown")

@bot.message_handler(commands=["poll"], chat_types=["group","supergroup"])
def cmd_poll(msg):
    polls = [
        ("What's your mood today? 😊", ["😄 Happy","😐 Okay","😔 Sad","🔥 Excited"]),
        ("Best time of day? ⏰", ["🌅 Morning","🌆 Afternoon","🌇 Evening","🌙 Night"]),
        ("How was your day? 📅", ["🌟 Amazing!","👍 Good","😐 Average","😴 Tired"]),
        ("Favorite drink? ☕", ["☕ Tea","☕ Coffee","🥤 Cold drink","💧 Water"]),
    ]
    q, opts = random.choice(polls)
    bot.send_poll(msg.chat.id, q, opts, is_anonymous=False)

@bot.message_handler(commands=["togglequote"], chat_types=["group","supergroup"])
def cmd_togglequote(msg):
    db = load_db(); k = str(msg.chat.id)
    if k not in db["groups"]: db["groups"][k] = {"title": msg.chat.title, "quotes": True}
    db["groups"][k]["quotes"] = not db["groups"][k].get("quotes", True)
    status = "ON ✅" if db["groups"][k]["quotes"] else "OFF ❌"
    save_db(db)
    bot.reply_to(msg, f"💡 Daily morning quotes: *{status}*", parse_mode="Markdown")

@bot.message_handler(commands=["togglewelcome"], chat_types=["group","supergroup"])
def cmd_togglewelcome(msg):
    db = load_db(); k = str(msg.chat.id)
    if k not in db["groups"]: db["groups"][k] = {"title": msg.chat.title, "welcome": True}
    db["groups"][k]["welcome"] = not db["groups"][k].get("welcome", True)
    status = "ON ✅" if db["groups"][k]["welcome"] else "OFF ❌"
    save_db(db)
    bot.reply_to(msg, f"👋 Welcome messages: *{status}*", parse_mode="Markdown")

@bot.message_handler(commands=["help"], chat_types=["group","supergroup"])
def cmd_help_group(msg):
    bot.reply_to(msg,
        f"📋 *{BRAND} Bot Commands*\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"*/quote* — Send a motivational quote\n"
        f"*/joke* — Tell a funny joke 😂\n"
        f"*/fact* — Share a fun fact 🧠\n"
        f"*/poll* — Start a quick poll 🗳️\n"
        f"*/togglequote* — Toggle daily quotes\n"
        f"*/togglewelcome* — Toggle welcome msgs\n\n"
        f"🗣️ *Auto Triggers:*\n"
        f"Say 'gm' / 'good morning' → 🌅\n"
        f"Say 'gn' / 'good night' → 🌙\n"
        f"Say 'good evening' → 🌇\n"
        f"Say 'hbd' / 'happy birthday' → 🎂\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🤖 {BRAND_TAG}",
        parse_mode="Markdown")

# ══════════════════════════════════════════
#  CALLBACKS
# ══════════════════════════════════════════
@bot.callback_query_handler(func=lambda c: True)
def callbacks(call):
    uid = call.from_user.id
    d = call.data

    if d.startswith("react_"):
        parts = d.split("_")
        emoji = parts[1]
        bot.answer_callback_query(call.id, f"{emoji} Reacted!")
        return

    if d.startswith("sayhi_"):
        target = d.split("_")[1]
        name = call.from_user.first_name or "Someone"
        bot.answer_callback_query(call.id, f"👋 {name} said hi!")
        try:
            bot.send_message(call.message.chat.id,
                f"👋 *{name}* says hi to the new member! 😊",
                parse_mode="Markdown")
        except: pass
        return

    bot.answer_callback_query(call.id)

    if d == "commands":
        kb = InlineKeyboardMarkup()
        kb.add(InlineKeyboardButton("🔙 Back", callback_data="back_start"))
        try:
            bot.edit_message_text(
                f"📋 *Commands List*\n"
                f"━━━━━━━━━━━━━━━━━━━━\n\n"
                f"*In Groups:*\n"
                f"/quote — Daily motivation 💡\n"
                f"/joke — Funny joke 😂\n"
                f"/fact — Fun fact 🧠\n"
                f"/poll — Quick poll 🗳️\n"
                f"/togglequote — ON/OFF quotes\n"
                f"/togglewelcome — ON/OFF welcome\n"
                f"/help — Show commands\n\n"
                f"*Auto Triggers:*\n"
                f"🌅 good morning / gm\n"
                f"🌆 good afternoon\n"
                f"🌇 good evening\n"
                f"🌙 good night / gn\n"
                f"🎂 happy birthday / hbd\n\n"
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
                f"📊 *Bot Statistics*\n"
                f"━━━━━━━━━━━━━━━━━━━━\n\n"
                f"🏘️ Groups: *{len(db['groups'])}*\n"
                f"👥 Users: *{len(db['users'])}*\n"
                f"💬 Total Greetings: *{db.get('total_greets',0)}*\n\n"
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
                f"3️⃣ That's it! I start working!\n\n"
                f"⚡ *IMPORTANT:*\n"
                f"Disable my privacy mode via\n"
                f"@BotFather → /setprivacy → DISABLE\n"
                f"So I can read all messages!\n\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"🤖 {BRAND_TAG}",
                uid, call.message.message_id,
                reply_markup=kb, parse_mode="Markdown")
        except: pass

    elif d == "back_start":
        try:
            bot_un = bot.get_me().username
        except:
            bot_un = BOT_USERNAME
        kb = InlineKeyboardMarkup(row_width=1)
        kb.add(
            InlineKeyboardButton("➕ Add me to your Group",
                url=f"https://t.me/{bot_un}?startgroup=start&admin=post_messages"),
            InlineKeyboardButton("📋 Commands List", callback_data="commands"),
            InlineKeyboardButton("📊 Bot Statistics", callback_data="botstats"),
            InlineKeyboardButton("ℹ️ How it works", callback_data="howworks"),
        )
        try:
            bot.edit_message_text(
                f"🌟 *{BRAND} Bot*\n"
                f"━━━━━━━━━━━━━━━━━━━━\n\n"
                f"Making groups warm & friendly! 🔥\n\n"
                f"👇 *Tap below!*\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"🤖 {BRAND_TAG}",
                uid, call.message.message_id,
                reply_markup=kb, parse_mode="Markdown")
        except: pass

# ══════════════════════════════════════════
#  ADMIN COMMANDS
# ══════════════════════════════════════════
@bot.message_handler(commands=["admin"])
def cmd_admin(msg):
    if msg.from_user.id != OWNER_ID: return
    db = load_db()
    today = datetime.now().strftime("%Y-%m-%d")
    new_groups = sum(1 for g in db["groups"].values() if g.get("joined")==today)
    bot.reply_to(msg,
        f"🔧 *ADMIN PANEL*\n"
        f"━━━━━━━━━━━━━━━━━━━━\n\n"
        f"🏘️ Groups: {len(db['groups'])}\n"
        f"🆕 New Groups Today: {new_groups}\n"
        f"👥 Users: {len(db['users'])}\n"
        f"💬 Greetings Sent: {db.get('total_greets',0)}\n\n"
        f"Groups:\n" +
        "\n".join([f"• {v.get('title','?')}" for k,v in list(db['groups'].items())[:10]]),
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
            ok += 1; time.sleep(0.1)
        except: fail += 1
    bot.reply_to(msg, f"✅ Groups: {ok} | ❌ Failed: {fail}")

# ══════════════════════════════════════════
#  DAILY MORNING QUOTE SCHEDULER
# ══════════════════════════════════════════
def send_morning_quotes():
    db = load_db()
    q, a = random.choice(QUOTES)
    now = datetime.now().strftime("%A, %d %B %Y")
    text = (
        f"🌅 *Good Morning Everyone!* ☀️\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📅 {now}\n\n"
        f"💡 *Quote of the Day:*\n\n"
        f"『 *{q}* 』\n"
        f"— _{a}_\n\n"
        f"🚀 Have an amazing day!\n"
        f"Stay positive, stay blessed! 🙏\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🤖 {BRAND_TAG}"
    )
    for gid, gdata in db["groups"].items():
        if gdata.get("quotes", True):
            try:
                bot.send_message(int(gid), text, parse_mode="Markdown")
                time.sleep(0.2)
            except Exception as e:
                logging.warning(f"Quote to {gid}: {e}")

def run_scheduler():
    schedule.every().day.at(QUOTE_TIME).do(send_morning_quotes)
    logging.info(f"⏰ Daily quotes at {QUOTE_TIME}")
    while True:
        schedule.run_pending()
        time.sleep(30)

# ══════════════════════════════════════════
#  RUN
# ══════════════════════════════════════════
if __name__ == "__main__":
    print(f"🤖 {BRAND} Bot RUNNING!")
    print(f"⏰ Daily quotes at {QUOTE_TIME}")
    print("─" * 42)
    threading.Thread(target=run_scheduler, daemon=True).start()
    bot.infinity_polling(timeout=30, long_polling_timeout=30)
