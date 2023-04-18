from sklearn.tree import DecisionTreeClassifier as DTC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from estudo import Estudo
from os import path
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from joblib import dump, load

def gerar_dados():
	"""
	Gera um arquivo de dados brutos em formato .parquet que é utilizado para 
	plotar os gráficos de marcha dos pacientes.
	"""
	if not path.exists('brutos.parquet'):
		estudo = Estudo()
		colunas = [
			'paciente',
			'movimento',
			'sentido',
			'passo',
			'lado',
			'calcanhar_x',
			'calcanhar_y',
			'ponta_x',
			'ponta_y',
			'tempo',
			'x',
			'y',
			'saudavel'
		]
		dados = []
		for paciente in estudo.pacientes:
			for movimento in paciente.movimentos:
				for passo in movimento.passos:
					for tempo, x, y in zip(passo.tempos, passo.x, passo.y):
						dados.append([
							paciente.numero,
							movimento.tipo,
							movimento.sentido,
							passo.numero,
							passo.lado,
							passo.calcanhar[0],
							passo.calcanhar[1],
							passo.ponta[0],
							passo.ponta[1],
							tempo,
							x,
							y,
							paciente.saudavel
						])

		dados = pd.DataFrame(dados, columns=colunas)
		dados.to_parquet('brutos.parquet')
		return dados
	
	return pd.read_parquet('brutos.parquet')
	

def transformar_dados():
	estudo = Estudo()
	
	medias_x = []
	medias_y = []
	desvios_x = []
	desvios_y = []
	saudavel = []

	for paciente in estudo.pacientes:
		for movimento in paciente.movimentos:
			for passo in movimento.passos:
				medias_x.append(np.mean(passo.x))
				medias_y.append(np.mean(passo.y))
				desvios_x.append(np.std(passo.x))
				desvios_y.append(np.std(passo.y))
				saudavel.append(paciente.saudavel)

	dados = {
		'medias_x' : medias_x,
		'medias_y' : medias_y,
		'desvios_x': desvios_x,
		'desvios_y': desvios_y,
		'saudavel' : saudavel
	}

	pd.DataFrame(dados).to_parquet('dados.parquet')
	
	
def teste_tree():
	"""
	A partir dos arquivos .xlsx, gera dados que serão utlizado para treinar o
	modelo de árvore de decisão. Ao final, salva o melhor modelo num arquivo
	.joblib.
	"""
	transformar_dados()
	dados = pd.read_parquet('dados.parquet')
	X = dados.drop('saudavel', axis=1)
	y = dados['saudavel']

	precision = []
	models = []

	vezes = 5000
	for i in range(vezes):
		X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=i)
		model = DTC(criterion='entropy', random_state=i)
		model.fit(X_train, y_train)

		# predict the test data
		y_pred = model.predict(X_test)

		precision.append(accuracy_score(y_test, y_pred))
		models.append(model)

	# find the best model based on the higher precision
	best_model = models[np.argmax(precision)]
	
	# print the best model
	print('Modelo a ser salvo:')
	print(best_model, 'com precisão de', precision[np.argmax(precision)])

	# save the best model
	dump(best_model, 'modelo.joblib')


def teste_modelo():
	model = load('modelo.joblib')
	print(model)

	dados = pd.read_parquet('dados.parquet')
	X = dados.drop('saudavel', axis=1)
	y = dados['saudavel']

	_, X_test, _, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
	y_pred = model.predict(X_test)

	print(confusion_matrix(y_test, y_pred))
	print(classification_report(y_test, y_pred, digits=4))
	print(accuracy_score(y_test, y_pred))


def gerar_passos(dados:pd.DataFrame, paciente:int, movimento:int, sentido:int):
	dados[(dados['paciente']==paciente) & (dados['movimento']==movimento) & (dados['sentido'] == sentido)][['x','y']].plot(
		kind='scatter',
		x='x',
		y='y',
		title=f'Paciente {paciente} - Movimento {movimento} - Sentido {sentido}'
	)
	plt.show()


def mostrar_marcha():
	opcoes = ['s', 'S', 'SIM', 'sim', 'Sim', 'sIm', 'siM', 'SIm', 'sIM', 'SiM']
	brutos = gerar_dados()
	stop = False
	while not stop:
		print(list(brutos['paciente'].unique()))
		paciente = int(input('Digite o número do paciente: '))
		pacientes = brutos[brutos['paciente']==paciente]['movimento'].unique().tolist()
		print('Legenda para os tipos de movimentos:')
		print('1 - Andar normal;')
		print('2 - Andar devagar;')
		print('3 - Andar rápido;')
		print('4 - Andar normal + teste cognitivo;')
		print('5 - Andar normal + teste motor;')
		print('8 - Andar até uma marcação visual no chão, parar e ficar lá por 10 segundos.')
		print('Depois de ter passado o tempo, continuar a andar para frente.')
		print(pacientes)
		movimento = int(input('Digite o tipo do movimento: '))
		print(brutos[(brutos['paciente']==paciente) & (brutos['movimento']==movimento)]['sentido'].unique().tolist())
		sentido = int(input('Digite o sentido do movimento: '))
		gerar_passos(brutos, paciente, movimento, sentido)
		print('Deseja parar? (s/n): ')
		if input() in opcoes:
			stop = True



def teste_paciente(paciente:pd.DataFrame):
	dados = {'medias_x':[], 'medias_y':[], 'desvios_x':[], 'desvios_y':[]}
	for i in range(max(paciente['passo'])):
		dados['medias_x'].append(np.mean(paciente[paciente['passo']==i+1]['x']))
		dados['medias_y'].append(np.mean(paciente[paciente['passo']==i+1]['y']))
		dados['desvios_x'].append(np.std(paciente[paciente['passo']==i+1]['x']))
		dados['desvios_y'].append(np.std(paciente[paciente['passo']==i+1]['y']))

	dados = pd.DataFrame(dados)
	model = load('modelo.joblib')
	results = model.predict(dados)
	chance = sum(results)/len(results)
	diagnosis = 'saudável' if chance > 0.5 else 'não saudável'
	print('===Diagnóstico===')
	if diagnosis == 'saudável':
		print(f'Chance de ser {diagnosis}: {chance*100:.2f}%')
	else:
		print(f'Chance de ser {diagnosis}: {(1-chance)*100:.2f}%')
	print('=================')


def testar_paciente(caminho:str):
	pasta = 'healthy' if int(caminho.split('-')[0][3:]) < 25 else 'nohealthy'
	paciente = pd.read_excel(f"{pasta}/{caminho}").dropna()
	paciente = paciente[paciente['Obj'] < 100]
	passos1 = {'paciente':[], 'movimento':[], 'sentido':[], 'passo':[], 'lado':[], 'calcanhar_x':[], 'calcanhar_y':[], 'ponta_x':[], 'ponta_y':[], 'tempo':[], 'x':[], 'y':[]}

	for i in range(max(paciente['Obj'])):
		pac = int(caminho.split('-')[0][3:])
		mov = int(caminho.split('-')[1][0])
		try:
			sen = int(caminho.split('-')[2][:1])
		except:
			sen = 1
		pas = i+1
		lado = int(paciente[paciente['Obj'] == i+1]['L/R'].to_list()[0])
		tempos 	= paciente[paciente['Obj'] == i+1]['Time'].to_list()
		x 		= paciente[paciente['Obj'] == i+1]['X'].to_list()
		y 		= paciente[paciente['Obj'] == i+1]['Y'].to_list()
		for j in range(len(paciente[paciente['Obj'] == i+1]) - 2):
			passos1['paciente'].append(pac)
			passos1['movimento'].append(mov)
			passos1['sentido'].append(sen)
			passos1['passo'].append(pas)
			passos1['lado'].append(lado)
			passos1['calcanhar_x'].append(x[0])
			passos1['calcanhar_y'].append(y[0])
			passos1['ponta_x'].append(x[1])
			passos1['ponta_y'].append(y[1])
			passos1['tempo'].append(tempos[j+2])
			passos1['x'].append(x[j+2])
			passos1['y'].append(y[j+2])

	colunas = [
		'paciente',
		'movimento',
		'sentido',
		'passo',
		'lado',
		'calcanhar_x',
		'calcanhar_y',
		'ponta_x',
		'ponta_y',
		'tempo',
		'x',
		'y'
	]

	paciente = pd.DataFrame(passos1, columns=colunas)

	teste_paciente(paciente)

	
def para_csv():
	dados = pd.read_parquet('dados.parquet')
	dados.to_csv('dados.csv', index=False)


def main():

	# Gerar modelo a partir de uma árvore de decisão
	# teste_tree()

	# Mostrar o gráfico da marcha de um paciente
	# mostrar_marcha()

	# Testar um paciente
	testar_paciente('lga35-1-2.xlsx')

if __name__ == '__main__':
	main()