

class Passo:
	def __init__(self):
		self.numero = None
		self.lado = None
		self.calcanhar = (None, None)
		self.ponta = (None, None)
		self.tempos = []
		self.x = []
		self.y = []
		
def main():
	import pandas as pd
	dados = pd.read_excel('nohealthy/lga30-1-1.xlsx').dropna()
	dados = dados[dados['Obj'] < 100]
	passos = []
	for i in range(max(dados['Obj'])):
		passo = Passo()
		passo.numero = i+1
		tempos 	= dados[dados['Obj'] == i+1]['Time'].to_list()
		x 		= dados[dados['Obj'] == i+1]['X'].to_list()
		y 		= dados[dados['Obj'] == i+1]['Y'].to_list()
		passo.tempos = tempos[4:]
		passo.x = x[4:]
		passo.y = y[4:]
		passo.calcanhar = (x[0], y[0])
		passo.ponta = (x[1], y[1])
		lado = dados[dados['Obj'] == i+1]['L/R'].to_list()[0]
		if lado == 0:
			passo.lado = 'E'
		else:
			passo.lado = 'D'
		passos.append(passo)

if __name__ == '__main__':
	main()