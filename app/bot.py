from proccessing import transcribe, gpt
import asyncio, os, io
from aiogram import Bot, Dispatcher, F, Router
from aiogram.types import Message, Voice

BOT_TOKEN = os.getenv("BOT_TOKEN")


# audio='app/tracks/test1.ogg'
# response = transcribe(audio)
# print(response)

system_prompt = "Ты полезный помошник. Опиши в 5-10 предложениях о чем был разговор и выдели ключевые моменты в нем. Описание не должно быть длиннее исходного текста. Если разговор содержит только посторонние звуки вместо речи, то так и напиши, что в представленном разговоре нет речи, а только набор звуков."
# summed_text = gpt(0, system_prompt, response)
# print(summed_text)

router: Router = Router()

async def save_voice_as_mp3(bot: Bot, voice: Voice) -> str:
    """Скачивает голосовое сообщение и сохраняет в формате mp3."""
    voice_file_info = await bot.get_file(voice.file_id)
    # voice_ogg = io.BytesIO()
    await bot.download_file(voice_file_info.file_path, f"app/tracks/{voice.file_id}.ogg")
    voice_path = f"app/tracks/{voice.file_id}.ogg"
    return voice_path

# Хендлер сообщений с которым будем работать
@router.message(F.content_type == "voice")
async def process_voice_message(message: Message, bot: Bot):
    """Принимает голосовое сообщение, транскрибирует его в текст."""
    voice_path = await save_voice_as_mp3(bot, message.voice)
    transcripted_voice_text = transcribe(voice_path)
    summed_text = gpt(0, system_prompt, transcripted_voice_text)
    text = "tldr:\n" + summed_text + "\n\n Timestamps:\n" + transcripted_voice_text

    if transcripted_voice_text:
        await message.reply(text=text)

# @router.message(F.content_type == "voice")
# async def process_message(message: Message):
#     """Принимает все голосовые сообщения и отвечает эхо."""
#     await message.answer(text="echo")

async def main():
    bot: Bot = Bot(token=BOT_TOKEN)
    # bot.delete_webhook()
    dp: Dispatcher = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())