
import pygame as pg
import os
import sys
import random
import time

config = {
	"janela": {
		"titulo": "SnakeGame",
		"tamanho": [0, 0],
		"corFundo": (2, 65, 7),
		"corGameOver": (255, 0, 0)
	},
	"jogo": {
		"area": (50, 40),
		"colidirBorda": False,
		"colidirSnake": True
	},
	"tile": {
		"tamanho": (16, 16)
	},
	"snake": {
		"tamanhoInicial": 4,
		"velocidade": 100,
		"velocidadeMinima": 15,
		"direcaoInicial": pg.K_RIGHT,
		"imagem": "snake.png",
		"imagemCarregada": ""
	},
	"pontoColeta": {
		"imagem": "pontoColeta.png",
		"imagemCarregada": ""
	},
	"textoTela": {
		"posicao": [32, 16],
		"cor": (0, 0, 0)
	},
	"direcoes": {
		pg.K_LEFT: (-1, 0),
		pg.K_RIGHT: (1, 0),
		pg.K_UP: (0,-1),
		pg.K_DOWN: (0, 1)
	},
	"direcoesOpostas": {
		pg.K_LEFT: pg.K_RIGHT,
		pg.K_RIGHT: pg.K_LEFT,
		pg.K_UP: pg.K_DOWN,
		pg.K_DOWN: pg.K_UP
	},
	"area": []
}

def definirTamanhos():
	configJogo = config["jogo"]
	areaJogo = configJogo["area"]
	tamanhoTile = config["tile"]["tamanho"]
	config["janela"]["tamanho"][0] = areaJogo[0] * tamanhoTile[0]
	config["janela"]["tamanho"][1] = areaJogo[1] * tamanhoTile[1]

	config["area"] = []
	for i in range(areaJogo[0]):
		config["area"].append([])
		for j in range(areaJogo[1]):
			config["area"][i].append(0)

def calcularPosicao(x, y):
	tamanhoTile = config["tile"]["tamanho"]
	posicaoX = x * tamanhoTile[0]
	posicaoY = y * tamanhoTile[1]
	return (posicaoX, posicaoY)

def carregarImagem(arquivo):
	return pg.image.load(os.path.join(sys.path[0], arquivo)).convert_alpha()

def definirImagemSnake():
	config["snake"]["imagemCarregada"] = carregarImagem(config["snake"]["imagem"])

def definirImagemPontoColeta():
	config["pontoColeta"]["imagemCarregada"] = carregarImagem(config["pontoColeta"]["imagem"])

def definirImagens():
	definirImagemSnake()
	definirImagemPontoColeta()

class Snake(pg.sprite.Sprite):
	def __init__(self, posicao):
		pg.sprite.Sprite.__init__(self)
		self.image = config["snake"]["imagemCarregada"]
		self.rect = self.image.get_rect(topleft = posicao)
		self.mask = pg.mask.from_surface(self.image)

class PontoColeta(pg.sprite.Sprite):
	def __init__(self, posicao):
		pg.sprite.Sprite.__init__(self)
		self.image = config["pontoColeta"]["imagemCarregada"]
		self.rect = self.image.get_rect(topleft = posicao)
		self.mask = pg.mask.from_surface(self.image)

class Controle(object):
	def __init__(self):
		self.screen = pg.display.get_surface()
		self.clock = pg.time.Clock()
		self.fps = 60.0
		self.done = False
		self.keys = pg.key.get_pressed()

		self.iniciarJogo()

	def iniciarJogo(self):
		definirTamanhos()

		self.jogoFinalizado = False
		self.tempo = time.time()

		self.movimentoLiberado = True
		self.aumentarTamanhoSnake = False
		self.posicoes = []

		self.definirPosicaoInicialSnake()
		configSnake = config["snake"]
		self.direcao = configSnake["direcaoInicial"]
		self.snake = self.criarSnake()
		self.velocidade = configSnake["velocidade"]

		self.ultimoMovimento = 0
		self.movimentos = 0
		self.proximoMovimento = 0

		self.adicionarPontoColeta()
		self.pontos = 0

	def definirPosicaoInicialSnake(self):
		areaJogo = config["jogo"]["area"]
		posicaoInicial = [int(areaJogo[0] / 2), int(areaJogo[1] / 2)]
		tamanhoInicial = config["snake"]["tamanhoInicial"]

		for i in range(tamanhoInicial):
			x, y = posicaoInicial[0] - i, posicaoInicial[1]
			self.posicoes.append([x, y])
			config["area"][x][y] = 1

	def criarSnake(self):
		snake = []

		area = config["area"]
		for i in range(len(area)):
			for j in range(len(area[i])):
				if area[i][j] == 1:
					snake.append(Snake(calcularPosicao(i, j)))

		return pg.sprite.Group(snake)

	def movimentarSnake(self):
		agora = pg.time.get_ticks()
		if self.ultimoMovimento < agora:
			self.ultimoMovimento = agora + self.velocidade

			configJogo = config["jogo"]
			areaJogo = configJogo["area"]
			colidirBorda = configJogo["colidirBorda"]
			colidirSnake = configJogo["colidirSnake"]

			posicaoVaga = [-1, -1]

			for i in range(len(self.posicoes)):
				posicao = self.posicoes[i]
				x, y = posicao[0], posicao[1]

				if i == 0:
					direcao = config["direcoes"][self.direcao]
					novoX, novoY = x + direcao[0], y + direcao[1]

					# Definir movimento automático da snake
					# if self.direcao == pg.K_DOWN:
						# if novoX >= areaJogo[0] - 1:
							# self.direcao = pg.K_LEFT
						# else:
							# self.direcao = pg.K_RIGHT
					# if novoX < 0:
						# self.direcao = pg.K_DOWN
					# if novoX >= areaJogo[0]:
						# self.direcao = pg.K_DOWN

					# direcao = config["direcoes"][self.direcao]
					# novoX, novoY = x + direcao[0], y + direcao[1]
				else:
					novoX, novoY = posicaoVaga[0], posicaoVaga[1]

				posicaoVaga = [x, y]

				if colidirBorda and (novoX >= areaJogo[0] or novoX < 0 or novoY >= areaJogo[1] or novoY < 0):
					self.jogoFinalizado = True
					break
				else:
					if not colidirBorda:
						if novoX < 0:
							novoX = areaJogo[0] - 1
						elif novoX > areaJogo[0] - 1:
							novoX = 0

						if novoY < 0:
							novoY = areaJogo[1] - 1
						elif novoY > areaJogo[1] - 1:
							novoY = 0

					if colidirSnake and config["area"][novoX][novoY] == 1:
						self.jogoFinalizado = True
						break

					self.posicoes[i] = [novoX, novoY]

					if self.aumentarTamanhoSnake and i == len(self.posicoes) - 1:
						self.posicoes.append(posicao)
						self.aumentarTamanhoSnake = False
					else:
						config["area"][x][y] = 0

					if config["area"][novoX][novoY] == 2:
						self.adicionarTamanhoSnake((novoX, novoY))

					config["area"][novoX][novoY] = 1

			self.snake = self.criarSnake()
			self.movimentos += 1
			self.movimentoLiberado = True

	def adicionarTamanhoSnake(self, posicaoPontoColeta):
		posicao = self.posicoes[len(self.posicoes) - 1]
		self.aumentarTamanhoSnake = True
		self.adicionarPontoColeta()
		self.aumentarVelocidade()
		self.pontos += 1

	def adicionarPontoColeta(self):
		configJogo = config["jogo"]
		areaJogo = configJogo["area"]

		posicaoPontoValida = False
		while not posicaoPontoValida:
			posicaoPonto = [random.randint(0, areaJogo[0] - 1), random.randint(0, areaJogo[1] - 1)]
			if config["area"][posicaoPonto[0]][posicaoPonto[1]] == 0:
				posicaoPontoValida = True
				config["area"][posicaoPonto[0]][posicaoPonto[1]] = 2
				self.pontoColeta = pg.sprite.Group(PontoColeta(calcularPosicao(posicaoPonto[0], posicaoPonto[1])))

				if areaJogo[0] * areaJogo[1] == len(self.posicoes) + 1:
					self.jogoFinalizado = True

	def aumentarVelocidade(self):
		modificadorVelocidade = 0
		if self.velocidade >= 80:
			modificadorVelocidade = 4
		elif self.velocidade >= 50:
			modificadorVelocidade = 3
		elif self.velocidade >= 30:
			modificadorVelocidade = 2
		elif self.velocidade >= 15:
			modificadorVelocidade = 1
		self.velocidade = min(self.velocidade - modificadorVelocidade, 2000)

	def carregarTextoTela(self):
		fonte = pg.font.SysFont("verdana", 32)

		if self.jogoFinalizado:
			texto = "Jogo Finalizado. Pressione F5 para reiniciar."

		self.textoTela = fonte.render(texto, 1, config["textoTela"]["cor"])
		self.posicaoTextoTela = self.textoTela.get_rect()
		self.posicaoTextoTela.topleft = config["textoTela"]["posicao"]

	def exibirVelocidade(self):
		return 100 - self.velocidade

	def exibirTempo(self):
		return "{}s".format(int(time.time() - self.tempo))

	def exibirFps(self):
		tituloJanela = "{} - Pontos: {} - Movimentos: {} - Velocidade: {} - Tempo: {} - FPS: {:.2f}".format(config["janela"]["titulo"], self.pontos, self.movimentos, self.exibirVelocidade(), self.exibirTempo(), self.clock.get_fps())
		pg.display.set_caption(tituloJanela)

	def loopEventos(self):
		for event in pg.event.get():
			self.keys = pg.key.get_pressed()

			if event.type == pg.QUIT or self.keys[pg.K_ESCAPE]:
				self.done = True
			elif event.type == pg.KEYDOWN:
				if event.key == pg.K_F5:
					self.iniciarJogo()
				elif self.movimentoLiberado and event.key != self.direcao and event.key in config["direcoes"] and event.key != config["direcoesOpostas"][self.direcao]:
					self.direcao = event.key
					self.movimentoLiberado = False

	def atualizar(self):
		if not self.jogoFinalizado:
			self.movimentarSnake()

	def desenhar(self):
		if self.jogoFinalizado:
			self.screen.fill(config["janela"]["corGameOver"])
			self.carregarTextoTela()
			self.screen.blit(self.textoTela, self.posicaoTextoTela)
		else:
			self.screen.fill(config["janela"]["corFundo"])
			self.snake.draw(self.screen)
			self.pontoColeta.draw(self.screen)

	def loopPrincipal(self):
		while not self.done:
			self.loopEventos()
			self.atualizar()
			self.desenhar()
			pg.display.update()
			if not self.jogoFinalizado:
				self.clock.tick(self.fps)
				self.exibirFps()

def main():
	os.environ['SDL_VIDEO_CENTERED'] = '1'
	pg.init()
	pg.display.set_caption(config["janela"]["titulo"])
	definirTamanhos()
	pg.display.set_mode(config["janela"]["tamanho"])
	definirImagens()
	Controle().loopPrincipal()
	pg.quit()
	sys.exit()

if __name__ == "__main__":
	main()
