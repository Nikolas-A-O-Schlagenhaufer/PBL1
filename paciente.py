from movimento import Movimento

class Paciente:
	def __init__(self, numero:int) -> None:

		self.numero = numero
		self.saudavel = self.eh_saudavel()
		self.movimentos = self.adicionar_movimentos()

	def __str__(self) -> str:
		return f"Paciente {self.numero} está {'saudável' if self.saudavel else 'doente'}"
		
	def eh_saudavel(self):
		return 1 if self.numero < 25 else 0

	def adicionar_movimentos(self) -> list:
		import os
		movimentos = []
		if self.saudavel:
			pasta = 'healthy'
		else:
			pasta = 'nohealthy'
		for arquivo in os.listdir(pasta):
			if arquivo.endswith('.xlsx') and arquivo.startswith(f"lga{self.numero}-"):
				movimentos.append(Movimento(f"{pasta}/{arquivo}"))
		return movimentos

def main():
	paciente = Paciente(15)
	print(paciente.movimentos[0].passos)

if __name__ == '__main__':
	main()