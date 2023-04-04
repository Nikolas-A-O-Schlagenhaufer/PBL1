import pandas as pd
import matplotlib.pyplot as plt

def main():
	data = pd.read_excel('healthy/lga1-1-1.xlsx')
	data.dropna(inplace=True)
	data = data[data['Obj'] < 100]
	passos = [data[data['Obj'] == i+1] for i in range(max(data['Obj']))]
	for passo in passos:
		passo.plot(x='X', y='Y', kind='scatter', s=5, title=f"Passo: {passo['Obj'].iloc[0]}")
	plt.show()
	data.plot(x='X', y='Y', kind='scatter', s=5, title='Passos')
	plt.show()

if __name__ == '__main__':
	main()