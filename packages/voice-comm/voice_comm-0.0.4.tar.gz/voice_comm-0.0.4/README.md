# Voice Communication

With this package you can create programs which can speak to you and recognize your voice adn run commands. (easy eg.: You can create J.A.R.V.I.S from Iron Man :))

Supported language is python 3. (Package wrote in 3.9.6)

## Installation
Use this command:

    pip install voice-comm

## Change Log

0.0.4 (10/09/2021)
-------------------
- Added modules option | Load modules / Stop modules
- Fixing some issue

## Help

Help:

    import voice_comm

    voice = voice_comm.VoiceComm(language="en-EN") # Here you can specify rate, volume, voice (this voice is choose from voice tokens [HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens])

    voice.load_modules("test")

    @voice.add_command(or_required_words=["hi", "hello"], words=["Da4ndo"]) #Here you can specify is_capital_letters_matter [default: False], required_words, words and or_required_words (or_required_words is very similar to required_words but if its contaion more, its don't require all words, just one)
    def hello():
        voice.say("Hello word!")

    text = voice.recognize() # Here you can specify phrase_time_limit, timeout, snowboy_configuration. Advanced: only ``phrase_time_limit`` and value ``5``

    voice.recognize_command(text) # hello function will call if you say ``hello`` or ``hi``

How to load module:

    # File name ``test.py`` | Can be modified.

    import datetime

    class Mod():
        def __init__(self, engine):
            self.engine = engine
        
        def run(self):
            @self.engine.add_command(is_capital_letters_matter=True, words=["Microsoft"])
            def test(text):
                print(text)
                self.engine.say("Test sikeres!")

            @self.engine.add_command(or_required_words=["idő", "óra"], words=["hány", "mennyi"])
            def time():
                time = str(datetime.datetime.now().replace(microsecond=0)).replace("-", ".")
                print(f"[RESPOND] {time}")
                self.engine.say(time)
        
    def setup(engine):
        Mod(engine).run()