import random
import logging
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, WebAppInfo, FSInputFile

# --- CONFIGURATION ---
TOKEN = "8797117906:AAG-S0uTTtS-vIE35_4CBHYQKBlPhfbtoic"
# Chemin exact vers ton image sur Android/Termux
PHOTO_PATH = "1773931259708.png" 
# Ton lien Mini App (doit être en https://)
MINI_APP_URL = "https://le-menu-app-ashen.vercel.app" 
# Ton lien de canal
CHANNEL_URL = "https://t.me/menu000000"

# Logging pour voir les erreurs dans Termux
logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- 1. LE CAPTCHA ---

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    n1, n2 = random.randint(1, 9), random.randint(1, 9)
    correct = n1 + n2
    
    # Générer 4 options uniques
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

# --- 2. VÉRIFICATION ET ENVOI ---

@dp.callback_query(F.data.startswith("c_"))
async def check_captcha(callback: types.CallbackQuery):
    data = callback.data.split("_")
    choice, correct = data[1], data[2]

    if choice == correct:
        await callback.message.delete() # Nettoie le captcha
        
        # Texte en Allemand (B2 Style)
        # Note: J'utilise Markdown normal pour éviter les erreurs de caractères spéciaux
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

        # Boutons
        builder = InlineKeyboardBuilder()
        builder.row(InlineKeyboardButton(text="🚀 Menü Öffnen (Mini App)", web_app=WebAppInfo(url=MINI_APP_URL)))
        builder.row(InlineKeyboardButton(text="📢 Unserem Kanal beitreten", url=CHANNEL_URL))

        try:
            # Vérifier si l'image existe avant d'envoyer
            if os.path.exists(PHOTO_PATH):
                photo = FSInputFile(PHOTO_PATH)
                await callback.message.answer_photo(
                    photo=photo,
                    caption=caption_text,
                    reply_markup=builder.as_markup(),
                    parse_mode="Markdown"
                )
            else:
                # Si l'image est introuvable, on envoie quand même le texte
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

if __name__ == "__main__":
    print("🚀 Bot Marsupilami lancé avec succès sur Termux...")
    dp.run_polling(bot)
