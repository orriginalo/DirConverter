import os
import subprocess
from PIL import Image
from rich import print
from rich.console import Console
from pydub import AudioSegment
from time import perf_counter

# pip install rich pydub pillow

console = Console()

audio_ext = [".mp3", ".wav", ".flac", ".ogg", ".aac", ".m4a", ".wma", ".aiff", ".au", ".opus"]

pictures_ext = [".png", ".jpg", ".jpeg", ".webp", ".svg", ".tiff", ".heic", ".jfif", ".bmp", ".apng", ".avif", ".tif", ".tga", ".psd", ".eps", ".ai", ".indd", ".raw"]


audio_convertto    = ".opus" # Audio convert to
pictures_convertto = ".avif"  # Photo convert to
pictures_quality = 30  # Quality level for photos


def shorten_string(original_string, max_length=20, extention:str = ''):
		if len(original_string) > max_length:
				return original_string[:max_length - 3] + '.. ' + extention
		return f"{original_string}"
	
def convert_audio(path):
	for file in os.listdir(f"{path}"):
		name, extention = os.path.splitext(file)
		if extention != audio_convertto and extention in audio_ext and not os.path.isdir(file):
			audio_file_path = os.path.join(f"{path}", file)
			converted_file_path = os.path.join(f"{path}", f"{name}{audio_convertto}")
			print(f"AUDIO: [bold yellow]Converting: {shorten_string(file,20,extention)} [bold white]>>>[bold yellow] {shorten_string(name, 20)}{audio_convertto}", end='')
			
			# Конвертация файла в MP3
			start = perf_counter()
			sound = AudioSegment.from_file(audio_file_path)
			sound.export(converted_file_path, format=audio_convertto.replace(".", ""))
	 
			# Удаление оригинального файла (опционально)
			os.remove(audio_file_path)
			end = perf_counter()
			
			elapsed_time = end - start
			print(f" [bold green] Succerfully! [/bold green]{elapsed_time:.1f} sec")
	print("\n")
def convert_photo(path):
	for file in os.listdir(path):
		name, extention = os.path.splitext(file)
		if extention != pictures_convertto and extention in pictures_ext and not os.path.isdir(file):
			input_path = os.path.join(path, file)
			output_path = os.path.join(path, f"{name}{pictures_convertto}")
			
			# Формируем команду для конвертации с помощью FFmpeg
			command = [
					'ffmpeg',
					'-i', input_path,
					'-c:v', 'libaom-av1',
					'-crf', str(pictures_quality),  # Уровень качества (можно настроить)
					'-pix_fmt', 'yuv420p',
					output_path
			]
			
	 
			print(f"IMAGE: [bold yellow]Converting: {shorten_string(file,20,extention)} [bold white]>>>[bold yellow] {shorten_string(name, 20)}{pictures_convertto}", end='')
			try:
					# Запускаем команду
					start = perf_counter()
					cmd = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
					os.remove(input_path)
					end = perf_counter()
			
					elapsed_time = end - start
					print(f" [bold green] Successfully! [/bold green]{elapsed_time:.1f} sec")
			except subprocess.CalledProcessError as e:
					print(f" [bold red]ERROR")
	print("\n")


def main():
	print("========[bold green]SUPER-CONVERTER[/bold green]========")
	path = str(console.input("[yellow]Select a folder: "))

	while os.path.exists(path) == False:
		path = str(console.input("[red]Folder not found. [/red]Try again: "))
	
	print(f"[bold green]Folder selected")

	print("Select a variant(s):")
	print(f"1. Audio to [bold]{audio_convertto}")
	print(f"2. Images to [bold]{pictures_convertto}")
	variant = list(dict.fromkeys([int(x) for x in input("Enter your choice: ").split() if int(x) <= 2]))
	
	for i in variant:
		match i:
			case 1:
				convert_audio(path)
			case 2:
				convert_photo(path)
				
	print("[bold green]Files converted successfully!")
	
if __name__ == "__main__":
	main()