# -*- coding: utf-8 -*-

import asyncio
import os
import tempfile
import threading

import edge_tts
from kivy.core.audio import SoundLoader


# ============================================================
# CONFIGURAÇÃO DAS VOZES
# ============================================================

VOZES = {

    "leo": {
        "nome": "Léo",
        "voz": "pt-BR-AntonioNeural",
        "rate": "+0%",
        "pitch": "+0Hz",
        "volume": "+0%",
    },

    "lia": {
        "nome": "Lia",
        "voz": "pt-BR-ThalitaNeural",
        "rate": "+0%",
        "pitch": "+0Hz",
        "volume": "+0%",
    },

    "tico": {
        "nome": "Tico",
        "voz": "pt-BR-AntonioNeural",
        "rate": "+18%",
        "pitch": "+35Hz",
        "volume": "+0%",
    },
}


# ============================================================
# CLASSE VOZ
# ============================================================

class Voz:

    def __init__(self):

        # Voz inicial
        self.personagem = "leo"

        # Arquivo temporário atual
        self.arquivo_audio = None

        # Controle para evitar várias falas simultâneas
        self.falando = False


    # ========================================================
    # ESCOLHER VOZ
    # ========================================================

    def escolher_voz(self, personagem):

        personagem = personagem.lower().strip()

        if personagem not in VOZES:

            print(
                f"Voz '{personagem}' não encontrada."
            )

            return False

        self.personagem = personagem

        print(
            f"Voz selecionada: "
            f"{VOZES[personagem]['nome']}"
        )

        return True


    # ========================================================
    # VOZ ATUAL
    # ========================================================

    def obter_voz(self):

        return VOZES[
            self.personagem
        ]


    # ========================================================
    # FALAR
    # ========================================================

    def falar(self, texto):

        if texto is None:

            return

        texto = str(texto).strip()

        if not texto:

            return

        # -----------------------------------------------
        # Executar em outra thread para não travar o Kivy
        # -----------------------------------------------

        thread = threading.Thread(
            target=self._gerar_e_reproduzir,
            args=(texto,),
            daemon=True
        )

        thread.start()


    # ========================================================
    # GERAR E REPRODUZIR
    # ========================================================

    def _gerar_e_reproduzir(self, texto):

        try:

            self.falando = True

            configuracao = self.obter_voz()

            # -----------------------------------------------
            # Criar arquivo temporário
            # -----------------------------------------------

            arquivo = tempfile.NamedTemporaryFile(
                suffix=".mp3",
                delete=False
            )

            caminho = arquivo.name

            arquivo.close()

            self.arquivo_audio = caminho

            # -----------------------------------------------
            # Gerar áudio
            # -----------------------------------------------

            asyncio.run(
                self._gerar_audio(
                    texto,
                    caminho,
                    configuracao
                )
            )

            # -----------------------------------------------
            # Reproduzir
            # -----------------------------------------------

            sound = SoundLoader.load(
                caminho
            )

            if sound:

                sound.play()

                # Guardar referência
                self.sound = sound

                # -------------------------------------------
                # Aguardar terminar
                # -------------------------------------------

                duracao = sound.length or 1

                threading.Event().wait(
                    duracao + 0.2
                )

                sound.stop()

            else:

                print(
                    "ERRO: Não foi possível "
                    "carregar o áudio."
                )


        except Exception as erro:

            print(
                "ERRO NA VOZ:"
            )

            print(
                erro
            )


        finally:

            self.falando = False

            # -----------------------------------------------
            # Remover arquivo temporário
            # -----------------------------------------------

            try:

                if (
                    self.arquivo_audio
                    and
                    os.path.exists(
                        self.arquivo_audio
                    )
                ):

                    os.remove(
                        self.arquivo_audio
                    )

            except Exception:

                pass


    # ========================================================
    # GERAR ÁUDIO COM EDGE TTS
    # ========================================================

    async def _gerar_audio(
        self,
        texto,
        caminho,
        configuracao
    ):

        comunicador = edge_tts.Communicate(

            texto,

            configuracao["voz"],

            rate=configuracao["rate"],

            volume=configuracao["volume"],

            pitch=configuracao["pitch"]

        )

        await comunicador.save(
            caminho
        )


# ============================================================
# TESTE
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 50)
    print("TESTE DAS VOZES")
    print("=" * 50)
    print()

    voz = Voz()

    # --------------------------------------------------------
    # LÉO
    # --------------------------------------------------------

    print("Testando Léo...")

    voz.escolher_voz(
        "leo"
    )

    voz.falar(
        "Olá! Eu sou o Léo!"
    )

    threading.Event().wait(4)

    # --------------------------------------------------------
    # LIA
    # --------------------------------------------------------

    print("Testando Lia...")

    voz.escolher_voz(
        "lia"
    )

    voz.falar(
        "Olá! Eu sou a Lia!"
    )

    threading.Event().wait(4)

    # --------------------------------------------------------
    # TICO
    # --------------------------------------------------------

    print("Testando Tico...")

    voz.escolher_voz(
        "tico"
    )

    voz.falar(
        "Oi! Eu sou o Tico! Vamos brincar de ditado!"
    )

    threading.Event().wait(5)

    print()
    print("=" * 50)
    print("TESTE FINALIZADO")
    print("=" * 50)