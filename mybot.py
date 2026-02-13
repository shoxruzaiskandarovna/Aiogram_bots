import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.exceptions import TelegramBadRequest

TOKEN = "7682243909:AAEB5Ol6zVSLeCVrcNmxDqqTaT22QESCWsc"
ADMIN_ID = 2052902289
CHANNEL_USERNAME = "@aaestix"  # Kanalingizni kiriting (@ bilan)
last_user = {}
dp = Dispatcher()


# Kanal a'zoligini tekshirish
async def check_subscription(user_id: int, bot: Bot) -> bool:
    """Foydalanuvchi kanalga a'zo ekanligini tekshiradi"""
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        # A'zo bo'lsa: creator, administrator, member
        return member.status in ["creator", "administrator", "member"]
    except TelegramBadRequest:
        return False


@dp.message(Command("start"))
async def start(message: Message):
    """Start buyrug'i - kanal a'zoligini tekshiradi"""

    # Admin uchun tekshiruv yo'q
    if message.from_user.id == ADMIN_ID:
        await message.answer("Salom Admin! 👋")
        return

    # Kanal a'zoligini tekshirish
    is_subscribed = await check_subscription(message.from_user.id, message.bot)

    if not is_subscribed:
        # Agar a'zo bo'lmasa - tugma ko'rsatish
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="💕Kanalga a'zo bo'lish", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")],
            [InlineKeyboardButton(text="✅ Tekshirish", callback_data="check_sub")]
        ])

        await message.answer(
            "⚠️ Botdan foydalanish uchun quyidagi kanalga a'zo bo'ling:\n\n"
            f"Kanal: {CHANNEL_USERNAME}\n\n"
            "A'zo bo'lganingizdan so'ng '✅ Tekshirish' tugmasini bosing.",
            reply_markup=keyboard
        )
        return

    # A'zo bo'lsa - oddiy start xabari
    await message.answer(
        f"😊Assalomu alaykum, {message.from_user.first_name}!\n\n"
        "📬 Bu bot orqali men bilan to'g'ridan-to'g'ri bog'lanishingiz mumkin.\n\n"
        "💬 Xabaringizni yuboring, tez orada javob beraman!"
    )


# Tekshirish tugmasi bosilganda
@dp.callback_query(lambda c: c.data == "check_sub")
async def check_sub_callback(callback):
    """A'zolikni qayta tekshirish"""
    is_subscribed = await check_subscription(callback.from_user.id, callback.bot)

    if is_subscribed:
        await callback.message.edit_text(
            f"😊 Rahmat, {callback.from_user.first_name}!\n\n"
            "📬 Endi xabaringizni yuboring, men javob beraman."
        )
    else:
        await callback.answer(
            "😒 Siz hali kanalga a'zo bo'lmadingiz!\n"
            "Avval kanalga a'zo bo'lib, keyin tekshiring.",
            show_alert=True
        )


@dp.message(Command("javob"))
async def reply_handler(message: Message):
    """Admin javob berish uchun"""
    if message.from_user.id != ADMIN_ID:
        return

    try:
        parts = message.text.split(maxsplit=2)
        user_id = int(parts[1])
        javob = parts[2]

        await message.bot.send_message(user_id, f"📬 Admin: {javob}")
        await message.answer("💕Javob yuborildi!")
    except:
        await message.answer("Format: /javob 987654321 Javob matni")


@dp.message()
async def forward_message(message: Message):
    """Xabarlarni boshqarish"""

    # Admin uchun
    if message.from_user.id == ADMIN_ID:
        if last_user:
            await message.bot.send_message(
                last_user['id'],
                f"📬 Admin: {message.text}"
            )
            await message.answer("💕 Javob yuborildi!")
        else:
            await message.answer("Hali hech kim xabar yozmagan")
        return

    # Oddiy foydalanuvchi uchun - kanal a'zoligini tekshirish
    is_subscribed = await check_subscription(message.from_user.id, message.bot)

    if not is_subscribed:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Kanalga a'zo bo'lish", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")],
            [InlineKeyboardButton(text="✅ Tekshirish", callback_data="check_sub")]
        ])

        await message.answer(
            "⚠️ Botdan foydalanish uchun avval kanalga a'zo bo'ling!",
            reply_markup=keyboard
        )
        return

    # A'zo bo'lsa - xabarni yuborish
    last_user['id'] = message.from_user.id
    last_user['name'] = message.from_user.first_name

    await message.answer("💕 Xabaringiz yuborildi!")

    await message.bot.send_message(
        ADMIN_ID,
        f"📩 Yangi xabar:\n\n"
        f"👤 Ism: {message.from_user.first_name}\n"
        f"🆔 Username: @{message.from_user.username or 'Yo\'q'}\n"
        f"🔢 ID: {message.from_user.id}\n\n"
        f"💬 Xabar:\n{message.text}"
    )


async def main():
    bot = Bot(token=TOKEN)
    print("🤖 Bot ishga tushdi!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())