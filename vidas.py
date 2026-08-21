# ============================================================
# CONTROLE DE VIDAS DO DITADOGAME
# ============================================================

VIDAS_INICIAIS = 5


class ControleVidas:

    def __init__(self, vidas_iniciais=VIDAS_INICIAIS):

        self.vidas_iniciais = vidas_iniciais
        self.vidas = vidas_iniciais

    # ========================================================
    # RESETAR VIDAS
    # ========================================================

    def resetar(self):

        self.vidas = self.vidas_iniciais

        return self.vidas

    # ========================================================
    # PERDER UMA VIDA
    # ========================================================

    def perder(self):

        if self.vidas > 0:
            self.vidas -= 1

        if self.vidas < 0:
            self.vidas = 0

        return self.vidas

    # ========================================================
    # GANHAR UMA VIDA
    # ========================================================

    def ganhar(self):

        self.vidas += 1

        if self.vidas > self.vidas_iniciais:
            self.vidas = self.vidas_iniciais

        return self.vidas

    # ========================================================
    # DEFINIR VIDAS
    # ========================================================

    def definir(self, quantidade):

        try:

            quantidade = int(quantidade)

        except (ValueError, TypeError):

            quantidade = self.vidas_iniciais

        if quantidade < 0:
            quantidade = 0

        if quantidade > self.vidas_iniciais:
            quantidade = self.vidas_iniciais

        self.vidas = quantidade

        return self.vidas

    # ========================================================
    # VERIFICAR SE ACABARAM
    # ========================================================

    def acabou(self):

        return self.vidas <= 0

    # ========================================================
    # RETORNAR QUANTIDADE
    # ========================================================

    def quantidade(self):

        return self.vidas

    # ========================================================
    # RETORNAR COMO LISTA
    # ========================================================

    def como_lista(self):

        return list(range(self.vidas))

    # ========================================================
    # REPRESENTAÇÃO
    # ========================================================

    def __str__(self):

        return str(self.vidas)