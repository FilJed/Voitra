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
        "Привет! Это Бот для конвертации голосового/аудио сообщения в текст c таймкодами и выделением ключевых моментов в нем.\n"
        "Просто пришли или перешли мне голосовое сообщение и я сконвертирую его в текст.\n"
        "Добавь меня в чат и я сам автоматически буду отлавливать аудиосообщения и превращать их в текст.\n"
        "Я пока сырой и могу косячить, не ругайся.\n"
        "Из меркантильных соображений, длительность войса ограничена ~10 минутами.\n"
        "О всех чудесах писать сюда https://t.me/FilJed"
    )

async def save_audio_file(bot: Bot, file_id) -> str:
    """Скачивает голосовое сообщение и сохраняет в формате"""
    voice_file_info = await bot.get_file(file_id)
    logging.info(msg=f"file id:{file_id}\n, info: {voice_file_info}\n, path: {voice_file_info.file_path[-3:]} ")
    # voice_ogg = io.BytesIO()
    output_file_path = f"app/tracks/{file_id}.{voice_file_info.file_path[-3:]}"
    await bot.download_file(voice_file_info.file_path, output_file_path)
    return output_file_path


system_prompt = "Ты полезный помошник.  Опиши в 5-10 предложениях о чем был разговор и выдели ключевые моменты в нем. Описание не должно быть длиннее исходного текста. Если разговор содержит только посторонние звуки вместо речи, то так и напиши, что в представленном разговоре нет речи, а только набор звуков."

# Хендлер сообщений? TODO причесать
# @flag.chat_action(action=)
# @router.message(content_type=["voice", "audio"])
@router.message(F.content_type == "voice" | F.content_type == "audio")
# @router.message(F.content_type == "audio")
async def process_voice_message(message: Message, bot: Bot):
    """Принимает голосовое сообщение, транскрибирует его в текст."""
    if message.content_type == ContentType.VOICE:
        file_id = message.voice.file_id
        logging.info(msg="Got voice message")
    elif message.content_type == ContentType.AUDIO:
        file_id = message.audio.file_id
        logging.info(msg="Got audio message")
    voice_path = await save_audio_file(bot, file_id)
    transcripted_voice_text = "\n\nTimestamps:\n" + transcribe(voice_path)
    summed_text = gpt(0, system_prompt, transcripted_voice_text)
    text = summed_text + transcripted_voice_text

    if len(text)<4096:
        await message.reply(text=text)
    elif len(transcripted_voice_text)<4096:
        await message.reply(text=summed_text)
        await message.reply(text=transcripted_voice_text)
    else:
        await message.reply(text=summed_text)

async def main():
    bot: Bot = Bot(token=BOT_TOKEN)
    dp: Dispatcher = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())