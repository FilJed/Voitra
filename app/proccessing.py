import subprocess, re, os
from openai import OpenAI, BadRequestError

client = OpenAI()

# Openai is using old version of ffmpeg that cannot proccess some ogg files correctly. Wav is too havy :(
def audio_to_wav(audio):
    name = audio.split('.')[0]
    subprocess.call(f"ffmpeg -v quiet -y -i {audio} -vn -ar 16000 -ac 1 {name}.wav", shell=True)
    print(f"{name}.wav")
    return f"{name}.wav"

# # check file size is less then 25mb
# def size(audio):
#     if os.stat(audio).st_size > 25 * 1024 * 1024:
#         return True
#     else:
#         return False

def transcribe(audio):
    try:
        with open(audio, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                file = audio_file,
                model = "whisper-1",
                response_format="srt",
                prompt="Если вместо речи есть постороние звуки (к примеру: музыка), то опиши её (к примеру: *музыка на фоне*, *скрип*)."
            )
    except BadRequestError as e:
        print("Wait for audio to be processed")
        audio = audio_to_wav(audio)
        tr = transcribe(audio)
        return tr
    except FileNotFoundError as e:
        return "Логистика файлов сломалась"
    os.remove(audio)
    #TODO make it all as one function. fucking regexes
    transcript = re.sub("\n[0-9]+\n|,\d{3}", "", transcript)
    transcript = re.sub("(\d{2}:)+\d{2}\n", "", transcript)
    transcript = re.sub(r"(0{2}:)(\d{2}:\d{2})", r"\2", transcript)
    transcript = transcript.replace("--> ", "")
    return transcript[2:]

def gpt(temperature, prompt, text):
    text = client.chat.completions.create(
        model="gpt-3.5-turbo-16k-0613",
        temperature=temperature,
        messages=[
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": text
            }
        ]
    )
    return text.choices[0].message.content

