from aiogram import Bot, Dispatcher, executor, types
import json
import os

TOKEN = "7882795675:AAGDzMp9JHO-D9WPS4lSSLYHYSUecu19jy0"
ADMIN_ID = @Admen_Flx 

CHANNELS = [
    "@HarryPotterseriesss",
    "@GameOfThrones_1234"
]

bot = Bot(token=7882795675:AAGDzMp9JHO-D9WPS4lSSLYHYSUecu19jy0, parse_mode="HTML")
dp = Dispatcher(bot)

DATA_FILE = "movies.json"

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

def load_data():
    with open(DATA_FILE) as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

async def is_subscribed(user_id):
    for ch in CHANNELS:
        try:
            m = await bot.get_chat_member(ch, user_id)
            if m.status not in ["member", "administrator", "creator"]:
                return False
        except:
            return False
    return True

# ===== START =====
@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    await msg.answer(
        "🎬 <b>Movie Code Bot</b>\n\n"
        "• Subscribe to our channels\n"
        "• Send your movie code\n"
        "• Watch instantly"
    )

# ===== ADMIN: MOVIE =====
@dp.message_handler(content_types=types.ContentType.VIDEO)
async def admin_video(msg: types.Message):
    if msg.from_user.id != ADMIN_ID:
        return

    await msg.answer("✅ Movie received.\nNow send the access code.")

    dp.current_state(user=msg.from_user.id).update_data(
        file_id=msg.video.file_id
    )

# ===== ADMIN: CODE =====
@dp.message_handler(lambda m: m.from_user.id == ADMIN_ID)
async def admin_code(msg: types.Message):
    state = dp.current_state(user=msg.from_user.id)
    data = await state.get_data()

    if "file_id" not in data:
        return

    code = msg.text.strip()
    movies = load_data()
    movies[code] = data["file_id"]
    save_data(movies)

    await msg.answer(f"🎉 Movie saved!\nCode: <b>{code}</b>")
    await state.finish()

# ===== USER: CODE =====
@dp.message_handler()
async def user_code(msg: types.Message):
    if not await is_subscribed(msg.from_user.id):
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("Join Channel 1", url="https://t.me/my_movie_channel"))
        kb.add(types.InlineKeyboardButton("Join Channel 2", url="https://t.me/premium_movies"))
        await msg.answer("❌ Subscribe to channels first.", reply_markup=kb)
        return

    movies = load_data()
    code = msg.text.strip()

    if code not in movies:
        await msg.answer("❌ Invalid or used code.")
        return

    await bot.send_video(
        msg.chat.id,
        movies[code],
        caption="🎥 Enjoy your movie!",
        protect_content=True
    )

    del movies[code]
    save_data(movies)

executor.start_polling(dp)
