import random  
import logging  
import os  
import asyncio  # ✅ AJOUT
from aiohttp import web  # ✅ AJOUT

from aiogram import Bot, Dispatcher, types, F  
from aiogram.filters import Command  
from aiogram.utils.keyboard import InlineKeyboardBuilder  
from aiogram.types import InlineKeyboardButton, WebAppInfo, FSInputFile  

# --- SERVEUR WEB (OBLIGATOIRE POUR REPLIT) ---
async def start_web_server():
    app = web.Application()

    async def handle(request):
        return web.Response(text="Bot en ligne ✅")

    app.router.add_get("/", handle)

    runner = web.AppRunner(app)
    await runner.setup()

    port = int(os.environ.get("PORT", 8080))  # ✅ IMPORTANT
    site = web.TCPSite(runner, "0.0.0.0", port)

    await site.start()

# --- CONFIGURATION ---  
TOKEN = "TON_TOKEN_ICI"  
PHOTO_PATH = "1773931259708.png"   
MINI_APP_URL = "https://le-menu-app-ashen.vercel.app"   
CHANNEL_URL = "https://t.me/menu000000"  

logging.basicConfig(level=logging.INFO)  

bot = Bot(token=TOKEN)  
dp = Dispatcher()  

# --- MAIN CORRIGÉ ---
async def main():
    asyncio.create_task(start_web_server())
    await asyncio.sleep(2)
    print("BOT LANCÉ")
    await dp.start_polling(bot)

# --- 1. LE CAPTCHA ---  
@dp.message(Command("start"))  
async def cmd_start(message: types.Message):  
    n1, n2 = random.randint(1, 9), random.randint(1, 9)  
    correct = n1 + n2  
      
    options = {correct}  
    while len(options) < 4:  
        options.add(random.randint(2, 18))  
      
    opts_list = list(options)  
    random.shuffle(opts_list)  

    builder = InlineKeyboardBuilder()  
    for o in opts_list:  
        builder.add(InlineKeyboardButton(text=str(o), callback_data=f"c_{o}_{correct}"))  
    builder.adjust(2)  

    text = f"🤖 **Vérification anti-bot**\n\nRésous : **{n1} + {n2} = ?**"  
    await message.answer(text, reply_markup=builder.as_markup(), parse_mode="Markdown")  

# --- 2. VÉRIFICATION ---  
@dp.callback_query(F.data.startswith("c_"))  
async def check_captcha(callback: types.CallbackQuery):  
    data = callback.data.split("_")  
    choice, correct = data[1], data[2]  

    if choice == correct:  
        await callback.message.delete()  

        caption_text = (  
            "⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️⚡️\n"  
            "5 Jahre beherrschter Großstadtdschungel. Die anderen? Immer noch in den Lianen fest 🤭\n"  
            "Deine neue wilde Referenz im Coffee-Shop 🇳🇱🔥 & für exotische Genüsse 🐍🍄\n\n"  
            "👋 Tritt unserem Menü-Bot der neuen Generation bei\n"  
            "📱 Hier kannst du:\n"  
            "• News über [UNSEREN KANAL](" + CHANNEL_URL + ") verfolgen 😈\n"  
            "• Bestellungen & Meet-ups erfahren 📦\n"  
            "• Das komplette Menü entdecken 🧪\n\n"  
            "💬 Bei Le Marsupilami kümmern wir uns mit Leidenschaft um dein Vergnügen ✨\n"  
            "Willkommen im Dschungel 😘\n\n"  
            "👇👇👇 HIER BESTELLEN 👇👇👇"  
        )  

        builder = InlineKeyboardBuilder()  
        builder.row(InlineKeyboardButton(text="🚀 Menü Öffnen (Mini App)", web_app=WebAppInfo(url=MINI_APP_URL)))  
        builder.row(InlineKeyboardButton(text="📢 Unserem Kanal beitreten", url=CHANNEL_URL))  

        try:  
            if os.path.exists(PHOTO_PATH):  
                photo = FSInputFile(PHOTO_PATH)  
                await callback.message.answer_photo(  
                    photo=photo,  
                    caption=caption_text,  
                    reply_markup=builder.as_markup(),  
                    parse_mode="Markdown"  
                )  
            else:  
                await callback.message.answer(  
                    "⚠️ Image introuvable à : " + PHOTO_PATH + "\n\n" + caption_text,  
                    reply_markup=builder.as_markup(),  
                    parse_mode="Markdown",  
                    disable_web_page_preview=True  
                )  
        except Exception as e:  
            await callback.message.answer(f"❌ Erreur d'envoi : {e}")  
    else:  
        await callback.answer("❌ Falsche Antwort! Versuch es nochmal.", show_alert=True)  

# --- LANCEMENT ---
if __name__ == "__main__":  
    print("🚀 Bot Marsupilami lancé...")  
    asyncio.run(main())  # ✅ IMPORTANT (remplace run_polling)
