# PBL1
Alicação desenvolvida para a disciplina de Biônica do curso de Engenharia Mecatrônica, da PUC-PR.
## **Alunos**:
- Mateus Uriel Graunke Barroso
- Nikolas Arnfried Olsson Schlagenhaufer
- Pedro Vicenzo Ceccatto
## **Código**
### Código Principal
O código principal a ser rodado é o `main.py`.

Nele, dentro da função `main()`, existem chamadas de funções que podem ser utilizadas para realizar algumas tarefas:
- `mostrar_marcha()`: é a função a qual deve ser habilitada (descomentada) para que o programa solicite o número do paciente, o número do teste e o sentido do movimento.
Com essas informações o código irá gerar o gráfico solicitado, perguntando se gostaria de gerar outro gráfico;
- `testar_paciente()`: é a função que realiza o diagnóstico do paciente do arquivo passado como entrada para a função, mostrando o resultado no terminal;
- `teste_tree()`: essa função pode ser utilizada para encontrar o melhor modelo novamente caso mais arquivos de testes de marcha sejam obtidos. 

### Códigos auxiliares
- Os outros arquivos `.py` são códigos auxiliares utilizados para o tratamento e leitura dos dados dos arquivos `.xlsx`;
- Dentro da pasta `Simulacao_unity` se encontra o código responsável por movimentar o pé e por identificar o arquivo `.csv` gerado a partir dos arquivos `.xlsx` brutos.
