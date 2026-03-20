import os
import random
import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, WebAppInfo, FSInputFile
from aiohttp import web

# --- CONFIGURATION ---
TOKEN = os.getenv("BOT_TOKEN")
PHOTO_PATH = "1774008211360.png" # Nom exact de l'image sur ton GitHub
MINI_APP_URL = "https://ton-pseudo.github.io/ton-repo/" 
CHANNEL_URL = "https://t.me/TonCanal"

logging.basicConfig(level=logging.INFO)

if not TOKEN:
    raise ValueError("ERREUR : BOT_TOKEN manquant dans les variables d'environnement !")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- ASTUCE POUR RENDER (Serveur Web) ---
async def handle(request):
    return web.Response(text="Bot Marsupilami is Alive!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    # Render utilise le port 10000 par défaut
    site = web.TCPSite(runner, '0.0.0.0', 10000)
    await site.start()

# --- LOGIQUE DU BOT ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    n1, n2 = random.randint(1, 9), random.randint(1, 9)
    correct = n1 + n2
    builder = InlineKeyboardBuilder()
    options = {correct, correct+1, correct-1, random.randint(2,18)}
    opts_list = list(options)
    random.shuffle(opts_list)
    for o in opts_list:
        builder.add(InlineKeyboardButton(text=str(o), callback_data=f"c_{o}_{correct}"))
    builder.adjust(2)
    await message.answer(f"🤖 **Anti-Bot**\n\n{n1} + {n2} = ?", reply_markup=builder.as_markup(), parse_mode="Markdown")

@dp.callback_query(F.data.startswith("c_"))
async def check_captcha(callback: types.CallbackQuery):
    _, choice, correct = callback.data.split("_")
    if choice == correct:
        await callback.message.delete()
        caption_text = (
            "⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️\n"
            "Willkommen im Dschungel! 🌴\n\n"
            "• News: [KANAL](" + CHANNEL_URL + ")\n"
            "• Menu: Instinktiv ausgewählt 🧪\n\n"
            "👇👇👇 HIER BESTELLEN 👇👇👇"
        )
        builder = InlineKeyboardBuilder()
        builder.row(InlineKeyboardButton(text="🚀 Menü Öffnen", web_app=WebAppInfo(url=MINI_APP_URL)))
        
        if os.path.exists(PHOTO_PATH):
            await callback.message.answer_photo(photo=FSInputFile(PHOTO_PATH), caption=caption_text, reply_markup=builder.as_markup(), parse_mode="Markdown")
        else:
            await callback.message.answer(caption_text, reply_markup=builder.as_markup(), parse_mode="Markdown")
    else:
        await callback.answer("❌ Falsch!", show_alert=True)

async def main():
    # Lancer le serveur web en arrière-plan pour Render
    asyncio.create_task(start_web_server())
    # Lancer le bot
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
