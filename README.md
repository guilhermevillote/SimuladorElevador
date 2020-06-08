# Simulador Elevador
## Simulador de operação de um grupo de elevadores em um Hotel com 60 andares.

Nota: No início de cada dia dentro da simulação, as filas de todos os andares, inclusive do térreo, são zeradas e os elevadores são levados para o térreo, ficando de portas abertas esperando que cheguem hóspedes pelo térreo ou que algum hóspede que já está num andar peça para descer. 

### Parâmetros de entrada:
1. N_ELEVADORES: número de elevadores no sistema
2. MAX_ELEVADORES: capacidade máxima dos elevadores no sistema
3. LAMBDA: taxa de chegada de hóspedes, seguindo uma distribuição de Poisson.

### Amostras:
Média em um dia de simulação do tempo de espera na fila para subir;
Média em um dia de simulação do tamanho da fila de espera para subir

### Saída:
Dados estatísticos e gráficos referentes às amostras obtida (média das amostras segue distribuição normal)


### Variáveis:
1. NA_DIA: Controle diário da hora que cada pessoa chegou na fila;
2. ND_DIA: Controle diário da hora que cada pessoa saiu da fila;
3. NB: Controle diário da hora que cada pessoa que subiu para algum andar, descerá;
4. NF: Controle diário da hora que cada pessoa desceu;
5. lotacao_elevador_subir: controle diário, por elevador, de quantas pessoas utilizaram cada elevador por viagem;
6. i_fila: Controle diário do tamanho da fila e a hora que ocorreu a mudança;
7. ctrl_elevador: Controle para que o elevador não exceda a capacidade máxima ao descer hóspedes;
8. andares: Controle para armazenar os andares que o elevador deve parar ao subir;
9. atendimento_andares: Controle de quais andares têm hóspedes querendo descer, sendo o valor -1 para sinalizar que ninguem quer descer no referido andar, 0 para sinalizar q qualquer elevador pode ir e (1,2,3,.) para sinalizar o elevador que já está indo para o referido andar;
10. tempo_subir: Controle do tempo de subida de cada elevador;
11. tempo_terreo: Controle do tempo para chegar ao terreo de cada elevador;
12. tempo_andar: Controle do tempo para chegar ao proximo andar que terá hóspedes para descer para o térreo;
13. td: Controle do tempo da próximo hóspede que solicitará descer;
14. lista_td: Controle dos andares desses hóspedes que solicitarão descer no tempo td;
15. tc: Controle do tempo da próxima pessoa que chegará na fila do térreo;
16. n_fila: Controle do tamanho da fila do térreo;
17. t: Controle do tempo da simulação;
18. mostrador: Controle da passagem dos dias.
