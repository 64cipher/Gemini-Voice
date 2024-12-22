import google.generativeai as genai
import speech_recognition as sr
import pyttsx3
import os
import simpleaudio as sa


# Remplacez par votre clé API Google Gemini
GOOGLE_API_KEY = "API-KEY-HERE"
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('gemini-2.0-flash-exp')


def parler(texte, vitesse=175, voix_id=None):
    engine = pyttsx3.init()
    engine.setProperty('rate', vitesse)  # Ajuste la vitesse

    if voix_id:
        engine.setProperty('voice', voix_id)
    else:
      voices = engine.getProperty('voices') # permet de récupérer la liste des voix
      for index, voice in enumerate(voices):
            print(f"Voice {index}: {voice.name}") # permet d'afficher le nom de chaque voix disponible
            if 'french' in voice.name.lower(): # On selectionne la première voix française si pas de voix_id
              engine.setProperty('voice', voice.id)
              break

    engine.save_to_file(texte, 'reponse.mp3')
    engine.runAndWait()
    engine.stop()
    wave_obj = sa.WaveObject.from_wave_file("reponse.mp3")
    play_obj = wave_obj.play()
    play_obj.wait_done()
    os.remove("reponse.mp3")


def ecouter():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("En attente de 'Gemini'...")
        r.adjust_for_ambient_noise(source)
        while True:
            try:
                audio = r.listen(source)
                texte = r.recognize_google(audio, language="fr-FR")
                print(f"Vous avez dit: {texte}")
                if "gemini" in texte.lower():
                    parler("y a quoi sale fou", 190)
                    return True
            except sr.UnknownValueError:
                print("Je n'ai pas compris.")
            except sr.RequestError as e:
                print(f"Erreur de requête: {e}")


def parler_gemini():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Parlez à Gemini...")
        r.adjust_for_ambient_noise(source)
        try:
            audio = r.listen(source)
            texte = r.recognize_google(audio, language="fr-FR")
            print(f"Vous avez dit: {texte}")
            response = model.generate_content(texte)
            parler(response.text, 175)

        except sr.UnknownValueError:
            print("Je n'ai pas compris.")
        except sr.RequestError as e:
            print(f"Erreur de requête: {e}")


if __name__ == "__main__":
    while True:
        if ecouter():
            parler_gemini()