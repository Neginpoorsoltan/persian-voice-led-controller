import speech_recognition as sr
import requests

NODEMCU_IP = "10.198.24.243"

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("say...")
        audio = r.listen(source, timeout=5, phrase_time_limit=3)
    return r.recognize_google(audio, language="fa-IR")

def parse_command(text):
    text = text.lower()

    if "روشن" in text:
        state = "on"
    elif "خاموش" in text:
        state = "off"
    else:
        return None

    if "همه" in text:
        return {"color": "all", "state": state}
    elif "هیچکدوم" in text or "هیچ کدوم" in text:
        return {"color": "all", "state": "off"}
    elif "سبز" in text:
        return {"color": "green", "state": state}
    elif "زرد" in text:
        return {"color": "yellow", "state": state}
    elif "قرمز" in text:
        return {"color": "red", "state": state}
    else:
        return None

def control_led(color, state):
    try:
        if color == "all":
            for c in ["green", "yellow", "red"]:
                url = f"http://{NODEMCU_IP}/led?color={c}&state={state}"
                requests.get(url, timeout=3)
        else:
            url = f"http://{NODEMCU_IP}/led?color={color}&state={state}"
            requests.get(url, timeout=3)
    except Exception as e:
        print("connection error:", e)


print("system ready")
while True:
    try:
        text = listen()
        print("heard:", text)
        cmd = parse_command(text)
        if cmd:
            control_led(cmd["color"], cmd["state"])
            print("LED", cmd["color"], "->", cmd["state"])
        else:
            print("command not recognized, try again")
    except sr.WaitTimeoutError:
        print("nothing heard, try again")
    except sr.UnknownValueError:
        print("could not understand, try again")
    except Exception as e:
        print("error:", e)