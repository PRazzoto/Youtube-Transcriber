from openai import OpenAI
import yt_dlp
import whisper


def getkey():
    try:
        with open("apikey", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        print("'%s' file not found" % "apikey")


def download_audio(url, output_path="audio"):
    ydl_opts = {
        "format": "bestaudio/best",  # Baixar o melhor áudio disponível
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",  # Extrair apenas o áudio
                "preferredcodec": "mp3",  # Converter para MP3
                "preferredquality": "192",  # Qualidade do áudio
            }
        ],
        "outtmpl": output_path,  # Caminho para salvar o arquivo de saída
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"Áudio baixado com sucesso e salvo em {output_path}")

    except Exception as e:
        print(f"Erro ao baixar o áudio: {e}")


def transcribe_audio(audio_file):
    try:
        model = whisper.load_model("base")
        result = model.transcribe(audio_file)
        print("Transcrição do áudio:\n", result["text"])
    except Exception as e:
        print(f"Erro ao transcrever o áudio: {e}")


def openai_api(transcription):
    completion = client.chat.completions.create(
        model=f"gpt-3.5-turbo",
        messages=[
            {
                "roles": "user",
                "content": f"Give me a summary of this transcript with Title, Subtitles and Bullet Points:{transcription}",
            }
        ],
    )

    return completion.choices[0].message.content


def main_function(youtube_url):
    audio_file = "audio.mp3"
    download_audio(url=youtube_url)
    transcription = transcribe_audio(audio_file)
    print(openai_api(transcription=transcription))


youtube_url = input("Type the video URL that you wish to be Summarized:")
api_key = getkey()
print(api_key)
client = OpenAI(api_key)
main_function(youtube_url)
