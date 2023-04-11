from passo import Passo

class Movimento:
	def __init__(self, nome_arquivo:str):
		self.tipo = nome_arquivo.split('-')[1]
		try:
			self.sentido = nome_arquivo.split('-')[2][:1]
		except:
			self.sentido = 1
		self.passos = self.adicionar_passos(nome_arquivo)

	def adicionar_passos(self, nome_arquivo:str):
		import pandas as pd
		dados = pd.read_excel(nome_arquivo).dropna()
		dados = dados[dados['Obj'] < 100]
		passos = []
		for i in range(max(dados['Obj'])):
			passo = Passo()
			passo.numero = i+1
			tempos = dados[dados['Obj'] == i+1]['Time'].to_list()
			x = dados[dados['Obj'] == i+1]['X'].to_list()
			y = dados[dados['Obj'] == i+1]['Y'].to_list()
			passo.tempos = tempos[2:]
			passo.x = x[2:]
			passo.y = y[2:]
			passo.calcanhar = (x[0], y[0])
			passo.ponta = (x[1], y[1])
			lado = dados[dados['Obj'] == i+1]['L/R'].to_list()[0]
			if lado == 0:
				passo.lado = 'E'
			else:
				passo.lado = 'D'
			passos.append(passo)
		return passos