from sklearn.tree import DecisionTreeClassifier as DTC
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from estudo import Estudo
from os import path
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from alive_progress import alive_bar
from joblib import dump, load

def gerar_dados():

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
	
	
def teste_tree(dados):
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
	print(best_model, precision[np.argmax(precision)])

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


def mostrar_marcha(brutos:pd.DataFrame):
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


def gerar_passos(dados:pd.DataFrame, paciente:int, movimento:int, sentido:int):
	dados[(dados['paciente']==paciente) & (dados['movimento']==movimento) & (dados['sentido'] == sentido)][['x','y']].plot(
		kind='scatter',
		x='x',
		y='y',
		title=f'Paciente {paciente} - Movimento {movimento} - Sentido {sentido}'
	)
	plt.show()
	

def main():
	# Gerar dados brutos, lendo-os a partir dos arquivos .xlsx
	brutos = gerar_dados()
	# print(brutos.head(50))

	# Calcular médias e desvio padrão, salvando os resultados em outro arquivo
	# transformar_dados()
	# dados = pd.read_parquet('dados.parquet')
	# print(dados)

	# Gerar modelo a partir de uma árvore de decisão
	# teste_tree(dados)
	
	# Testar a eficácia do modelo encontrado
	# teste_modelo()

	# Mostrar o gráfico da marcha de um paciente
	mostrar_marcha(brutos)




if __name__ == '__main__':
	main()