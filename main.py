from estudo import Estudo
import pandas as pd

def main():
	estudo = Estudo()
	colunas = [
		'paciente',
		'movimento',
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
	print(dados.head(10))
	print(dados.tail(10))

if __name__ == '__main__':
	main()