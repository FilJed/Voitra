from proccessing import transcribe, gpt
import asyncio, os, io
from aiogram import Bot, Dispatcher, F, Router
from aiogram.utils.chat_action import ChatActionMiddleware
from aiogram.types import ContentType, Message, Voice, Audio
from aiogram.filters.command import Command

import logging
logging.basicConfig(level=logging.INFO, filename="bot.log")


BOT_TOKEN = os.getenv("BOT_TOKEN")
router: Router = Router()

# Show bot is proccessing
router.message.middleware(ChatActionMiddleware())

# Хэндлер на команду /start , /help
@router.message(Command("start", "help"))
async def cmd_start(message: Message):
    await message.reply(
        "Привет! Это Бот для конвертации голосового/аудио сообщения в текст c таймкодами и выделением ключевых моментов в нем."
        "Просто пришли или перешли мне голосовое сообщение и я сконвертирую его в текст."
        "Добавь меня в чат и я сам автоматически буду отлавливать аудиосообщения и превращать их в текст."
        "Я пока сырой и могу косячить, не ругайся."
    )

async def save_voice_as_mp3(bot: Bot, file_id) -> str:
    """Скачивает голосовое сообщение и сохраняет в формате mp3."""
    voice_file_info = await bot.get_file(file_id)
    # voice_ogg = io.BytesIO()
    await bot.download_file(voice_file_info.file_path, f"app/tracks/{file_id}.ogg")
    voice_path = f"app/tracks/{file_id}.ogg"
    return voice_path


system_prompt = "Ты полезный помошник. Опиши в 5-10 предложениях о чем был разговор и выдели ключевые моменты в нем. Описание не должно быть длиннее исходного текста. Если разговор содержит только посторонние звуки вместо речи, то так и напиши, что в представленном разговоре нет речи, а только набор звуков."

# Хендлер сообщений с которым будем работать
# @router.message(content_type=["voice", "audio"])
@router.message(F.content_type == "voice" or "audio")
# @flag.chat_action(action=)
async def process_voice_message(message: Message, bot: Bot):
    """Принимает голосовое сообщение, транскрибирует его в текст."""

    # Sending indication that bot is proccessing message
    # await bot.send_chat_action(message.chat.id, action=ChatActionSender.typing)

    if message.content_type == ContentType.VOICE:
        file_id = message.voice.file_id
    elif message.content_type == ContentType.AUDIO:
        file_id = message.audio.file_id
    voice_path = await save_voice_as_mp3(bot, file_id)
    transcripted_voice_text = transcribe(voice_path)
    summed_text = gpt(0, system_prompt, transcripted_voice_text)
    text = "tldr:\n" + summed_text + "\n\n Timestamps:\n" + transcripted_voice_text

    if transcripted_voice_text:
        await message.reply(text=text)

async def main():
    bot: Bot = Bot(token=BOT_TOKEN)
    dp: Dispatcher = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())