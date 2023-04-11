from paciente import Paciente

class Estudo:
	def __init__(self) -> None:
		self.pacientes = self.adicionar_pacientes()
		
	def adicionar_pacientes(self) -> list:
		pacientes = []
		for i in range(1, 51):
			pacientes.append(Paciente(i))
		return pacientes

def main():
	pass

if __name__ == '__main__':
	main()