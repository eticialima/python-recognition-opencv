import cv2
import kivy

kivy.require('1.9.1') 

from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.app import App
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.core.window import Window

# COR DA JANELA E TAMANHO
Window.clearcolor = (0.5, 0.5, 0.5, 1)
Window.size = (980, 720)

# CAMERA NO KIVY CONFIGURAÇÃO
class KivyCV(Image):
    def __init__(self, capture, fps, **kwargs):
        Image.__init__(self, **kwargs)
        self.capture = capture
        Clock.schedule_interval(self.update, 1.0 / fps)

    # CONFIGURAÇÃO PARA DETECTAR FACE
    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faceCascade = cv2.CascadeClassifier("lib/haarcascade_frontalface_default.xml")
            faces = faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(20, 20))
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # TRANSFORMANDO UMA IMAGEM EM TEXTURA PARA COLOCAR A CAMERA
            buf = cv2.flip(frame, 0).tostring()
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            # display image from the texture
            self.texture = image_texture


# FUNÇÃO DO SCREAN PARA MUDAR DE TELA
class SISTEMA(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(WelcomeScreen(name='welcomeScreen'))
        sm.add_widget(FunctionScreen(name='functionScreen'))
        return sm

# PRIMEIRA TELA DO SUB-SCREEN
class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs)
        layout1 = FloatLayout()
        box = BoxLayout(orientation='horizontal', size_hint=(0.4, 0.2), padding=8, pos_hint={'top': 0.2, 'center_x': 0.5})
        tituloscreen1 = Label(text='CLIQUE EM FOTOS PARA CADASTRAR AS FACES PARA O RECONHECIMENTO',color =[1, 0, 0, 1], halign='center',
                              font_name = 'Roboto-Bold', valign='center', size_hint=(0.4, 0.2), pos_hint={'top': 0.3, 'center_x': 0.5})

        # TILULO DO PROGRAMA
        self.title1 = Label(text='SISTEMA DE CADASTRO')
        self.title1.font_size = '60sp'
        self.title1.color = [1, 25, 91, 1]
        self.title1.font_name = 'Roboto-Bold'
        self.title1.size_hint = (.99, .99)
        self.title1.pos_hint = {'x': .0, 'y': .40}

        # CONFIGURAÇÃO DO BOTÃO TIRAR FOTOS
        FOTO = Button(text='FOTOS', on_press=self.tirarfoto)

        # CONFIGURAÇÃO DO BOTÃO CADASTRO
        CADASTRAR = Button(text='CADASTRAR', on_press=self.cadastrar)

        # CAMPO NOME: CAIXA E TEXTO INPUT
        self.caixatexto = (Label(text="NOME:"))
        self.caixatexto.size_hint = (.005, .07)
        self.caixatexto.font_size = 26
        self.caixatexto.pos_hint = {'x': .21, 'y': .72}
        self.username = TextInput(multiline=False)
        self.username.write_tab = False
        self.username.size_hint = (.5, .07)
        self.username.font_size = 26
        self.username.pos_hint = {'x': .30, 'y': .72}

        # CAMPO CPF: CAIXA E TEXTO INPUT
        self.caixatextocpf = (Label(text="CPF:"))
        self.caixatextocpf.size_hint = (.005, .07)
        self.caixatextocpf.font_size = 26
        self.caixatextocpf.pos_hint = {'x': .21, 'y': .60}
        self.cpf = TextInput(multiline=False)
        self.cpf.write_tab = False
        self.cpf.size_hint = (.5, .07)
        self.cpf.font_size = 26
        self.cpf.pos_hint = {'x': .30, 'y': .60}

        # CAMPO CARGO: CAIXA E TEXTO INPUT
        self.caixatextocargo = (Label(text="CARGO:"))
        self.caixatextocargo.size_hint = (.005, .07)
        self.caixatextocargo.font_size = 26
        self.caixatextocargo.pos_hint = {'x': .21, 'y': .48}
        self.cargo = TextInput(multiline=False)
        self.cargo.write_tab = False
        self.cargo.size_hint = (.5, .07)
        self.cargo.font_size = 26
        self.cargo.pos_hint = {'x': .30, 'y': .48}

        # CAMPO EMAIL: CAIXA E TEXTO INPUT
        self.caixatextoemail = (Label(text="E-MAIL:"))
        self.caixatextoemail.size_hint = (.005, .07)
        self.caixatextoemail.font_size = 26
        self.caixatextoemail.pos_hint = {'x': .21, 'y': .36}
        self.email = TextInput(multiline=False)
        self.email.write_tab = False
        self.email.size_hint = (.5, .07)
        self.email.font_size = 26
        self.email.pos_hint = {'x': .30, 'y': .36}

        # LAYOUT PARA MOSTRAR OS WIDGET NA TELA
        # WIDGETS BOXLAYOUT
        box.add_widget(CADASTRAR)
        box.add_widget(FOTO)

        # WIDGETES FLOATLAYOUT
        layout1.add_widget(box)
        layout1.add_widget(self.title1)
        layout1.add_widget(self.username)
        layout1.add_widget(self.caixatexto)
        layout1.add_widget(self.cpf)
        layout1.add_widget(self.caixatextocpf)
        layout1.add_widget(self.cargo)
        layout1.add_widget(self.caixatextocargo)
        layout1.add_widget(self.email)
        layout1.add_widget(self.caixatextoemail)
        layout1.add_widget(tituloscreen1)

        # CONFIGURAÇÃO LAYOUT1
        self.add_widget(layout1)

    # FUNÇÃO DO CLIQUE PARA IR TIRAR AS FOTOS
    def tirarfoto(self, instance):
        print('VOCE FOI PARA TELA 2')
        self.manager.current = 'functionScreen'

    # FUNÇÃO DO CLIQUE CADASTRAR
    def cadastrar(self, instance):
        name = self.username.text
        cpf = self.cpf.text
        cargo = self.cargo.text
        email = self.email.text
        print("Name:", name, "\nCPF:", cpf, "\nCargo:", cargo, "\nEmail:", email)

        print('CADASTRO EFETUADO COM SUCESSO')



# SEGUNDA TELA DO SCREEN
class FunctionScreen(Screen):
    def __init__(self, **kwargs):
        super(FunctionScreen, self).__init__(**kwargs)
        layout2 = FloatLayout()
        tituloscreen2 = Label(text='CLIQUE NO BOTÃO FOTO PARA REGISTRAR AS FACES NO BANDO DE DADOS'
                               '\nATENÇÃO APÓS TIRAR AS 30 FOTOS CLIQUE EM VOLTAR PARA CONFIRMAR O CADASTRO',
                              halign='center', valign='center', size_hint=(0.4, 0.2),
                              color =[1, 0, 0, 1], pos_hint={'top': 1, 'center_x': 0.5})

        # CONFIGURAÇÃO DO FLOATLAYOUT
        self.add_widget(layout2) 

        # CONFIGURAÇÕES DO BOTÃO VOLTAR
        self.botaoClick1 = Button(text='VOLTAR')
        self.botaoClick1.size_hint = (.2, .1)
        self.botaoClick1.pos_hint = {'x': .55, 'y': .50}

        # CONFIGURAÇÕES DO BOTÃO TIRAR FOTOS
        self.botaoClick2 = Button(text='TIRAR FOTOS')
        self.botaoClick2.size_hint = (.2, .1)
        self.botaoClick2.pos_hint = {'x': .25, 'y': .50}

        # FUNÇÃO DE CLICK DO BOTÃO VOLTAR
        self.botaoClick1.bind(on_press=self.voltar)
        self.botaoClick2.bind(on_press=self.fotofaces)

        # LAYOUT PARA MOSTRAR OS WIDGET NA TELA
        layout2.add_widget(tituloscreen2) 
        layout2.add_widget(self.botaoClick1)
        layout2.add_widget(self.botaoClick2)

        # RETORNA PARA O WIDGET

    # FUNÇÃO DO CLIQUE VOLTAR
    def voltar(self, *args):
        print('VOCE CLICOU NO BOTÃO VOLTAR')
        self.manager.current = 'welcomeScreen'

    # FUNÇÃO DO CLIQUE PARA EXTRAIR AS FACES
    def fotofaces(self, *args):
        print('VOCE CLICOU NO BOTÃO TIRAR FOTOS')

        # CODIGO PARA EXTRAIR AS IMAGENS
        def face_extractor(img):
            face_classifier = cv2.CascadeClassifier("lib/haarcascade_frontalface_default.xml")
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            faces = face_classifier.detectMultiScale(gray,1.3,5)

            if faces is():
                return None

            for(x,y,w,h) in faces:
                cropped_face = img[y:y+h, x:x+w]

            return cropped_face


        cap = cv2.VideoCapture(0)
        count = 0

        while True:
            ret, frame = cap.read()
            if face_extractor(frame) is not None:
                count+=1
                face = cv2.resize(face_extractor(frame),(200,200))
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

                file_name_path = 'faces/user'+str(count)+'.jpg'
                cv2.imwrite(file_name_path,face)

                cv2.putText(face,str(count),(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),2)
                cv2.imshow('Face Cropper',face)
            else:
                print("Face not Found")
                pass

            if cv2.waitKey(1)==13 or count==100:
                break

        cap.release()
        cv2.destroyAllWindows()
        print('Colleting Samples Complete!!!')
        
# FIM DO SISTEMA
if __name__ == '__main__':
    SISTEMA().run()
