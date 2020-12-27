
# Audio Book (A basic text-to-speech program)

# imports
import pyttsx3
import PyPDF2

# PyPDF2 setup
book_directory=r'/my_drive/my_folder/my_file.pdf'

book = open(book_directory, 'rb')
pdfReader = PyPDF2.PdfFileReader(book)
start_page_no = 1
end_page_no = pdfReader.numPages

# pyttsx3 setup
speaker = pyttsx3.init()	# OSError: libespeak.so.1: cannot open shared object file: No such file or directory
							# sudo apt-get update && sudo apt-get install espeak ffmpeg libespeak1 (using Ubuntu: 20.10)
speaker.setProperty("rate", 145)	# Words/min rate chaning

voices = speaker.getProperty('voices') 		
speaker.setProperty('voice', voices[16].id)		# Voice changing

# Speaker code
for num in range(start_page_no, end_page_no):
    page = pdfReader.getPage(num)
    text = page.extractText()
    speaker.say(text)
    speaker.runAndWait()