import tempfile
import requests
import whisper

model = whisper.load_model("base")

async def transcribe(FILE_URL, ORIGINAL_MESSAGE, NEW_MESSAGE=None, REGENERATE=False, LANGUAGE=None):
    with tempfile.NamedTemporaryFile() as tmp:
        res = requests.get(FILE_URL)
        if res.status_code != 200:
            event.message.reply("I couldn't download audio message!")
            return
        tmp.write(res.content)

        print("RECEIVED NEW AUDIO MESSAGE!")
        if REGENERATE:
        	new_message = await NEW_MESSAGE.edit(content = "Regenerating transcription! Depending on the audio length, you may receive a response quickly or not.")
        else:
        	new_message = await ORIGINAL_MESSAGE.reply("Generating response! Depending on the audio length, you may receive a response quickly or not.")

        if LANGUAGE is None:
        	result = model.transcribe(tmp.name)
        else:
        	result = model.transcribe(tmp.name, language = LANGUAGE)

        if result['text'] == "":
            await new_message.edit(content="Nothing to transcribe!")
            return
        await new_message.edit(content=result['text'])
