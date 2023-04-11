from paciente import Paciente

class Estudo:
	def __init__(self) -> None:
		self.pacientes = self.adicionar_pacientes()

	def listar_pacientes(self) -> list:
		import os
		pacientes = []
		pastas = ['healthy', 'nohealthy']
		for pasta in pastas:
			for arquivo in os.listdir(pasta):
				if arquivo.endswith('.xlsx') and arquivo.startswith('lga'):
					pacientes.append(arquivo.split('-')[0][3:])
		pacientes = set(pacientes)
		pacientes = [int(paciente) for paciente in pacientes]
		pacientes.sort()
		return pacientes
		
	def adicionar_pacientes(self) -> list:
		pacientes = []
		lista_pacientes = self.listar_pacientes()
		for i in lista_pacientes:
			pacientes.append(Paciente(i))
		return pacientes

def main():
	estudo = Estudo()
	print(estudo.pacientes[0])

if __name__ == '__main__':
	main()