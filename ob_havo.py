import asyncio
import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

TOKEN = "8100238469:AAHeLqOzip7AfSWgc0el9siBoScvFWQm6fY"
viloyatlar = {
    "Toshkent": ["41.3351", "69.2299"],
    "Sirdaryo": ["40.8711", "68.7103"],
    "Qashqadaryo": ["38.9288", "65.7436"],
    "Surxondaryo": ["37.9382", "67.5627"],
    "Samarqand": ["39.6645", "67.1848"],
    "Jizzax": ["40.1431", "67.9883"],
    "Buxoro": ["39.7807", "64.5670"],
    "Qoraqalpogiston": ["43.8160", "59.4695"],
    "Xorazm": ["41.5307", "60.5952"],
    "Navoiy": ["40.1160", "65.5065"],
    "Andijon": ["40.8133", "72.2834"],
    "Fargona": ["40.3685", "71.7693"]
}

dp = Dispatcher()
@dp.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(
        "Assalomu alaykum! 👋\n\n"
        "Viloyat nomini yuboring:\n"
    )
@dp.message(Command(*viloyatlar.keys()))
async def obhavo_handler(message: Message):
    viloyat = message.text[1:]  # "/" ni olib tashlash
    lat, lon = viloyatlar[viloyat]
    async with aiohttp.ClientSession() as session:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=apparent_temperature_max&timezone=Etc/GMT-5"
        async with session.get(url) as response:
            data = await response.json()
            harorat = data["daily"]["apparent_temperature_max"][0]
            sana = data["daily"]["time"][0]
            await message.answer(
                f"🌤 {viloyat} ob-havo:\n\n"
                f"🌡 Harorat: {harorat}°C\n"
                f"Sana: {sana}"

            )
async def main():
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())