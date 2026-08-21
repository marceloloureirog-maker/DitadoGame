from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.modalview import ModalView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.graphics import Color, RoundedRectangle, Line, Ellipse
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp

import os
import sys
import random


# ============================================================
# CAMINHOS DOS ARQUIVOS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


def caminho_arquivo(*partes):
    return os.path.join(BASE_DIR, *partes)


def localizar_fundo():

    caminhos = [
        caminho_arquivo("imagens", "fundo_jogo.jpeg"),
        caminho_arquivo("imagens", "fundo_jogo.jpg"),
        caminho_arquivo("imagens", "fundo_jogo.png"),
        caminho_arquivo("fundo_jogo.jpeg"),
        caminho_arquivo("fundo_jogo.jpg"),
        caminho_arquivo("fundo_jogo.png"),
    ]

    for caminho in caminhos:

        if os.path.isfile(caminho):
            print("FUNDO ENCONTRADO:", caminho)
            return caminho

    print("AVISO: imagem de fundo não encontrada.")

    return ""


FUNDO_JOGO = localizar_fundo()


# ============================================================
# BALÃO ANIMADO
# ============================================================

class BalaoAnimado(FloatLayout):

    def on_touch_down(self, touch):
        return False

    def on_touch_move(self, touch):
        return False

    def on_touch_up(self, touch):
        return False

    def __init__(
        self,
        x=0,
        y=0,
        tamanho=50,
        cor=(1, 0.2, 0.3, 1),
        **kwargs
    ):

        super().__init__(**kwargs)

        self.size = (
            dp(tamanho),
            dp(tamanho * 1.25)
        )

        self.pos = (x, y)

        self.tamanho = dp(tamanho)
        self.cor_balao = cor

        with self.canvas:

            Color(*self.cor_balao)

            self.corpo = Ellipse(
                pos=self.pos,
                size=(
                    self.tamanho,
                    self.tamanho * 1.15
                )
            )

            Color(
                1,
                1,
                1,
                0.70
            )

            self.brilho = Ellipse(
                pos=(
                    self.x + self.tamanho * 0.22,
                    self.y + self.tamanho * 0.72
                ),
                size=(
                    self.tamanho * 0.16,
                    self.tamanho * 0.24
                )
            )

            Color(*self.cor_balao)

            self.bico = Ellipse(
                pos=(
                    self.x + self.tamanho * 0.43,
                    self.y - self.tamanho * 0.03
                ),
                size=(
                    self.tamanho * 0.14,
                    self.tamanho * 0.12
                )
            )

            Color(
                0.20,
                0.20,
                0.20,
                0.65
            )

            self.cordao = Line(
                points=[
                    self.x + self.tamanho * 0.50,
                    self.y,
                    self.x + self.tamanho * 0.50,
                    self.y - self.tamanho * 0.70
                ],
                width=1
            )

        self.bind(
            pos=self.atualizar_desenho
        )

    def atualizar_desenho(self, *args):

        self.corpo.pos = self.pos

        self.brilho.pos = (
            self.x + self.tamanho * 0.22,
            self.y + self.tamanho * 0.72
        )

        self.bico.pos = (
            self.x + self.tamanho * 0.43,
            self.y - self.tamanho * 0.03
        )

        self.cordao.points = [
            self.x + self.tamanho * 0.50,
            self.y,
            self.x + self.tamanho * 0.50,
            self.y - self.tamanho * 0.70
        ]


# ============================================================
# CAMADA DOS BALÕES
# ============================================================

class CamadaBaloes(FloatLayout):

    def on_touch_down(self, touch):
        return False

    def on_touch_move(self, touch):
        return False

    def on_touch_up(self, touch):
        return False

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.baloes = []

    def comemorar(self):

        for balao in self.baloes[:]:

            try:
                Animation.cancel_all(balao)
            except Exception:
                pass

            if balao.parent:
                self.remove_widget(balao)

        self.baloes.clear()

        cores = [
            (1.00, 0.20, 0.30, 1),
            (0.20, 0.55, 1.00, 1),
            (1.00, 0.75, 0.10, 1),
            (0.30, 0.80, 0.35, 1),
            (0.70, 0.35, 1.00, 1),
            (1.00, 0.45, 0.15, 1),
            (0.15, 0.80, 0.80, 1),
            (1.00, 0.35, 0.70, 1),
        ]

        quantidade = random.randint(10, 14)

        largura = self.width
        altura = self.height

        if largura <= 0:
            largura = dp(800)

        if altura <= 0:
            altura = dp(600)

        for i in range(quantidade):

            tamanho = random.randint(35, 55)

            largura_disponivel = max(
                dp(10),
                largura - dp(tamanho) - dp(10)
            )

            x = random.uniform(
                dp(10),
                largura_disponivel
            )

            y = random.uniform(
                -dp(100),
                -dp(20)
            )

            cor = random.choice(cores)

            balao = BalaoAnimado(
                x=x,
                y=y,
                tamanho=tamanho,
                cor=cor
            )

            self.add_widget(balao)

            self.baloes.append(balao)

            deslocamento_x = random.randint(
                -160,
                160
            )

            destino_x = (
                x +
                dp(deslocamento_x)
            )

            destino_x = max(
                dp(5),
                min(
                    destino_x,
                    largura - dp(tamanho) - dp(5)
                )
            )

            destino_y = (
                altura +
                random.randint(60, 180)
            )

            duracao = random.uniform(
                3.0,
                4.5
            )

            animacao = Animation(
                x=destino_x,
                y=destino_y,
                duration=duracao,
                t="out_quad"
            )

            animacao.bind(
                on_complete=self.remover_balao
            )

            animacao.start(balao)

    def remover_balao(
        self,
        animation,
        balao
    ):

        if balao.parent:
            self.remove_widget(balao)

        if balao in self.baloes:
            self.baloes.remove(balao)


# ============================================================
# BOTÃO BONITO
# ============================================================

class BotaoBonito(Button):

    def __init__(
        self,
        texto,
        cor=(0.25, 0.55, 0.90, 0.95),
        largura=180,
        altura=52,
        fonte=17,
        **kwargs
    ):

        super().__init__(**kwargs)

        self.text = texto
        self.font_size = fonte
        self.bold = True

        self.size_hint = (
            None,
            None
        )

        self.size = (
            dp(largura),
            dp(altura)
        )

        self.background_normal = ""
        self.background_down = ""

        self.background_color = (
            0,
            0,
            0,
            0
        )

        self.cor_normal = cor

        with self.canvas.before:

            self.cor = Color(
                *self.cor_normal
            )

            self.fundo = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(14)]
            )

            self.borda = Color(
                1,
                1,
                1,
                0.45
            )

            self.linha = Line(
                rounded_rectangle=(
                    self.x,
                    self.y,
                    self.width,
                    self.height,
                    dp(14)
                ),
                width=1.2
            )

        self.bind(
            pos=self.atualizar_visual,
            size=self.atualizar_visual
        )

        self.bind(
            state=self.mudar_estado
        )

    def atualizar_visual(
        self,
        *args
    ):

        self.fundo.pos = self.pos
        self.fundo.size = self.size

        self.linha.rounded_rectangle = (
            self.x,
            self.y,
            self.width,
            self.height,
            dp(14)
        )

    def mudar_estado(
        self,
        instance,
        estado
    ):

        if estado == "down":

            self.cor.rgba = (
                self.cor_normal[0] * 0.80,
                self.cor_normal[1] * 0.80,
                self.cor_normal[2] * 0.80,
                self.cor_normal[3]
            )

        else:

            self.cor.rgba = (
                self.cor_normal[0],
                self.cor_normal[1],
                self.cor_normal[2],
                self.cor_normal[3]
            )


# ============================================================
# TELA DE PROGRESSO
# ============================================================

class TelaProgresso(FloatLayout):

    def __init__(
        self,
        jogo,
        voltar_callback,
        **kwargs
    ):

        super().__init__(**kwargs)

        self.jogo = jogo
        self.voltar_callback = voltar_callback

        self.fundo = Image(
            source=FUNDO_JOGO,
            size_hint=(1, 1),
            pos_hint={
                "x": 0,
                "y": 0
            },
            allow_stretch=True,
            keep_ratio=False
        )

        self.add_widget(self.fundo)

        self.painel = FloatLayout(
            size_hint=(0.48, 0.88),
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.50
            }
        )

        with self.painel.canvas.before:

            Color(
                1,
                1,
                1,
                0.88
            )

            self.painel_fundo = RoundedRectangle(
                pos=self.painel.pos,
                size=self.painel.size,
                radius=[dp(25)]
            )

        self.painel.bind(
            pos=self.atualizar_painel,
            size=self.atualizar_painel
        )

        self.add_widget(self.painel)

        titulo = Label(
            text="MEU PROGRESSO",
            font_size="27sp",
            bold=True,
            color=(0.15, 0.25, 0.55, 1),
            size_hint=(1, None),
            height=dp(50),
            pos_hint={
                "center_x": 0.5,
                "top": 0.94
            }
        )

        self.painel.add_widget(titulo)

        acertos = jogo.acertos
        erros = jogo.erros
        pontos = jogo.pontos
        nivel = jogo.nivel
        sequencia = jogo.sequencia
        melhor = jogo.melhor_sequencia

        total = acertos + erros

        if total > 0:
            aproveitamento = int(
                (acertos / total) * 100
            )
        else:
            aproveitamento = 0

        texto = (
            f"NÍVEL ATUAL: {nivel}\n\n"
            f"PONTOS: {pontos}\n\n"
            f"ACERTOS: {acertos}     "
            f"ERROS: {erros}\n\n"
            f"SEQUÊNCIA: {sequencia}\n"
            f"MELHOR SEQUÊNCIA: {melhor}\n\n"
            f"APROVEITAMENTO: "
            f"{aproveitamento}%"
        )

        estatisticas = Label(
            text=texto,
            font_size="17sp",
            bold=True,
            color=(0.15, 0.15, 0.15, 1),
            halign="center",
            valign="middle",
            size_hint=(0.90, None),
            height=dp(210),
            pos_hint={
                "center_x": 0.5,
                "top": 0.82
            }
        )

        estatisticas.bind(
            size=lambda instance, value:
            setattr(
                instance,
                "text_size",
                value
            )
        )

        self.painel.add_widget(
            estatisticas
        )

        palavras = getattr(
            jogo,
            "palavras_revisao",
            []
        )

        if palavras:

            texto_revisao = (
                "PALAVRAS PARA TREINAR\n\n"
                +
                "   ".join(
                    palavra.upper()
                    for palavra in palavras[:6]
                )
            )

        else:

            texto_revisao = (
                "PALAVRAS PARA TREINAR\n\n"
                "Nenhuma palavra no momento!"
            )

        revisao = Label(
            text=texto_revisao,
            font_size="15sp",
            bold=True,
            color=(0.15, 0.40, 0.25, 1),
            halign="center",
            valign="middle",
            size_hint=(0.88, None),
            height=dp(110),
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.40
            }
        )

        revisao.bind(
            size=lambda instance, value:
            setattr(
                instance,
                "text_size",
                value
            )
        )

        self.painel.add_widget(
            revisao
        )

        if aproveitamento >= 90:

            mensagem = (
                "EXCELENTE!\n"
                "VOCÊ ESTÁ VOANDO!"
            )

        elif aproveitamento >= 70:

            mensagem = (
                "MUITO BEM!\n"
                "CONTINUE ASSIM!"
            )

        elif aproveitamento >= 50:

            mensagem = (
                "VOCÊ ESTÁ APRENDENDO!\n"
                "CONTINUE TENTANDO!"
            )

        else:

            mensagem = (
                "NÃO DESISTA!\n"
                "VAMOS CONTINUAR!"
            )

        mensagem_label = Label(
            text=mensagem,
            font_size="17sp",
            bold=True,
            color=(0.10, 0.35, 0.70, 1),
            halign="center",
            valign="middle",
            size_hint=(0.90, None),
            height=dp(65),
            pos_hint={
                "center_x": 0.5,
                "center_y": 0.25
            }
        )

        mensagem_label.bind(
            size=lambda instance, value:
            setattr(
                instance,
                "text_size",
                value
            )
        )

        self.painel.add_widget(
            mensagem_label
        )

        botao_voltar = BotaoBonito(
            "VOLTAR AO JOGO",
            cor=(0.25, 0.55, 0.90, 0.95),
            largura=220,
            altura=52,
            fonte=17,
            pos_hint={
                "center_x": 0.5,
                "y": 0.06
            }
        )

        botao_voltar.bind(
            on_press=self.voltar
        )

        self.painel.add_widget(
            botao_voltar
        )

    def atualizar_painel(
        self,
        *args
    ):

        self.painel_fundo.pos = (
            self.painel.pos
        )

        self.painel_fundo.size = (
            self.painel.size
        )

    def voltar(
        self,
        instance
    ):

        self.voltar_callback()


# ============================================================
# TELA DO JOGO
# ============================================================

class TelaJogo(FloatLayout):

    # ========================================================
    # CONSTANTES DA REGRA DAS VIDAS
    # ========================================================

    PALAVRAS_INICIAIS = 10
    PALAVRAS_MAXIMAS = 15

    VIDAS_INICIAIS = 3
    VIDAS_MAXIMAS = 10

    ERROS_PARA_AUMENTAR_NIVEL = 2

    def __init__(
        self,
        **kwargs
    ):

        super().__init__(**kwargs)

        self.em_correcao = False

        self.palavra_que_foi_errada = ""

        self.resposta_errada = ""

        self.nome_voz_atual = "Léo"

        self.janela_vozes = None

        # ----------------------------------------------------
        # CONTROLE DINÂMICO DO NÍVEL
        # ----------------------------------------------------

        self.palavras_do_nivel = self.PALAVRAS_INICIAIS

        self.vidas_do_nivel = self.VIDAS_INICIAIS

        self.erros_reais_nivel = 0

        self.acertos_reais_nivel = 0

        self.finalizando_nivel = False

        # ----------------------------------------------------
        # FUNDO
        # ----------------------------------------------------

        self.fundo = Image(
            source=FUNDO_JOGO,
            size_hint=(1, 1),
            pos_hint={
                "x": 0,
                "y": 0
            },
            allow_stretch=True,
            keep_ratio=False
        )

        self.add_widget(
            self.fundo
        )

        # ----------------------------------------------------
        # BALÕES
        # ----------------------------------------------------

        self.camada_baloes = CamadaBaloes(
            size_hint=(1, 1),
            pos_hint={
                "x": 0,
                "y": 0
            }
        )

        self.add_widget(
            self.camada_baloes
        )

        # ----------------------------------------------------
        # JOGO E VOZ
        # ----------------------------------------------------

        try:

            from jogo import JogoDitado
            from voz import Voz

        except ModuleNotFoundError as erro:

            print("==================================================")
            print(
                "ERRO: não foi possível encontrar jogo.py ou voz.py"
            )
            print("Pasta procurada:", BASE_DIR)
            print("Erro:", erro)
            print("==================================================")

            raise

        self.jogo = JogoDitado()

        self.voz = Voz()

        # ----------------------------------------------------
        # ÁREA CENTRAL
        # ----------------------------------------------------

        self.area_central = FloatLayout(
            size_hint=(0.38, 0.72),
            pos_hint={
                "center_x": 0.50,
                "center_y": 0.48
            }
        )

        self.add_widget(
            self.area_central
        )

        # ----------------------------------------------------
        # INFORMAÇÕES
        # ----------------------------------------------------

        self.informacoes = Label(
            text="",
            font_size="14sp",
            bold=True,
            color=(0.15, 0.15, 0.15, 1),
            size_hint=(1, None),
            height=dp(28),
            pos_hint={
                "center_x": 0.5,
                "top": 0.98
            }
        )

        self.area_central.add_widget(
            self.informacoes
        )

        # ----------------------------------------------------
        # VIDAS
        # ----------------------------------------------------

        self.vidas = Label(
            text="VIDAS: 3",
            font_size="18sp",
            bold=True,
            color=(0.25, 0.20, 0.20, 1),
            size_hint=(1, None),
            height=dp(30),
            pos_hint={
                "center_x": 0.5,
                "top": 0.90
            }
        )

        self.area_central.add_widget(
            self.vidas
        )

        # ----------------------------------------------------
        # VOZ
        # ----------------------------------------------------

        self.label_voz = Label(
            text="Voz: Léo",
            font_size="13sp",
            bold=True,
            color=(0.25, 0.25, 0.45, 1),
            size_hint=(1, None),
            height=dp(25),
            pos_hint={
                "center_x": 0.5,
                "top": 0.84
            }
        )

        self.area_central.add_widget(
            self.label_voz
        )

        # ----------------------------------------------------
        # INSTRUÇÃO
        # ----------------------------------------------------

        self.instrucao = Label(
            text=(
                "Clique em OUVIR e escreva\n"
                "a palavra que você escutar."
            ),
            font_size="14sp",
            color=(0.20, 0.20, 0.20, 1),
            halign="center",
            valign="middle",
            size_hint=(1, None),
            height=dp(48),
            pos_hint={
                "center_x": 0.5,
                "top": 0.77
            }
        )

        self.instrucao.bind(
            size=lambda instance, value:
            setattr(
                instance,
                "text_size",
                value
            )
        )

        self.area_central.add_widget(
            self.instrucao
        )

        # ----------------------------------------------------
        # OUVIR
        # ----------------------------------------------------

        self.botao_ouvir = BotaoBonito(
            "OUVIR PALAVRA",
            cor=(0.20, 0.62, 0.88, 0.95),
            largura=190,
            altura=52,
            fonte=17,
            pos_hint={
                "center_x": 0.5,
                "top": 0.66
            }
        )

        self.botao_ouvir.bind(
            on_press=self.ouvir_palavra
        )

        self.area_central.add_widget(
            self.botao_ouvir
        )

        # ----------------------------------------------------
        # RESPOSTA
        # ----------------------------------------------------

        self.resposta = TextInput(
            hint_text="Digite a palavra",
            font_size="19sp",
            multiline=False,
            halign="center",
            foreground_color=(
                0.12,
                0.12,
                0.12,
                1
            ),
            background_color=(
                0,
                0,
                0,
                0
            ),
            cursor_color=(
                0.10,
                0.35,
                0.70,
                1
            ),
            padding=(
                dp(10),
                dp(8)
            ),
            size_hint=(None, None),
            size=(
                dp(260),
                dp(48)
            ),
            pos_hint={
                "center_x": 0.5,
                "top": 0.55
            }
        )

        with self.resposta.canvas.before:

            Color(
                1,
                1,
                1,
                0.95
            )

            self.resposta_fundo = RoundedRectangle(
                pos=self.resposta.pos,
                size=self.resposta.size,
                radius=[dp(12)]
            )

            Color(
                0.30,
                0.55,
                0.80,
                0.80
            )

            self.resposta_borda = Line(
                rounded_rectangle=(
                    self.resposta.x,
                    self.resposta.y,
                    self.resposta.width,
                    self.resposta.height,
                    dp(12)
                ),
                width=1.3
            )

        self.resposta.bind(
            pos=self.atualizar_resposta_visual,
            size=self.atualizar_resposta_visual
        )

        self.area_central.add_widget(
            self.resposta
        )

        # ----------------------------------------------------
        # RESPONDER
        # ----------------------------------------------------

        self.botao_responder = BotaoBonito(
            "RESPONDER",
            cor=(0.30, 0.72, 0.42, 0.95),
            largura=190,
            altura=52,
            fonte=17,
            pos_hint={
                "center_x": 0.5,
                "top": 0.44
            }
        )

        self.botao_responder.bind(
            on_press=self.verificar
        )

        self.area_central.add_widget(
            self.botao_responder
        )

        # ----------------------------------------------------
        # CORREÇÃO
        # ----------------------------------------------------

        self.botao_repetir = BotaoBonito(
            "OUVIR CORREÇÃO",
            cor=(0.55, 0.50, 0.82, 0.95),
            largura=175,
            altura=40,
            fonte=14,
            pos_hint={
                "center_x": 0.5,
                "top": 0.34
            }
        )

        self.botao_repetir.bind(
            on_press=self.repetir_palavra
        )

        self.area_central.add_widget(
            self.botao_repetir
        )

        self.botao_repetir.opacity = 0
        self.botao_repetir.disabled = True

        # ----------------------------------------------------
        # RESULTADO
        # ----------------------------------------------------

        self.resultado = Label(
            text="",
            font_size="16sp",
            bold=True,
            color=(0.15, 0.15, 0.15, 1),
            halign="center",
            valign="middle",
            size_hint=(1, None),
            height=dp(55),
            pos_hint={
                "center_x": 0.5,
                "top": 0.32
            }
        )

        self.resultado.bind(
            size=lambda instance, value:
            setattr(
                instance,
                "text_size",
                value
            )
        )

        self.area_central.add_widget(
            self.resultado
        )

        # ----------------------------------------------------
        # PALAVRA CORRETA
        # ----------------------------------------------------

        self.palavra_correta_label = Label(
            text="",
            font_size="19sp",
            bold=True,
            color=(0.10, 0.55, 0.20, 1),
            halign="center",
            valign="middle",
            size_hint=(1, None),
            height=dp(60),
            pos_hint={
                "center_x": 0.5,
                "top": 0.22
            }
        )

        self.palavra_correta_label.bind(
            size=lambda instance, value:
            setattr(
                instance,
                "text_size",
                value
            )
        )

        self.area_central.add_widget(
            self.palavra_correta_label
        )

        # ----------------------------------------------------
        # BOTÕES INFERIORES
        # ----------------------------------------------------

        self.area_inferior = BoxLayout(
            orientation="horizontal",
            spacing=dp(18),
            size_hint=(None, None),
            size=(
                dp(328),
                dp(48)
            ),
            pos_hint={
                "center_x": 0.5,
                "y": 0.01
            }
        )

        self.area_central.add_widget(
            self.area_inferior
        )

        self.botao_voz = BotaoBonito(
            "ESCOLHER VOZ",
            cor=(0.70, 0.45, 0.78, 0.95),
            largura=155,
            altura=46,
            fonte=13
        )

        self.botao_voz.bind(
            on_press=self.mostrar_vozes
        )

        self.area_inferior.add_widget(
            self.botao_voz
        )

        self.botao_progresso = BotaoBonito(
            "MEU PROGRESSO",
            cor=(0.95, 0.62, 0.22, 0.95),
            largura=155,
            altura=46,
            fonte=13
        )

        self.botao_progresso.bind(
            on_press=self.abrir_progresso
        )

        self.area_inferior.add_widget(
            self.botao_progresso
        )

        # ----------------------------------------------------
        # PRÓXIMO NÍVEL
        # ----------------------------------------------------

        self.botao_proximo = BotaoBonito(
            "PRÓXIMO NÍVEL",
            cor=(0.95, 0.62, 0.12, 0.95),
            largura=200,
            altura=48,
            fonte=16,
            pos_hint={
                "center_x": 0.5,
                "y": 0.01
            }
        )

        self.botao_proximo.bind(
            on_press=self.proximo_nivel
        )

        self.add_widget(
            self.botao_proximo
        )

        self.botao_proximo.opacity = 0
        self.botao_proximo.disabled = True

        # ----------------------------------------------------
        # TENTAR NOVAMENTE
        # ----------------------------------------------------

        self.botao_tentar = BotaoBonito(
            "TENTAR NOVAMENTE",
            cor=(0.85, 0.35, 0.35, 0.95),
            largura=210,
            altura=48,
            fonte=16,
            pos_hint={
                "center_x": 0.5,
                "y": 0.01
            }
        )

        self.botao_tentar.bind(
            on_press=self.tentar_novamente
        )

        self.add_widget(
            self.botao_tentar
        )

        self.botao_tentar.opacity = 0
        self.botao_tentar.disabled = True

        # ----------------------------------------------------
        # PRIMEIRA PALAVRA
        # ----------------------------------------------------

        Clock.schedule_once(
            lambda dt: self.nova_palavra(),
            0.1
        )

    # ========================================================
    # PROTEÇÃO DE TOQUE
    # ========================================================

    def on_touch_down(self, touch):

        if (
            hasattr(self, "botao_proximo")
            and self.botao_proximo.opacity > 0
            and not self.botao_proximo.disabled
            and self.botao_proximo.collide_point(
                *touch.pos
            )
        ):

            print("======================================")
            print(">>> TOQUE DETECTADO EM PRÓXIMO NÍVEL")
            print(">>> BOTÃO ESTÁ HABILITADO")
            print(">>> DISPARANDO PROXIMO_NIVEL")
            print("======================================")

            self.botao_proximo.dispatch(
                "on_press"
            )

            return True

        if (
            hasattr(self, "botao_tentar")
            and self.botao_tentar.opacity > 0
            and not self.botao_tentar.disabled
            and self.botao_tentar.collide_point(
                *touch.pos
            )
        ):

            print("======================================")
            print(">>> TOQUE DETECTADO EM TENTAR NOVAMENTE")
            print(">>> DISPARANDO TENTAR_NOVAMENTE")
            print("======================================")

            self.botao_tentar.dispatch(
                "on_press"
            )

            return True

        return super().on_touch_down(touch)

    # ========================================================
    # CAMPO
    # ========================================================

    def atualizar_resposta_visual(
        self,
        *args
    ):

        self.resposta_fundo.pos = (
            self.resposta.pos
        )

        self.resposta_fundo.size = (
            self.resposta.size
        )

        self.resposta_borda.rounded_rectangle = (
            self.resposta.x,
            self.resposta.y,
            self.resposta.width,
            self.resposta.height,
            dp(12)
        )

    # ========================================================
    # FOCO
    # ========================================================

    def focar_resposta(self):

        if not self.resposta.disabled:
            self.resposta.focus = True

    # ========================================================
    # NOVA PALAVRA
    # ========================================================

    def nova_palavra(self):

        self.em_correcao = False
        self.finalizando_nivel = False

        self.botao_ouvir.opacity = 1
        self.botao_responder.opacity = 1
        self.botao_progresso.opacity = 1
        self.botao_voz.opacity = 1

        self.botao_ouvir.disabled = False
        self.botao_responder.disabled = False
        self.botao_progresso.disabled = False
        self.botao_voz.disabled = False

        self.resposta.disabled = False

        self.botao_repetir.opacity = 0
        self.botao_repetir.disabled = True

        self.botao_proximo.opacity = 0
        self.botao_proximo.disabled = True

        self.botao_tentar.opacity = 0
        self.botao_tentar.disabled = True

        self.resposta.text = ""

        self.resultado.text = ""

        self.palavra_correta_label.text = ""

        self.instrucao.text = (
            "Clique em OUVIR e escreva\n"
            "a palavra que você escutar."
        )

        try:

            self.jogo.nova_palavra()

        except Exception as erro:

            print(
                "ERRO AO CRIAR NOVA PALAVRA:",
                erro
            )

            self.resultado.text = (
                "ERRO AO CARREGAR PALAVRA"
            )

            return

        self.atualizar_informacoes()

        Clock.schedule_once(
            lambda dt: self.focar_resposta(),
            0.2
        )

    # ========================================================
    # OUVIR
    # ========================================================

    def ouvir_palavra(
        self,
        instance
    ):

        if self.em_correcao:
            return

        palavra = self.jogo.palavra_atual

        if not palavra:
            return

        try:

            self.voz.falar(
                palavra
            )

        except Exception as erro:

            print(
                "ERRO AO FALAR:",
                erro
            )

        self.instrucao.text = (
            "Escute com atenção e escreva\n"
            "a palavra!"
        )

    # ========================================================
    # REPETIR CORREÇÃO
    # ========================================================

    def repetir_palavra(
        self,
        instance
    ):

        if self.palavra_que_foi_errada:

            try:

                self.voz.falar(
                    self.palavra_que_foi_errada
                )

            except Exception as erro:

                print(
                    "ERRO AO REPETIR:",
                    erro
                )

    # ========================================================
    # VERIFICAR
    # ========================================================

    def verificar(
        self,
        instance
    ):

        resposta = (
            self.resposta.text
            .strip()
            .lower()
        )

        if not resposta:

            self.resultado.text = (
                "DIGITE UMA PALAVRA!"
            )

            self.focar_resposta()

            return

        # ----------------------------------------------------
        # MODO CORREÇÃO
        #
        # MUITO IMPORTANTE:
        #
        # Nenhum erro aqui é considerado erro real.
        # Não perde vida.
        # Não aumenta contador.
        # ----------------------------------------------------

        if self.em_correcao:

            self.verificar_correcao(
                resposta
            )

            return

        palavra_correta = (
            self.jogo.palavra_atual
        )

        acertou, terminou_jogo = (
            self.jogo.verificar_resposta(
                resposta
            )
        )

        # ----------------------------------------------------
        # ACERTO REAL
        # ----------------------------------------------------

        if acertou:

            self.acertos_reais_nivel += 1

            self.palavra_correta_label.text = ""

            self.resultado.text = (
                "MUITO BEM!\n"
                "VOCÊ ACERTOU!"
            )

            self.animar_baloes()

            self.animar_acerto()

            self.instrucao.text = (
                "Parabéns! Você está aprendendo!"
            )

            self.atualizar_informacoes()

            self.botao_ouvir.disabled = True
            self.botao_responder.disabled = True
            self.resposta.disabled = True

            # ------------------------------------------------
            # NÃO USAMOS MAIS O TERMINOU_JOGO DO jogo.py
            #
            # O tamanho do nível agora é controlado por:
            # self.palavras_do_nivel
            # ------------------------------------------------

            if (
                self.acertos_reais_nivel
                >= self.palavras_do_nivel
            ):

                Clock.schedule_once(
                    lambda dt:
                    self.mostrar_resultado(),
                    2.5
                )

            else:

                Clock.schedule_once(
                    lambda dt:
                    self.nova_palavra(),
                    2.5
                )

            return

        # ----------------------------------------------------
        # ERRO REAL DO DITADO
        # ----------------------------------------------------

        self.registrar_erro_real()

        self.palavra_que_foi_errada = (
            palavra_correta
        )

        self.resposta_errada = (
            resposta
        )

        self.animar_erro()

        self.iniciar_correcao()

    # ========================================================
    # REGISTRAR ERRO REAL
    # ========================================================

    def registrar_erro_real(self):

        # +1 erro real
        self.erros_reais_nivel += 1

        # Atualiza contador geral do jogo somente aqui.
        #
        # O método verificar_resposta() já fez isso.
        # Portanto não alteramos jogo.erros novamente.
        #
        # Aqui controlamos especificamente as regras
        # adicionais de vidas e tamanho do nível.

        # ----------------------------------------------------
        # PERDE 1 VIDA
        # ----------------------------------------------------

        self.vidas_do_nivel = max(
            0,
            self.vidas_do_nivel - 1
        )

        # Mantém o valor visual sincronizado
        self.jogo.vidas = self.vidas_do_nivel

        # ----------------------------------------------------
        # A CADA 2 ERROS REAIS:
        #
        # +1 palavra
        # +1 vida
        # ----------------------------------------------------

        if (
            self.erros_reais_nivel
            % self.ERROS_PARA_AUMENTAR_NIVEL
            == 0
        ):

            if (
                self.palavras_do_nivel
                < self.PALAVRAS_MAXIMAS
            ):

                self.palavras_do_nivel += 1

                print(
                    ">>> +1 PALAVRA NO NÍVEL"
                )

            else:

                print(
                    ">>> LIMITE DE 15 PALAVRAS ATINGIDO"
                )

            if (
                self.vidas_do_nivel
                < self.VIDAS_MAXIMAS
            ):

                self.vidas_do_nivel += 1

                print(
                    ">>> +1 VIDA"
                )

            else:

                print(
                    ">>> LIMITE DE 10 VIDAS ATINGIDO"
                )

            self.jogo.vidas = (
                self.vidas_do_nivel
            )

        print("======================================")
        print(">>> ERRO REAL")
        print(
            ">>> Erros reais:",
            self.erros_reais_nivel
        )
        print(
            ">>> Palavras do nível:",
            self.palavras_do_nivel
        )
        print(
            ">>> Vidas:",
            self.vidas_do_nivel
        )
        print("======================================")

        self.atualizar_informacoes()

    # ========================================================
    # BALÕES
    # ========================================================

    def animar_baloes(self):

        self.camada_baloes.comemorar()

    # ========================================================
    # INICIAR CORREÇÃO
    # ========================================================

    def iniciar_correcao(self):

        self.em_correcao = True

        palavra = (
            self.palavra_que_foi_errada
        )

        digitado = (
            self.resposta_errada
        )

        self.resultado.text = (
            "QUASE!\n"
            f"Você escreveu: "
            f"{digitado.upper()}"
        )

        self.palavra_correta_label.text = (
            "O CORRETO É:\n"
            f"{palavra.upper()}"
        )

        self.instrucao.text = (
            "Observe a palavra correta e\n"
            "tente escrever novamente."
        )

        # ----------------------------------------------------
        # FICA PRESA NA PALAVRA
        # ----------------------------------------------------

        self.botao_ouvir.disabled = True
        self.botao_progresso.disabled = True
        self.botao_voz.disabled = True

        self.botao_responder.disabled = False
        self.resposta.disabled = False

        self.botao_repetir.opacity = 1
        self.botao_repetir.disabled = False

        self.resposta.text = ""

        Clock.schedule_once(
            lambda dt:
            self.falar_correcao(),
            0.8
        )

        Clock.schedule_once(
            lambda dt:
            self.focar_resposta(),
            1.2
        )

    # ========================================================
    # FALAR CORREÇÃO
    # ========================================================

    def falar_correcao(self):

        if self.palavra_que_foi_errada:

            try:

                self.voz.falar(
                    self.palavra_que_foi_errada
                )

            except Exception as erro:

                print(
                    "ERRO AO FALAR CORREÇÃO:",
                    erro
                )

    # ========================================================
    # VERIFICAR CORREÇÃO
    # ========================================================

    def verificar_correcao(
        self,
        resposta
    ):

        correta = (
            self.palavra_que_foi_errada
            .strip()
            .lower()
        )

        # ----------------------------------------------------
        # ACERTO DA CORREÇÃO
        # ----------------------------------------------------

        if resposta == correta:

            self.animar_baloes()

            self.animar_acerto()

            self.resultado.text = (
                "MUITO BEM!\n"
                "AGORA VOCÊ ACERTOU!"
            )

            self.palavra_correta_label.text = (
                correta.upper()
            )

            self.em_correcao = False

            self.botao_repetir.opacity = 0
            self.botao_repetir.disabled = True

            self.botao_progresso.disabled = False
            self.botao_voz.disabled = False

            self.botao_responder.disabled = True
            self.resposta.disabled = True

            self.resposta.text = ""

            self.instrucao.text = (
                "Excelente!\n"
                "Vamos para a próxima palavra."
            )

            # ------------------------------------------------
            # A CORREÇÃO NÃO CONTA COMO NOVO ACERTO
            #
            # Ela apenas libera a criança para avançar.
            # ------------------------------------------------

            if (
                self.acertos_reais_nivel
                >= self.palavras_do_nivel
            ):

                Clock.schedule_once(
                    lambda dt:
                    self.mostrar_resultado(),
                    2.5
                )

            else:

                Clock.schedule_once(
                    lambda dt:
                    self.nova_palavra(),
                    2.5
                )

        # ----------------------------------------------------
        # ERRO DURANTE A CORREÇÃO
        #
        # NÃO PERDE VIDA
        # NÃO AUMENTA ERROS
        # NÃO AVANÇA
        # ----------------------------------------------------

        else:

            self.animar_erro()

            self.resultado.text = (
                "AINDA NÃO!\n"
                f"Você escreveu: "
                f"{resposta.upper()}"
            )

            self.palavra_correta_label.text = (
                "O CORRETO É:\n"
                f"{correta.upper()}"
            )

            self.resposta.text = ""

            Clock.schedule_once(
                lambda dt:
                self.voz.falar(correta),
                0.5
            )

            Clock.schedule_once(
                lambda dt:
                self.focar_resposta(),
                1
            )

    # ========================================================
    # ANIMAÇÃO ACERTO
    # ========================================================

    def animar_acerto(self):

        animacao = (
            Animation(
                font_size=25,
                duration=0.15
            )
            +
            Animation(
                font_size=18,
                duration=0.15
            )
            +
            Animation(
                font_size=25,
                duration=0.15
            )
        )

        animacao.start(
            self.resultado
        )

        Clock.schedule_once(
            lambda dt:
            self.falar_comemoracao(),
            0.3
        )

    # ========================================================
    # COMEMORAÇÃO
    # ========================================================

    def falar_comemoracao(self):

        frases = [
            "Muito bem!",
            "Você acertou!",
            "Parabéns!",
            "Excelente!",
            "Isso aí!"
        ]

        try:

            self.voz.falar(
                random.choice(frases)
            )

        except Exception as erro:

            print(
                "Erro na comemoração:",
                erro
            )

    # ========================================================
    # ANIMAÇÃO ERRO
    # ========================================================

    def animar_erro(self):

        x_original = self.resposta.x

        animacao = (
            Animation(
                x=x_original - dp(8),
                duration=0.07
            )
            +
            Animation(
                x=x_original + dp(8),
                duration=0.07
            )
            +
            Animation(
                x=x_original - dp(6),
                duration=0.07
            )
            +
            Animation(
                x=x_original + dp(6),
                duration=0.07
            )
            +
            Animation(
                x=x_original,
                duration=0.07
            )
        )

        animacao.start(
            self.resposta
        )

    # ========================================================
    # RESULTADO DO NÍVEL
    # ========================================================

    def mostrar_resultado(self):

        if self.finalizando_nivel:
            return

        self.finalizando_nivel = True

        self.botao_ouvir.disabled = True
        self.botao_responder.disabled = True
        self.resposta.disabled = True
        self.botao_progresso.disabled = True
        self.botao_voz.disabled = True

        self.botao_repetir.opacity = 0
        self.botao_repetir.disabled = True

        self.palavra_correta_label.text = ""

        acertos = self.acertos_reais_nivel
        erros = self.erros_reais_nivel

        total = (
            acertos +
            erros
        )

        print("======================================")
        print(">>> NÍVEL TERMINADO")
        print(">>> PALAVRAS DO NÍVEL:", self.palavras_do_nivel)
        print(">>> ACERTOS:", acertos)
        print(">>> ERROS REAIS:", erros)
        print(">>> VIDAS RESTANTES:", self.vidas_do_nivel)
        print("======================================")

        # ----------------------------------------------------
        # REGRA DE APROVAÇÃO
        #
        # Mantemos a regra anterior de 70%.
        # ----------------------------------------------------

        percentual = 0

        if total > 0:

            percentual = (
                acertos /
                total
            ) * 100

        if percentual >= 70:

            self.resultado.text = (
                "PARABÉNS!\n\n"
                f"Você acertou {acertos} "
                f"de {self.palavras_do_nivel}!\n"
                f"Errou {erros} palavras.\n\n"
                "VOCÊ PASSOU DE NÍVEL!"
            )

            self.botao_proximo.disabled = False
            self.botao_proximo.opacity = 1

            print(
                ">>> BOTÃO PRÓXIMO NÍVEL LIBERADO"
            )

            self.animar_nivel_concluido()

        else:

            self.resultado.text = (
                "MUITO BEM POR TENTAR!\n\n"
                f"Você acertou {acertos} "
                f"de {self.palavras_do_nivel}.\n"
                f"Errou {erros} palavras.\n\n"
                "Vamos tentar novamente!"
            )

            self.botao_tentar.opacity = 1
            self.botao_tentar.disabled = False

    # ========================================================
    # ANIMAÇÃO NÍVEL CONCLUÍDO
    # ========================================================

    def animar_nivel_concluido(self):

        animacao = (
            Animation(
                font_size=28,
                duration=0.20
            )
            +
            Animation(
                font_size=20,
                duration=0.20
            )
            +
            Animation(
                font_size=28,
                duration=0.20
            )
        )

        animacao.start(
            self.resultado
        )

        Clock.schedule_once(
            lambda dt:
            self.voz.falar(
                "Parabéns! Você passou de nível!"
            ),
            0.5
        )

    # ========================================================
    # PRÓXIMO NÍVEL
    # ========================================================

    def proximo_nivel(
        self,
        instance=None
    ):

        print("======================================")
        print(">>> PROXIMO_NIVEL FOI EXECUTADO")
        print(">>> NÍVEL ANTES:", self.jogo.nivel)
        print("======================================")

        self.botao_proximo.disabled = True
        self.botao_proximo.opacity = 0

        try:

            self.jogo.passar_de_nivel()

            print(
                ">>> NOVO NÍVEL:",
                self.jogo.nivel
            )

        except Exception as erro:

            print(
                ">>> ERRO AO PASSAR DE NÍVEL:",
                erro
            )

            self.botao_proximo.disabled = False
            self.botao_proximo.opacity = 1

            return

        # ----------------------------------------------------
        # NOVO NÍVEL COMEÇA COM A CONFIGURAÇÃO PADRÃO
        # ----------------------------------------------------

        self.palavras_do_nivel = (
            self.PALAVRAS_INICIAIS
        )

        self.vidas_do_nivel = (
            self.VIDAS_INICIAIS
        )

        self.erros_reais_nivel = 0

        self.acertos_reais_nivel = 0

        self.jogo.vidas = (
            self.vidas_do_nivel
        )

        self.em_correcao = False

        self.finalizando_nivel = False

        self.palavra_que_foi_errada = ""
        self.resposta_errada = ""

        self.resposta.text = ""

        self.resultado.text = ""

        self.palavra_correta_label.text = ""

        self.instrucao.text = (
            "Clique em OUVIR e escreva\n"
            "a palavra que você escutar."
        )

        # ----------------------------------------------------
        # REATIVA CONTROLES
        # ----------------------------------------------------

        self.botao_ouvir.disabled = False
        self.botao_responder.disabled = False
        self.botao_progresso.disabled = False
        self.botao_voz.disabled = False
        self.resposta.disabled = False

        self.botao_ouvir.opacity = 1
        self.botao_responder.opacity = 1
        self.botao_progresso.opacity = 1
        self.botao_voz.opacity = 1

        self.botao_repetir.opacity = 0
        self.botao_repetir.disabled = True

        self.botao_tentar.opacity = 0
        self.botao_tentar.disabled = True

        self.atualizar_informacoes()

        Clock.schedule_once(
            lambda dt:
            self.nova_palavra(),
            0.15
        )

    # ========================================================
    # TENTAR NOVAMENTE
    # ========================================================

    def tentar_novamente(
        self,
        instance=None
    ):

        print("======================================")
        print(">>> TENTAR NOVAMENTE EXECUTADO")
        print("======================================")

        self.botao_tentar.disabled = True
        self.botao_tentar.opacity = 0

        self.botao_proximo.disabled = True
        self.botao_proximo.opacity = 0

        self.botao_ouvir.disabled = False
        self.botao_responder.disabled = False
        self.botao_progresso.disabled = False
        self.botao_voz.disabled = False
        self.resposta.disabled = False

        self.botao_ouvir.opacity = 1
        self.botao_responder.opacity = 1
        self.botao_progresso.opacity = 1
        self.botao_voz.opacity = 1

        self.em_correcao = False

        self.finalizando_nivel = False

        # ----------------------------------------------------
        # RECOMEÇA A CONFIGURAÇÃO DO NÍVEL
        # ----------------------------------------------------

        self.palavras_do_nivel = (
            self.PALAVRAS_INICIAIS
        )

        self.vidas_do_nivel = (
            self.VIDAS_INICIAIS
        )

        self.erros_reais_nivel = 0

        self.acertos_reais_nivel = 0

        try:

            self.jogo.reiniciar_nivel()

        except Exception as erro:

            print(
                "ERRO AO REINICIAR NÍVEL:",
                erro
            )

            self.resultado.text = (
                "ERRO AO REINICIAR NÍVEL"
            )

            return

        self.jogo.vidas = (
            self.vidas_do_nivel
        )

        self.resultado.text = (
            "VAMOS TENTAR NOVAMENTE!"
        )

        self.palavra_correta_label.text = ""

        self.resposta.text = ""

        self.atualizar_informacoes()

        Clock.schedule_once(
            lambda dt:
            self.nova_palavra(),
            1.0
        )

    # ========================================================
    # INFORMAÇÕES
    # ========================================================

    def atualizar_informacoes(self):

        pergunta = (
            self.acertos_reais_nivel + 1
        )

        if pergunta > self.palavras_do_nivel:
            pergunta = self.palavras_do_nivel

        self.informacoes.text = (
            f"Nível: {self.jogo.nivel}    "
            f"Pergunta: {pergunta}/"
            f"{self.palavras_do_nivel}    "
            f"Pontos: {self.jogo.pontos}    "
            f"Acertos: {self.jogo.acertos}"
        )

        vidas = self.vidas_do_nivel

        if vidas < 0:
            vidas = 0

        if vidas > self.VIDAS_MAXIMAS:
            vidas = self.VIDAS_MAXIMAS

        self.vidas.text = (
            f"VIDAS: {vidas}"
        )

    # ========================================================
    # PROGRESSO
    # ========================================================

    def abrir_progresso(
        self,
        instance
    ):

        if self.em_correcao:
            return

        app = App.get_running_app()

        app.mostrar_progresso(
            self.jogo
        )

    # ========================================================
    # ESCOLHER VOZ
    # ========================================================

    def mostrar_vozes(
        self,
        instance
    ):

        if self.janela_vozes is not None:
            return

        self.janela_vozes = ModalView(
            size_hint=(0.38, 0.62),
            auto_dismiss=True,
            background_color=(
                0,
                0,
                0,
                0.45
            )
        )

        painel = BoxLayout(
            orientation="vertical",
            padding=dp(20),
            spacing=dp(12)
        )

        with painel.canvas.before:

            Color(
                1,
                1,
                1,
                0.98
            )

            painel.fundo = RoundedRectangle(
                pos=painel.pos,
                size=painel.size,
                radius=[dp(20)]
            )

        painel.bind(
            pos=lambda instance, value:
            setattr(
                painel.fundo,
                "pos",
                value
            ),
            size=lambda instance, value:
            setattr(
                painel.fundo,
                "size",
                value
            )
        )

        titulo = Label(
            text="ESCOLHA UMA VOZ",
            font_size="22sp",
            bold=True,
            color=(0.10, 0.20, 0.50, 1),
            size_hint_y=None,
            height=dp(50)
        )

        painel.add_widget(
            titulo
        )

        botao_leo = BotaoBonito(
            "LÉO\nVoz masculina",
            cor=(0.25, 0.55, 0.90, 1),
            largura=220,
            altura=62,
            fonte=16
        )

        botao_leo.pos_hint = {
            "center_x": 0.5
        }

        botao_leo.bind(
            on_press=lambda instance:
            self.selecionar_voz(
                "leo",
                "Léo"
            )
        )

        painel.add_widget(
            botao_leo
        )

        botao_lia = BotaoBonito(
            "LIA\nVoz feminina",
            cor=(0.85, 0.45, 0.65, 1),
            largura=220,
            altura=62,
            fonte=16
        )

        botao_lia.pos_hint = {
            "center_x": 0.5
        }

        botao_lia.bind(
            on_press=lambda instance:
            self.selecionar_voz(
                "lia",
                "Lia"
            )
        )

        painel.add_widget(
            botao_lia
        )

        botao_tico = BotaoBonito(
            "TICO\nVoz divertida",
            cor=(0.65, 0.45, 0.85, 1),
            largura=220,
            altura=62,
            fonte=16
        )

        botao_tico.pos_hint = {
            "center_x": 0.5
        }

        botao_tico.bind(
            on_press=lambda instance:
            self.selecionar_voz(
                "tico",
                "Tico"
            )
        )

        painel.add_widget(
            botao_tico
        )

        fechar = BotaoBonito(
            "FECHAR",
            cor=(0.45, 0.45, 0.45, 1),
            largura=150,
            altura=42,
            fonte=14
        )

        fechar.pos_hint = {
            "center_x": 0.5
        }

        fechar.bind(
            on_press=self.fechar_vozes
        )

        painel.add_widget(
            fechar
        )

        self.janela_vozes.add_widget(
            painel
        )

        self.janela_vozes.open()

    # ========================================================
    # SELECIONAR VOZ
    # ========================================================

    def selecionar_voz(
        self,
        codigo,
        nome
    ):

        try:

            sucesso = self.voz.escolher_voz(
                codigo
            )

        except Exception as erro:

            print(
                "ERRO AO ESCOLHER VOZ:",
                erro
            )

            sucesso = False

        if sucesso:

            self.nome_voz_atual = nome

            self.label_voz.text = (
                f"Voz: {nome}"
            )

            self.resultado.text = (
                f"Voz {nome} selecionada!"
            )

            Clock.schedule_once(
                lambda dt:
                self.voz.falar(
                    f"Olá! Eu sou {nome}!"
                ),
                0.3
            )

        self.fechar_vozes()

    # ========================================================
    # FECHAR VOZES
    # ========================================================

    def fechar_vozes(
        self,
        instance=None
    ):

        if self.janela_vozes is not None:

            self.janela_vozes.dismiss()

            self.janela_vozes = None


# ============================================================
# APLICAÇÃO
# ============================================================

class DitadoGameApp(App):

    def build(self):

        self.title = "Ditado da Maria"

        self.container = FloatLayout()

        self.tela_jogo = TelaJogo()

        self.container.add_widget(
            self.tela_jogo
        )

        return self.container

    # ========================================================
    # MOSTRAR JOGO
    # ========================================================

    def mostrar_jogo(self):

        self.container.clear_widgets()

        self.container.add_widget(
            self.tela_jogo
        )

    # ========================================================
    # MOSTRAR PROGRESSO
    # ========================================================

    def mostrar_progresso(
        self,
        jogo
    ):

        self.container.clear_widgets()

        self.tela_progresso = TelaProgresso(
            jogo,
            self.mostrar_jogo
        )

        self.container.add_widget(
            self.tela_progresso
        )


# ============================================================
# INICIAR
# ============================================================

if __name__ == "__main__":

    print("==========================================")
    print("      DITADO DA MARIA - INICIANDO")
    print("==========================================")
    print("Pasta do programa:", BASE_DIR)
    print("Fundo:", FUNDO_JOGO)

    print(
        "jogo.py encontrado:",
        os.path.isfile(
            caminho_arquivo("jogo.py")
        )
    )

    print(
        "voz.py encontrado:",
        os.path.isfile(
            caminho_arquivo("voz.py")
        )
    )

    print("==========================================")

    DitadoGameApp().run()