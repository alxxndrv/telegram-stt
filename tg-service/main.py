import json
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from client import transcription_client
from transcription_service_pb2 import VoiceMessageRequest, TranscriptionResponse
import os

API_TOKEN = os.getenv('TG_BOT_TOKEN')

logging.basicConfig(level=logging.INFO)


bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(content_types=types.ContentTypes.VOICE)
async def handle_voice_message(message: types.Message):

    transcribing_message = await message.reply("Transcribing...")

    file_id = message.voice.file_id

    file = await bot.get_file(file_id)

    file_url = f"https://api.telegram.org/file/bot{API_TOKEN}/{file.file_path}"

    request = VoiceMessageRequest(file_id=file_url)
    try:
        response = transcription_client.TranscribeVoiceMessage(request)
        transcription_text = response.text if response else "Failed to transcribe"
    except Exception as e:
        logging.error("Error during transcription: %s", e)
        transcription_text = "Error in transcription process"

    await transcribing_message.edit_text(transcription_text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
