import os
import random
import webbrowser
import playsound
import pyttsx3
import pywhatkit
import speech_recognition as sr
from gtts import gTTS


class assistenteVirtual():
    def __init__(self, nomedaAssistente, usuario):
        self.usuario = usuario
        self.nomedaAssistente = nomedaAssistente
        # Criar as variaveis que vamos utilizar
        self.maquina = pyttsx3.init()
        self.r = sr.Recognizer()  # reconhecer a voz
        self.voice_data = ''  # armazenar o texto do nosso audio

    def maquinaFalando(self, text):
        """
        fala da assitente virtual
        """
        text = str(text)  # conversao de texto para string
        self.maquina.say(text)  # vai dizer o nosso texto
        self.maquina.runAndWait()  # executar e esperar um pouco

    def gravarAudio(self, pergunta=""):

        with sr.Microphone() as source:  # usar a funcao do microfone
            os.system('clear') or None  # função para limpar tela do console
            if pergunta:
                print('gravando...')
                self.maquinaFalando(pergunta)  # vai falar o que agente está perguntando
            # pega dados de audio
            audio = self.r.listen(source, timeout=5, phrase_time_limit=5)
            print("olhando a base de dados")
            try:

                self.voice_data = self.r.recognize_google(audio, language='pt-BR')  # converte audio para texto

            except sr.UnknownValueError:
                # Quando não captar o Audio
                self.maquinaFalando('Você pode por favor repetir?')

            except sr.RequestError:

                self.maquinaFalando('Desculpe chefe, meu servidor está fora do ar')  # recognizer is not connected

            print(">>", self.voice_data.lower())  # imprime o que vc disse

            self.voice_data = self.voice_data.lower()

            return self.voice_data.lower()

    # Utilizar a voz direito para nao ficar com a voz estranha, configurar o Audio

    def maquinaFalando(self, sequenciaAudio):  # variavel
        sequenciaAudio = str(sequenciaAudio)  # converter o audio em texto
        tts = gTTS(text=sequenciaAudio, lang='pt-BR')  # pegar o tts e converter e salvar o audio em português
        r = random.randint(1, 2000)  # cada vez que for gravando ele não colocar o mesmo numero
        arquivoAudio = 'audio' + str(r) + '.mp3'  # arquivo que vai salvar em mp3
        tts.save(arquivoAudio)  # vai salvar o arquivo
        playsound.playsound(arquivoAudio)  # pyaudio para executar para sair o audio
        print(self.nomedaAssistente + ':', sequenciaAudio)  # audio em texto
        os.remove(arquivoAudio)  # remover o Audio

    def there_exist(self, terms):
        """
        função para identificar se o termo existe
        """
        for term in terms:  # se o que agente falar ele vai checar se tem no Dados_de_voz que e o nosso audio
            if term in self.voice_data:
                return True

    def respond(self, Dados_de_Voz):
        if self.there_exist(['oi']):
            saudacoes = [f'Olá {self.usuario},O que você precisa?']

            greet = saudacoes[
                random.randint(0, len(saudacoes) - 1)]  # Quantidade de saudações, e o -1 e para não passar.
            self.maquinaFalando(greet)  # aqui e as saudações que ela vai dizer depois que eu falar oi...

        # google(buscas)
        # pesquisar o que eu quiser e não pode ter a palavra youtube
        if self.there_exist(['pesquise por']) and 'youtube' not in Dados_de_Voz:
            search_term = Dados_de_Voz.split('por')[-1]  # -1 e para pegar depois do 'por'
            url = "https://www.google.de/search?q=" + search_term
            webbrowser.get().open(url)  # comando para abrir o browser
            # ela vai dizer com o que pedimos para pesquisar
            self.maquinaFalando("aqui está o que eu encontrei para " + search_term + 'no google')
        # youtube
        if self.there_exist(["procure no youtube por"]):
            search_term = Dados_de_Voz.split("por")[-1]
            url = "https://www.youtube.com/results?search_query=" + search_term
            webbrowser.get().open(url)
            self.maquinaFalando("aqui esta o que encontrei para" + search_term + 'no youtube')

        # spa (fazer o login automatico no sap) exemplo de como colocar
        if self.there_exist(['open sap']):
            pass

        # tocar uma musica direto no youtube
        if 'toque' in self.voice_data:
            musica = self.voice_data.replace('toque', '')
            pywhatkit.playonyt(musica)
            self.maquinaFalando('Tocando musica')

        if 'piada' in self.voice_data:
            self.maquinaFalando('ja ouviu a história do pinto sem cú....')
            self.maquinaFalando('Foi peidar e explodiu')
            self.maquinaFalando('kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk')


assistent = assistenteVirtual('Lana', 'André')  #
mensagem_anterior = ''

while True:  # executar e ficar aqui

    mensagem_atual = assistent.gravarAudio('ouvindo...')

    if mensagem_atual != mensagem_anterior:
        mensagem_anterior = mensagem_atual
        assistent.respond(mensagem_atual)  # vai dar a resposta de como a gente falar

    if assistent.there_exist(['bye', 'goodbye', 'até a próxima amigo', 'tchau']):  # termo para sair do loop
        assistent.maquinaFalando("Tenha um ótimo dia!!!")
        break
