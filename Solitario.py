# random permite embaralhar o baralho.
import random

# Path facilita localizar a pasta das imagens.
from pathlib import Path

# Importa o Flet usando o apelido ft.
import flet as ft


# ============================================================
# CONFIGURAÇÕES
# ============================================================

# Tamanho de cada carta em pixels.
# A proporção é próxima das artes enviadas.
LARGURA = 100
ALTURA = 142

# Distância vertical entre cartas de uma mesma coluna.
ESPACO = 28

# Distância horizontal entre o início de duas colunas.
PASSO = 125

# Margem inicial do tabuleiro.
MARGEM = 20

# Altura em que começam as sete colunas.
LINHA_COLUNAS = 200

# __file__ representa este arquivo Python.
# resolve() obtém seu caminho completo.
# parent obtém a pasta em que ele está.
PASTA_ASSETS = Path(__file__).resolve().parent / "assets"

NAIPES = ["♠", "♥", "♦", "♣"]

# Um conjunto permite verificar quais naipes são vermelhos.
VERMELHOS = {"♥", "♦"}

# Dicionário: associa um número à letra da carta.
NOMES = {
    1: "A",
    11: "J",
    12: "Q",
    13: "K",
}

# Cada chave é uma tupla: (número, naipe).
# Cada valor é o nome da imagem correspondente.
#
# 12 = Rainha, representada por Q.
# 13 = Rei, representado por K.
ARTES = {
    (13, "♠"): "rei_espadas.jpeg",
    (13, "♥"): "rei_copas.jpeg",
    (13, "♦"): "rei_ouros.jpeg",
    (13, "♣"): "rei_paus.jpeg",

    (12, "♠"): "rainha_espadas.jpeg",
    (12, "♥"): "rainha_copas.jpeg",
    (12, "♦"): "rainha_ouros.jpeg",
    (12, "♣"): "rainha_paus.jpeg",
}


# ============================================================
# CLASSE CARTA
# ============================================================

# Uma classe funciona como um modelo para criar objetos.
# Cada objeto Carta guarda seus próprios dados.
class Carta:

    def __init__(self, numero, naipe):
        # __init__ executa quando criamos uma nova Carta.
        #
        # self representa a própria carta.
        # Exemplo: self.numero é o número desta carta.

        self.numero = numero
        self.naipe = naipe

        # False significa que a carta começa fechada.
        self.aberta = False

        # O controle visual será associado depois.
        self.controle = None

    @property
    def vermelha(self):
        # @property permite acessar carta.vermelha
        # como um atributo, sem escrever parênteses.
        #
        # "in" verifica se o naipe está no conjunto.
        return self.naipe in VERMELHOS

    @property
    def nome(self):
        # get() procura o número no dicionário NOMES.
        #
        # Se encontrar 13, por exemplo, devolve "K".
        # Caso contrário, devolve o número como texto.
        return NOMES.get(self.numero, str(self.numero))


# ============================================================
# CLASSE PACIENCIA
# ============================================================

class Paciencia:

    def __init__(self, page):
        # Guarda a página para atualizar a interface depois.
        self.page = page

        # Cada lista representa uma região do jogo.
        self.monte = []
        self.descarte = []

        # Cria quatro listas independentes para as bases.
        self.bases = [[] for _ in range(4)]

        # Cria sete listas independentes para as colunas.
        self.colunas = [[] for _ in range(7)]

        # Guarda as cartas selecionadas durante o arraste.
        self.arrastando = []

        # Guarda a lista de onde as cartas estão saindo.
        self.origem = None

        self.movimentos = 0

        # Text é um controle que mostra texto na tela.
        self.status = ft.Text(
            color="white",
            size=18,
        )

        # Stack permite posicionar controles usando left e top.
        # Os últimos controles da lista aparecem na frente.
        self.tabuleiro = ft.Stack(
            width=920,
            height=1000,
        )

        # Column organiza os controles verticalmente.
        # Row organiza os controles horizontalmente.
        self.page.add(
            ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Button(
                                content="Novo jogo",

                                # Passamos a função sem ().
                                # Ela será chamada quando houver clique.
                                on_click=self.novo_jogo,
                            ),
                            self.status,
                        ]
                    ),
                    ft.Text(
                        "Monte: clique para comprar | "
                        "Colunas: cores alternadas | "
                        "Bases: Ás até Rei",
                        color="#D5E8DD",
                        size=14,
                    ),
                    self.tabuleiro,
                ]
            )
        )

        # Inicia a primeira partida.
        self.novo_jogo()

    def novo_jogo(self, e=None):
        # Cria uma partida nova.
        #
        # e representa o evento do botão.
        # O padrão None também permite chamar a função
        # diretamente, sem um evento.

        # Esta compreensão de lista combina:
        # quatro naipes × treze números = 52 cartas.
        baralho = [
            Carta(numero, naipe)
            for naipe in NAIPES
            for numero in range(1, 14)
        ]

        # Embaralha a própria lista.
        random.shuffle(baralho)

        # Limpa os dados da partida anterior.
        self.colunas = [[] for _ in range(7)]
        self.bases = [[] for _ in range(4)]
        self.descarte = []
        self.arrastando = []
        self.origem = None
        self.movimentos = 0

        # enumerate() fornece o índice e o elemento.
        # Os índices começam em zero.
        for indice, coluna in enumerate(self.colunas):

            # Coluna 0 recebe uma carta.
            # Coluna 1 recebe duas, e assim por diante.
            for _ in range(indice + 1):

                # pop() retira e devolve a última carta.
                coluna.append(baralho.pop())

            # O índice -1 acessa o último elemento.
            # Apenas a carta superior começa aberta.
            coluna[-1].aberta = True

        # O restante forma o monte de compra.
        self.monte = baralho

        self.desenhar()

    def criar_espaco(self, x, y, texto, clicar=None):
        # Desenha uma posição vazia para receber cartas.
        #
        # x e y são as coordenadas no Stack.
        # clicar é uma função opcional para o clique.

        return ft.Container(
            left=x,
            top=y,
            width=LARGURA,
            height=ALTURA,
            border=ft.Border.all(2, "#8AB8A1"),
            border_radius=10,

            # Alinhamento (0, 0) significa centro.
            alignment=ft.Alignment(0, 0),

            content=ft.Text(
                texto,
                size=30,
                color="#BBD8C9",
            ),

            on_click=clicar,
        )

    def criar_verso(self):
        # Cria a imagem usada nas cartas fechadas.
        #
        # O caminho é relativo à pasta assets,
        # configurada em ft.run() no final do arquivo.

        return ft.Container(
            width=LARGURA,
            height=ALTURA,
            content=ft.Image(
                src="verso.png",
                width=LARGURA,
                height=ALTURA,
            ),
        )

    def criar_indicador(self, carta):
        # Cria uma etiqueta pequena com número e naipe.
        #
        # Ela facilita identificar as artes nas pilhas,
        # mesmo quando o título da imagem fica escondido.

        cor = "#C62828" if carta.vermelha else "#17212B"

        return ft.Container(
            left=3,
            top=2,
            width=43,
            height=23,
            bgcolor="#FFFEF8",
            border_radius=4,
            alignment=ft.Alignment(0, 0),
            content=ft.Text(
                f"{carta.nome}{carta.naipe}",
                size=17,
                color=cor,
                weight=ft.FontWeight.BOLD,
            ),
        )

    def criar_visual(self, carta):
        # Escolhe a aparência da carta:
        # 1. Fechada: verso.
        # 2. Rei ou Rainha: arte personalizada.
        # 3. Outras cartas: número e símbolo.

        if not carta.aberta:
            return self.criar_verso()

        # Forma a chave para procurar a imagem.
        chave = (carta.numero, carta.naipe)

        # get() devolve None se não houver arte para a carta.
        arquivo = ARTES.get(chave)

        if arquivo is not None:
            # O Stack coloca a etiqueta por cima da arte.
            # A imagem usa toda a área da carta, sem
            # o cabeçalho separado da versão anterior.
            return ft.Container(
                width=LARGURA,
                height=ALTURA,
                content=ft.Stack(
                    width=LARGURA,
                    height=ALTURA,
                    controls=[
                        ft.Image(
                            src=arquivo,
                            left=0,
                            top=0,
                            width=LARGURA,
                            height=ALTURA,
                        ),
                        self.criar_indicador(carta),
                    ],
                ),
            )

        # Expressão condicional:
        # usa vermelho se a carta for vermelha;
        # caso contrário, usa a cor escura.
        cor = "#C62828" if carta.vermelha else "#17212B"

        return ft.Container(
            width=LARGURA,
            height=ALTURA,
            bgcolor="#FFFEF8",
            border=ft.Border.all(1, "#C9C9C9"),
            border_radius=10,
            content=ft.Column(
                spacing=0,
                controls=[
                    ft.Container(
                        height=ESPACO,
                        padding=ft.Padding.only(left=5),
                        content=ft.Text(
                            f"{carta.nome}{carta.naipe}",
                            size=18,
                            color=cor,
                            weight=ft.FontWeight.BOLD,
                        ),
                    ),
                    ft.Container(
                        # expand ocupa o espaço restante.
                        expand=True,
                        alignment=ft.Alignment(0, 0),
                        content=ft.Text(
                            carta.naipe,
                            size=40,
                            color=cor,
                        ),
                    ),
                ],
            ),
        )

    def adicionar_carta(self, carta, x, y):
        # GestureDetector detecta gestos sobre a carta.
        #
        # on_pan_start: início do arraste.
        # on_pan_update: movimento.
        # on_pan_end: soltura.

        controle = ft.GestureDetector(
            left=x,
            top=y,
            mouse_cursor=ft.MouseCursor.MOVE,
            drag_interval=10,
            content=self.criar_visual(carta),

            # lambda cria uma função curta.
            # c=carta guarda a carta deste controle.
            on_pan_start=lambda e, c=carta: self.iniciar_arraste(e, c),

            on_pan_update=self.arrastar,
            on_pan_end=self.soltar,
        )

        # Liga os dados da carta ao controle visual.
        carta.controle = controle

        # append() adiciona um elemento no fim da lista.
        self.tabuleiro.controls.append(controle)

    def desenhar(self):
        # Reconstrói os controles a partir das listas.
        #
        # Os dados são a fonte da verdade:
        # o desenho apenas representa onde as cartas estão.

        self.tabuleiro.controls.clear()

        # Espaço do monte.
        self.tabuleiro.controls.append(
            self.criar_espaco(
                MARGEM,
                MARGEM,
                "↻",
                self.comprar,
            )
        )

        # Lista não vazia é considerada verdadeira no if.
        if self.monte:
            self.tabuleiro.controls.append(
                ft.Container(
                    left=MARGEM,
                    top=MARGEM,
                    width=LARGURA,
                    height=ALTURA,
                    content=self.criar_verso(),
                    on_click=self.comprar,
                )
            )

        # Espaço do descarte.
        self.tabuleiro.controls.append(
            self.criar_espaco(
                MARGEM + PASSO,
                MARGEM,
                "",
            )
        )

        # Só a carta superior do descarte fica visível.
        if self.descarte:
            self.adicionar_carta(
                self.descarte[-1],
                MARGEM + PASSO,
                MARGEM,
            )

        # Desenha as quatro bases.
        for indice, base in enumerate(self.bases):
            x = MARGEM + (indice + 3) * PASSO

            self.tabuleiro.controls.append(
                self.criar_espaco(
                    x,
                    MARGEM,
                    NAIPES[indice],
                )
            )

            if base:
                self.adicionar_carta(
                    base[-1],
                    x,
                    MARGEM,
                )

        # Desenha as sete colunas.
        for indice, coluna in enumerate(self.colunas):
            x = MARGEM + indice * PASSO

            self.tabuleiro.controls.append(
                self.criar_espaco(
                    x,
                    LINHA_COLUNAS,
                    "",
                )
            )

            for posicao, carta in enumerate(coluna):
                y = LINHA_COLUNAS + posicao * ESPACO

                self.adicionar_carta(carta, x, y)

        # sum() soma a quantidade de cartas nas quatro bases.
        venceu = sum(len(base) for base in self.bases) == 52

        if venceu:
            self.status.value = "Você venceu! 👑"
        else:
            self.status.value = f"Movimentos: {self.movimentos}"

        # Envia as alterações para a interface.
        self.page.update()

    def comprar(self, e):
        # Compra uma carta por vez.
        # Quando o monte acaba, permite reciclar o descarte.

        if self.monte:
            carta = self.monte.pop()
            carta.aberta = True
            self.descarte.append(carta)

        elif self.descarte:
            # reversed() inverte a ordem.
            # list() transforma o resultado em uma lista.
            self.monte = list(reversed(self.descarte))
            self.descarte.clear()

            for carta in self.monte:
                carta.aberta = False

        else:
            # return encerra a função se não houver cartas.
            return

        self.movimentos += 1
        self.desenhar()

    def localizar(self, carta):
        # Encontra a lista em que a carta está.
        #
        # O * desempacota as listas de bases e colunas,
        # colocando cada pilha na lista de pesquisa.

        listas = [
            self.descarte,
            *self.bases,
            *self.colunas,
        ]

        for lista in listas:
            if carta in lista:
                return lista

        # None indica que nenhuma origem foi encontrada.
        return None

    def sequencia_valida(self, cartas):
        # Verifica se todas as cartas podem se mover juntas.

        # all() só devolve True se todas estiverem abertas.
        if not all(carta.aberta for carta in cartas):
            return False

        # cartas[1:] pega a lista sem o primeiro elemento.
        # zip() forma pares de cartas vizinhas.
        for anterior, seguinte in zip(cartas, cartas[1:]):

            # A sequência precisa ser decrescente.
            if anterior.numero != seguinte.numero + 1:
                return False

            # Cartas vizinhas precisam ter cores diferentes.
            if anterior.vermelha == seguinte.vermelha:
                return False

        return True

    def iniciar_arraste(self, e, carta):
        # Prepara a movimentação de uma carta ou sequência.

        self.arrastando = []
        self.origem = None

        if not carta.aberta:
            return

        origem = self.localizar(carta)

        # Usamos "is None" em vez de "if not origem"
        # para verificar especificamente ausência de resultado.
        if origem is None:
            return

        # index() encontra a posição da carta na lista.
        indice = origem.index(carta)

        # any() devolve True se alguma condição for verdadeira.
        # "is" verifica se é exatamente a mesma lista.
        eh_coluna = any(
            origem is coluna
            for coluna in self.colunas
        )

        # Fora das colunas, apenas a carta do topo pode sair.
        if not eh_coluna and indice != len(origem) - 1:
            return

        # Seleciona da carta escolhida até o final da pilha.
        cartas = origem[indice:]

        if not self.sequencia_valida(cartas):
            return

        self.origem = origem
        self.arrastando = cartas

        # Retira e recoloca os controles no fim do Stack.
        # Assim, as cartas arrastadas aparecem na frente.
        for atual in cartas:
            controle = atual.controle
            self.tabuleiro.controls.remove(controle)
            self.tabuleiro.controls.append(controle)

        self.page.update()

    def arrastar(self, e):
        # Move todas as cartas selecionadas.
        #
        # local_delta informa o deslocamento desde
        # o evento anterior, nos eixos x e y.

        if not self.arrastando:
            return

        for carta in self.arrastando:
            carta.controle.left += e.local_delta.x
            carta.controle.top += e.local_delta.y

        self.page.update()

    def aceita_base(self, indice):
        # Bases recebem uma carta de cada vez,
        # do Ás ao Rei e sempre do mesmo naipe.

        if len(self.arrastando) != 1:
            return False

        carta = self.arrastando[0]
        base = self.bases[indice]

        if carta.naipe != NAIPES[indice]:
            return False

        # Base vazia: len(base) é 0, então aceita 1 (Ás).
        # Base com Ás: len(base) é 1, então aceita 2.
        return carta.numero == len(base) + 1

    def aceita_coluna(self, coluna):
        # Valida a primeira carta da sequência arrastada.

        carta = self.arrastando[0]

        # Coluna vazia aceita somente Rei.
        if not coluna:
            return carta.numero == 13

        topo = coluna[-1]

        # "and" exige que todas as condições sejam verdadeiras.
        return (
            topo.aberta
            and topo.numero == carta.numero + 1
            and topo.vermelha != carta.vermelha
        )

    def encontrar_destino(self, x, y):
        # Procura uma base ou coluna próxima à carta solta.
        #
        # abs() calcula a distância sem sinal negativo.

        for indice, base in enumerate(self.bases):
            destino_x = MARGEM + (indice + 3) * PASSO

            perto = (
                abs(x - destino_x) < LARGURA / 2
                and abs(y - MARGEM) < ALTURA / 2
            )

            if (
                base is not self.origem
                and perto
                and self.aceita_base(indice)
            ):
                return base

        for indice, coluna in enumerate(self.colunas):
            destino_x = MARGEM + indice * PASSO

            # max() impede que uma coluna vazia
            # produza uma posição acima do início.
            destino_y = (
                LINHA_COLUNAS
                + max(0, len(coluna) - 1) * ESPACO
            )

            perto = (
                abs(x - destino_x) < LARGURA / 2
                and abs(y - destino_y) < ALTURA / 2
            )

            if (
                coluna is not self.origem
                and perto
                and self.aceita_coluna(coluna)
            ):
                return coluna

        return None

    def soltar(self, e):
        # Finaliza o arraste e aplica a jogada, se válida.

        if not self.arrastando:
            return

        primeira = self.arrastando[0].controle

        destino = self.encontrar_destino(
            primeira.left,
            primeira.top,
        )

        # Uma lista vazia pode ser um destino válido.
        # Por isso, verificamos "is not None".
        if destino is not None:
            quantidade = len(self.arrastando)

            # Remove as cartas do final da origem.
            del self.origem[-quantidade:]

            # extend() adiciona várias cartas ao destino.
            destino.extend(self.arrastando)

            eh_coluna = any(
                self.origem is coluna
                for coluna in self.colunas
            )

            # Revela a nova carta superior da origem.
            if eh_coluna and self.origem:
                self.origem[-1].aberta = True

            self.movimentos += 1

        # Se não houve destino válido, nenhuma lista mudou.
        # Ao redesenhar, as cartas voltam ao lugar original.
        self.arrastando = []
        self.origem = None

        self.desenhar()


# ============================================================
# INÍCIO DO APLICATIVO
# ============================================================

def main(page: ft.Page):
    # O Flet chama main e fornece o objeto Page.
    # Page representa a página ou janela do aplicativo.

    page.title = "Paciência Real do Careca"
    page.bgcolor = "#145A3A"
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    # values() obtém os nomes das imagens do dicionário.
    arquivos_necessarios = [
        "verso.png",
        *ARTES.values(),
    ]

    # Guarda somente os arquivos que não foram encontrados.
    # is_file() verifica se o caminho aponta para um arquivo.
    faltando = [
        nome
        for nome in arquivos_necessarios
        if not (PASTA_ASSETS / nome).is_file()
    ]

    if faltando:
        # join() junta os nomes com uma quebra de linha.
        page.add(
            ft.Text(
                "Faltam estas imagens na pasta assets:\n\n"
                + "\n".join(faltando)
                + "\n\nConfira os nomes e as extensões."
                + "\nDepois feche e abra o jogo novamente.",
                color="white",
                size=20,
            )
        )
        return

    # Cria o objeto que controla a partida.
    Paciencia(page)


# Só inicia o aplicativo quando este arquivo é executado.
# Isso permite importar suas classes sem abrir o jogo.
if __name__ == "__main__":
    ft.run(
        main,
        assets_dir=str(PASTA_ASSETS),
    )