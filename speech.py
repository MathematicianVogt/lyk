from pygsr import Pygsr
speech = Pygsr()
speech.record(3) # duration in seconds (3)
phrase, complete_response = speech.speech_to_text('es_ES') # select the language
print phrase