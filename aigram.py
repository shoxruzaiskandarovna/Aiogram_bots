import asyncio
import aiohttp

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

TOKEN = "8314898028:AAHkfuP4sBnwUDKxMVqibx80mWKO1FNwJ5c"
API_KEY = "28014de4385a212c57801796"
dp = Dispatcher()

@dp.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    await message.reply("Salom botimizga hush kelibsiz!✋")


@dp.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    await message.answer(
        "Buyruqlar:\n"
        "/start – Botni boshlash\n"
        "/help – Yordam\n"
        "/kursdolar – Dollar kursi"
    )


@dp.message(Command("kursdolar"))
async def command_kursdolar_handler(message: Message) -> None:
    async with aiohttp.ClientSession() as session:
        url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD"
        async with session.get(url) as response:
            data = await response.json()

            uzs_rate = data["conversion_rates"]["UZS"]
            rub_rate = data["conversion_rates"]["RUB"]
            eur_rate = data["conversion_rates"]["EUR"]

            await message.answer(
                f"Dollar kurslari:\n\n"
                f"🇺🇿 1 USD = {uzs_rate:,.2f} UZS\n"
                f"🇷🇺 1 USD = {rub_rate:,.2f} RUB\n"
                f"🇪🇺 1 USD = {eur_rate:.4f} EUR"
            )

async def main() -> None:
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

