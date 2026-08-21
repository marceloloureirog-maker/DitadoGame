import random
import json
import os
import unicodedata
from vidas import ControleVidas

from palavras import PALAVRAS


# ============================================================
# CONFIGURAÇÕES
# ============================================================

ARQUIVO_PROGRESSO = "progresso.json"

PALAVRAS_POR_NIVEL = 10

VIDAS_INICIAIS = 5

DOMINIO_APRENDENDO = 2

DOMINIO_APRENDIDA = 4


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def remover_acentos(texto):
    texto = unicodedata.normalize("NFD", texto)

    texto = "".join(
        caractere
        for caractere in texto
        if unicodedata.category(caractere) != "Mn"
    )

    return texto


def normalizar_palavra(texto):
    if texto is None:
        return ""

    texto = str(texto)
    texto = texto.strip().lower()
    texto = remover_acentos(texto)

    return texto


# ============================================================
# DIFICULDADE
# ============================================================

def calcular_dificuldade(palavra):

    palavra_original = palavra.lower()
    palavra = normalizar_palavra(palavra_original)

    pontos = 0

    # Tamanho
    tamanho = len(palavra)

    if tamanho <= 4:
        pontos += 0
    elif tamanho <= 6:
        pontos += 1
    elif tamanho <= 8:
        pontos += 2
    elif tamanho <= 10:
        pontos += 3
    else:
        pontos += 4

    # Grupos de vogais
    vogais = "aeiou"

    grupos_vogais = 0
    estava_em_vogal = False

    for letra in palavra:

        if letra in vogais:

            if not estava_em_vogal:
                grupos_vogais += 1

            estava_em_vogal = True

        else:

            estava_em_vogal = False

    if grupos_vogais <= 1:
        pontos += 0
    elif grupos_vogais == 2:
        pontos += 1
    elif grupos_vogais == 3:
        pontos += 2
    elif grupos_vogais == 4:
        pontos += 3
    else:
        pontos += 4

    # Dígrafos
    digrafos = [
        "ch",
        "lh",
        "nh",
        "rr",
        "ss",
        "qu",
        "gu"
    ]

    for digrafo in digrafos:
        pontos += palavra.count(digrafo)

    # Encontros consonantais
    encontros = [
        "br", "cr", "dr", "fr", "gr", "pr", "tr",
        "bl", "cl", "fl", "gl", "pl",
        "vr",
        "sc", "sp", "st",
        "ct", "pt"
    ]

    for encontro in encontros:
        pontos += palavra.count(encontro) * 2

    # Estruturas complexas
    estruturas_complexas = [
        "ção",
        "são",
        "tivo",
        "tiva",
        "mente",
        "ncia",
        "ncio",
        "qu",
        "gu"
    ]

    for estrutura in estruturas_complexas:

        if estrutura in palavra_original:
            pontos += 1

    # Consoantes consecutivas
    maior_sequencia = 0
    sequencia = 0

    for letra in palavra:

        if letra not in vogais:

            sequencia += 1

            if sequencia > maior_sequencia:
                maior_sequencia = sequencia

        else:

            sequencia = 0

    if maior_sequencia >= 3:
        pontos += 3
    elif maior_sequencia == 2:
        pontos += 1

    return pontos


def nivel_dificuldade(palavra):

    dificuldade = calcular_dificuldade(palavra)

    if dificuldade <= 2:
        return 1
    elif dificuldade <= 4:
        return 2
    elif dificuldade <= 6:
        return 3
    elif dificuldade <= 8:
        return 4
    elif dificuldade <= 10:
        return 5
    elif dificuldade <= 12:
        return 6
    elif dificuldade <= 14:
        return 7
    elif dificuldade <= 16:
        return 8
    elif dificuldade <= 18:
        return 9
    else:
        return 10


# ============================================================
# JOGO
# ============================================================

class JogoDitado:

    def __init__(self):

        self.palavras = self._carregar_palavras()

        if not self.palavras:

            print("ERRO: Nenhuma palavra foi carregada.")

            self.palavras = [
                "casa",
                "bola",
                "gato",
                "pato",
                "mesa",
                "banana",
                "escola",
                "caderno",
                "janela",
                "sapato"
            ]

        self.dominios = {}

        self._inicializar_dominios()

        self.carregar_progresso()

        self.nivel = 1
        self.pontos = 0
        self.acertos = 0
        self.erros = 0
        self.vidas = VIDAS_INICIAIS
        self.sequencia = 0
        self.melhor_sequencia = 0
        self.pergunta_nivel = 0

        self.palavra_atual = ""

        self.palavras_nivel = []
        self.indice_palavra = 0

        self.palavras_revisao = []

        self.atualizar_palavras_revisao()

        self.preparar_nivel()

        print(
            f"PALAVRAS CARREGADAS: {len(self.palavras)}"
        )

    # ========================================================
    # CARREGAR PALAVRAS
    # ========================================================

    def _carregar_palavras(self):

        resultado = []
        usadas = set()

        try:

            dados = PALAVRAS

            if isinstance(dados, (list, tuple, set)):

                palavras = list(dados)

            elif isinstance(dados, dict):

                palavras = []

                for valor in dados.values():

                    if isinstance(
                        valor,
                        (list, tuple, set)
                    ):

                        palavras.extend(valor)

                    elif isinstance(valor, str):

                        palavras.append(valor)

            else:

                print(
                    "ERRO: Formato de PALAVRAS não reconhecido."
                )

                return []

            for palavra in palavras:

                if not isinstance(palavra, str):
                    continue

                palavra = palavra.strip().lower()

                if not palavra:
                    continue

                if not all(
                    caractere.isalpha()
                    for caractere in palavra
                ):
                    continue

                chave = normalizar_palavra(palavra)

                if chave in usadas:
                    continue

                usadas.add(chave)

                resultado.append(palavra)

        except Exception as erro:

            print(
                "ERRO AO CARREGAR PALAVRAS:",
                erro
            )

            return []

        return resultado

    # ========================================================
    # NOVO REGISTRO
    # ========================================================

    def _novo_registro_palavra(self):

        return {
            "acertos": 0,
            "erros": 0,
            "dominio": 0,
            "tentativas": 0,
            "ultimo_resultado": "",
            "prioridade": 0
        }

    # ========================================================
    # INICIALIZAR
    # ========================================================

    def _inicializar_dominios(self):

        for palavra in self.palavras:

            if palavra not in self.dominios:

                self.dominios[palavra] = (
                    self._novo_registro_palavra()
                )

    # ========================================================
    # CARREGAR PROGRESSO
    # ========================================================

    def carregar_progresso(self):

        if not os.path.exists(ARQUIVO_PROGRESSO):
            return

        try:

            with open(
                ARQUIVO_PROGRESSO,
                "r",
                encoding="utf-8"
            ) as arquivo:

                dados = json.load(arquivo)

            if not isinstance(dados, dict):
                return

            for palavra, valores in dados.items():

                if palavra not in self.dominios:
                    continue

                if not isinstance(valores, dict):
                    continue

                dados_palavra = self.dominios[palavra]

                dados_palavra["acertos"] = int(
                    valores.get("acertos", 0)
                )

                dados_palavra["erros"] = int(
                    valores.get("erros", 0)
                )

                dados_palavra["dominio"] = int(
                    valores.get("dominio", 0)
                )

                dados_palavra["tentativas"] = int(
                    valores.get("tentativas", 0)
                )

                dados_palavra["ultimo_resultado"] = (
                    valores.get(
                        "ultimo_resultado",
                        ""
                    )
                )

                dados_palavra["prioridade"] = int(
                    valores.get("prioridade", 0)
                )

        except Exception as erro:

            print(
                "ERRO AO CARREGAR PROGRESSO:",
                erro
            )

        self.atualizar_palavras_revisao()

    # ========================================================
    # SALVAR
    # ========================================================

    def salvar_progresso(self):

        try:

            with open(
                ARQUIVO_PROGRESSO,
                "w",
                encoding="utf-8"
            ) as arquivo:

                json.dump(
                    self.dominios,
                    arquivo,
                    ensure_ascii=False,
                    indent=4
                )

        except Exception as erro:

            print(
                "ERRO AO SALVAR PROGRESSO:",
                erro
            )

    # ========================================================
    # REVISÃO
    # ========================================================

    def atualizar_palavras_revisao(self):

        palavras = []

        for palavra, dados in self.dominios.items():

            erros = dados.get("erros", 0)
            dominio = dados.get("dominio", 0)

            if (
                erros > 0
                and
                dominio < DOMINIO_APRENDIDA
            ):

                palavras.append(palavra)

        palavras.sort(
            key=lambda palavra:
            self.dominios[palavra].get(
                "prioridade",
                0
            ),
            reverse=True
        )

        self.palavras_revisao = palavras

    # ========================================================
    # PREPARAR NÍVEL
    # ========================================================

    def preparar_nivel(self):

        self.pergunta_nivel = 0
        self.vidas = VIDAS_INICIAIS
        self.indice_palavra = 0

        lista = []

        dificuldade_maxima = min(
            10,
            max(1, self.nivel)
        )

        # Palavras prioritárias
        prioritarias = [
            palavra
            for palavra in self.palavras
            if (
                self.dominios[palavra].get(
                    "prioridade",
                    0
                ) > 0
                and
                self.dominios[palavra].get(
                    "dominio",
                    0
                ) < DOMINIO_APRENDIDA
            )
        ]

        prioritarias.sort(
            key=lambda palavra:
            self.dominios[palavra].get(
                "prioridade",
                0
            ),
            reverse=True
        )

        for palavra in prioritarias:

            if palavra not in lista:
                lista.append(palavra)

            if len(lista) >= 5:
                break

        # Palavras do nível
        palavras_nivel = [
            palavra
            for palavra in self.palavras
            if (
                palavra not in lista
                and
                nivel_dificuldade(
                    palavra
                ) <= dificuldade_maxima
            )
        ]

        aprendendo = []
        novas = []
        aprendidas = []

        for palavra in palavras_nivel:

            dados = self.dominios[palavra]

            tentativas = dados.get(
                "tentativas",
                0
            )

            dominio = dados.get(
                "dominio",
                0
            )

            if tentativas == 0:

                novas.append(palavra)

            elif dominio < DOMINIO_APRENDIDA:

                aprendendo.append(palavra)

            else:

                aprendidas.append(palavra)

        random.shuffle(aprendendo)

        for palavra in aprendendo:

            if len(lista) >= 8:
                break

            if palavra not in lista:
                lista.append(palavra)

        random.shuffle(novas)

        for palavra in novas:

            if len(lista) >= PALAVRAS_POR_NIVEL:
                break

            lista.append(palavra)

        random.shuffle(aprendidas)

        for palavra in aprendidas:

            if len(lista) >= PALAVRAS_POR_NIVEL:
                break

            lista.append(palavra)

        # Completar
        if len(lista) < PALAVRAS_POR_NIVEL:

            restantes = [
                palavra
                for palavra in self.palavras
                if palavra not in lista
            ]

            random.shuffle(restantes)

            for palavra in restantes:

                if len(lista) >= PALAVRAS_POR_NIVEL:
                    break

                lista.append(palavra)

        self.palavras_nivel = (
            lista[:PALAVRAS_POR_NIVEL]
        )

        if self.palavras_nivel:

            self.palavra_atual = (
                self.palavras_nivel[0]
            )

        else:

            self.palavra_atual = ""

    # ========================================================
    # NOVA PALAVRA
    # ========================================================

    def nova_palavra(self):

        if not self.palavras_nivel:

            self.preparar_nivel()

        if self.pergunta_nivel >= PALAVRAS_POR_NIVEL:
            return

        self.indice_palavra = (
            self.pergunta_nivel
        )

        if self.indice_palavra < len(
            self.palavras_nivel
        ):

            self.palavra_atual = (
                self.palavras_nivel[
                    self.indice_palavra
                ]
            )

        elif self.palavras:

            self.palavra_atual = random.choice(
                self.palavras
            )

    # ========================================================
    # VERIFICAR RESPOSTA
    # ========================================================

    def verificar_resposta(self, resposta):

        correta = normalizar_palavra(
            self.palavra_atual
        )

        digitada = normalizar_palavra(
            resposta
        )

        if correta == digitada:

            self.registrar_acerto(
                self.palavra_atual
            )

            self.acertos += 1
            self.sequencia += 1

            if self.sequencia > self.melhor_sequencia:

                self.melhor_sequencia = (
                    self.sequencia
                )

            pontos = 10

            if self.sequencia >= 3:
                pontos += 2

            self.pontos += pontos

            self.pergunta_nivel += 1

            terminou = (
                self.pergunta_nivel
                >= PALAVRAS_POR_NIVEL
            )

            self.atualizar_palavras_revisao()
            self.salvar_progresso()

            return True, terminou

        self.registrar_erro(
            self.palavra_atual
        )

        self.erros += 1
        self.sequencia = 0
        self.vidas -= 1

        if self.vidas < 0:
            self.vidas = 0

        self.atualizar_palavras_revisao()
        self.salvar_progresso()

        return False, False

    # ========================================================
    # ACERTO
    # ========================================================

    def registrar_acerto(self, palavra):

        if palavra not in self.dominios:

            self.dominios[palavra] = (
                self._novo_registro_palavra()
            )

        dados = self.dominios[palavra]

        dados["acertos"] += 1
        dados["tentativas"] += 1
        dados["ultimo_resultado"] = "acerto"

        dados["dominio"] += 1

        if dados["dominio"] > DOMINIO_APRENDIDA:

            dados["dominio"] = DOMINIO_APRENDIDA

        dados["prioridade"] -= 2

        if dados["prioridade"] < 0:

            dados["prioridade"] = 0

    # ========================================================
    # ERRO
    # ========================================================

    def registrar_erro(self, palavra):

        if palavra not in self.dominios:

            self.dominios[palavra] = (
                self._novo_registro_palavra()
            )

        dados = self.dominios[palavra]

        dados["erros"] += 1
        dados["tentativas"] += 1
        dados["ultimo_resultado"] = "erro"

        dados["dominio"] -= 1

        if dados["dominio"] < 0:
            dados["dominio"] = 0

        dados["prioridade"] += 3

        if dados["prioridade"] > 20:
            dados["prioridade"] = 20

    # ========================================================
    # PRÓXIMO NÍVEL
    # ========================================================

    def passar_de_nivel(self):

        self.nivel += 1

        self.acertos = 0
        self.erros = 0
        self.pontos = 0
        self.sequencia = 0
        self.vidas = VIDAS_INICIAIS
        self.pergunta_nivel = 0
        self.indice_palavra = 0
        self.palavra_atual = ""

        self.preparar_nivel()

        self.salvar_progresso()

    # ========================================================
    # REINICIAR
    # ========================================================

    def reiniciar_nivel(self):

        self.acertos = 0
        self.erros = 0
        self.pontos = 0
        self.sequencia = 0
        self.vidas = VIDAS_INICIAIS
        self.pergunta_nivel = 0
        self.indice_palavra = 0
        self.palavra_atual = ""

        self.preparar_nivel()

    # ========================================================
    # PALAVRAS APRENDIDAS
    # ========================================================

    def palavras_aprendidas(self):

        return [
            palavra
            for palavra, dados
            in self.dominios.items()
            if dados.get(
                "dominio",
                0
            ) >= DOMINIO_APRENDIDA
        ]

    # ========================================================
    # PALAVRAS APRENDENDO
    # ========================================================

    def palavras_aprendendo(self):

        resultado = []

        for palavra, dados in self.dominios.items():

            dominio = dados.get(
                "dominio",
                0
            )

            tentativas = dados.get(
                "tentativas",
                0
            )

            if (
                tentativas > 0
                and
                dominio > 0
                and
                dominio < DOMINIO_APRENDIDA
            ):

                resultado.append(palavra)

        return resultado

    # ========================================================
    # PALAVRAS PARA TREINAR
    # ========================================================

    def palavras_para_treinar(self):

        resultado = []

        for palavra, dados in self.dominios.items():

            erros = dados.get(
                "erros",
                0
            )

            dominio = dados.get(
                "dominio",
                0
            )

            if (
                erros > 0
                and
                dominio < DOMINIO_APRENDIDA
            ):

                resultado.append(palavra)

        resultado.sort(
            key=lambda palavra:
            self.dominios[palavra].get(
                "prioridade",
                0
            ),
            reverse=True
        )

        return resultado

    # ========================================================
    # DADOS DA PALAVRA
    # ========================================================

    def dados_palavra(self, palavra):

        return self.dominios.get(
            palavra,
            self._novo_registro_palavra()
        )

    # ========================================================
    # DIFICULDADE
    # ========================================================

    def dificuldade_palavra(self, palavra):

        return calcular_dificuldade(
            palavra
        )

    # ========================================================
    # NÍVEL DA PALAVRA
    # ========================================================

    def nivel_da_palavra(self, palavra):

        return nivel_dificuldade(
            palavra
        )

    # ========================================================
    # RESETAR
    # ========================================================

    def resetar_progresso(self):

        self.dominios = {}

        self._inicializar_dominios()

        self.atualizar_palavras_revisao()

        self.salvar_progresso()

    # ========================================================
    # ESTATÍSTICAS
    # ========================================================

    def estatisticas(self):

        return {

            "total_palavras": len(
                self.palavras
            ),

            "aprendidas": len(
                self.palavras_aprendidas()
            ),

            "aprendendo": len(
                self.palavras_aprendendo()
            ),

            "treinar": len(
                self.palavras_para_treinar()
            )

        }