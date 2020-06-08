import numpy as np
import random
import matplotlib.pyplot as plt

#####################################################################################
########################      ENTRADA DE PARAMETROS     #############################
#####################################################################################
N_ELEVADORES = 5
MAX_ELEVADOR = 6
LAMBDA = 1.5 #DEVE SER DO TIPO FLOAT

#####################################################################################
#############################      DEFINICOES      ##################################
#####################################################################################
M_DIA = 360 # 6 HORAS
DIA = 100
T = DIA * M_DIA
N_ANDARES = 60
INFINITO = 99999.9
T_PORTA = 5.0/60.0
T_ANDAR = 7.0/60.0
T_PESSOA = 2.0/60.0

#####################################################################################
###############################      METODOS      ###################################
#####################################################################################
def prox_t(t):
    u = random.uniform(0,1)
    log= np.log(u)
    t =  (t) - log/LAMBDA
    return t

def prox_t_descer():
    t = 120.0
    return t

def escolher_andar():
    listaandares = []
    for i in range (N_ANDARES):
        listaandares.append(i+1)
    num = random.choice(listaandares)
    return num

def obter_tempo(andares_elevador, andar):
    #andar eh valor absoluto
    tempo = 0.0
    if(andar == -1):
        ultimo_andar = np.max(np.nonzero(andares_elevador)) +1 #VALOR ABSOLUTO
        for i in range(ultimo_andar-1): #vai ate ultimo_andar-2
            if(andares_elevador[i]==0):
                tempo += T_ANDAR #passa por um andar 7seg
            else:
                tempo += T_ANDAR + andares_elevador[i]*T_PESSOA + 2*T_PORTA #7Seg para chegar no andar mais 2seg por pessoa para sair mais 10seg para abrir e fechar a porta
        tempo += T_ANDAR + andares_elevador[ultimo_andar-1]*T_PESSOA + T_PORTA #NO ULTIMO ANDAR ELE DEIXA A PORTA ABERTA AO ESVAZIAR
    else:
        for i in range(andar-1): #vai ate andar-2
            if(andares_elevador[i]==0):
                tempo += T_ANDAR #passa por um andar 7seg
            else:
                tempo += T_ANDAR + andares_elevador[i]*T_PESSOA + 2*T_PORTA #7Seg para chegar no andar mais 2seg por pessoa para sair mais 10seg para abrir e fechar a porta
        tempo += T_ANDAR + andares_elevador[andar-1]*T_PESSOA + T_PORTA
    return tempo

#####################################################################################
#########################      FUNCAO  DA SIMULACAO      ############################
#####################################################################################
def main():

    #VARIAVEIS UTILIZADAS PARA CALCULAR AS VARIAVEIS DE INTERESE DA SIMULACAO
    FILA_DIA = [[]for _ in range(DIA+1)]
    NA_DIA = [[]for _ in range(DIA+1)]
    ND_DIA = [[]for _ in range(DIA+1)]
    NB = [[] for _ in range(N_ANDARES)] 
    NF = [[] for _ in range(N_ANDARES)]
    lotacao_elevador_subir = [[[] for _ in range(DIA+1)] for _ in range(N_ELEVADORES)]
    i_fila = [[]for _ in range(DIA+1)]
    i_fila[0].append([0.0, 0])
    #VARIAVEIS DE CONTROLE DA SIMULACAO
    ctrl_elevador = [0]*(N_ELEVADORES)
    andares = np.zeros((N_ELEVADORES, N_ANDARES), dtype = int)
    atendimento_andares = [-1]*(N_ANDARES)
    temp_viag = [INFINITO]*(N_ELEVADORES)
    temp_volta = [INFINITO]*(N_ELEVADORES)
    temp_andar = [INFINITO]*(N_ELEVADORES)
    td = INFINITO
    lista_td = []
    tc = prox_t(0.0)
    n_fila = 0
    t = 0
    mostrador = -1

#####################################################################################
##############################      Laco While       ################################
#####################################################################################
    while(t < T):

        #MUDANCA DE DIA
        #ZERAR AS FILAS DE SUBIDA, DE DESCIDA E COLOCAR TODOS OS ELEVADORES PARADOS NO SOLO
        #CONTINUAR COM PESSOAS NOS ANDARES, QUE NAO QUEREM DESCER NO MOMENTO
        if( int(t/M_DIA) != mostrador):
            mostrador = int(t/M_DIA)
            print"TEMPO: ",t, "\tDIA: ", mostrador
            print"FILA:  ", n_fila
            ctrl_elevador = [0]*(N_ELEVADORES)
            andares = np.zeros((N_ELEVADORES, N_ANDARES), dtype = int)
            atendimento_andares = [-1]*(N_ANDARES)
            temp_viag = [INFINITO]*(N_ELEVADORES)
            temp_volta = [INFINITO]*(N_ELEVADORES)
            temp_andar = [INFINITO]*(N_ELEVADORES)
            n_fila = 0
            #zerar pessoas na fila de cada andar
            for i in range(N_ANDARES):
                for j in range(len(NF[i]), len(NB[i]), 1):
                    if ( NB[i][j] < t):
                        NF[i].append(t)

##### CASO 1: CHEGA UM PASSAGEIRO NA FILA #####
        if((tc <= min(temp_viag)) and (tc <= min(temp_volta)) and (tc <= min(temp_andar)) and (tc <= td)): 
            andar = escolher_andar()
            t = tc
            NA_DIA[int(t/M_DIA)].append(t)
            i = -1
            statement = False
            for j in range(N_ELEVADORES):
                statement = (np.max(andares[j]) == 0)
                if(statement == True):
                    i = j
                    break
            if( statement ): #TEM ELEVADOR NO SOLO
                #Ne[i] += 1
                FILA_DIA[ int(t/M_DIA) ].append( t - NA_DIA[int(t/M_DIA)][len(ND_DIA[int(t/M_DIA)])] )
                ND_DIA[int(t/M_DIA)].append(t)
                andares[i][andar-1] += 1
                temp_viag[i] = t +2*T_PORTA +T_PESSOA + obter_tempo(andares[i], -1) #ABRIR, ENTRAR, FECHAR, SUBIR, ABRIR
                tempo_descer = t  + 2*T_PORTA + T_PESSOA + obter_tempo(andares[i], andar) + prox_t_descer()
                NB[andar-1].append(tempo_descer) #VERIFICAR TEMPO
                if(tempo_descer < td):
                    td = tempo_descer
                    lista_td[:] = []
                    lista_td.append(andar)
                elif(tempo_descer == td):
                    lista.append(andar)
                    myset = set(lista_td)
                    lista_td = list(myset)
                tc = prox_t(t)
                lotacao_elevador_subir[i][int(t/M_DIA)].append(1)

            else: #NAO TEM ELEVADOR NO SOLO
                if(min(temp_volta) == INFINITO and max(temp_viag) == INFINITO ): #NAO TEM NENHUM ELEVADOR VINDO MAS TEM ALGUM QUE JA TERMINOU A VIAGEM
                    ultimos = []
                    for i in range(N_ELEVADORES):
                        if(temp_viag[i] == INFINITO and temp_andar[i] == INFINITO): #ELEVADOR PARADO
                            ultimo_andar = np.max(np.nonzero(andares[i]))
                            ultimos.append(ultimo_andar)
                        else: #ELEVADOR PEGANDO PASSAGEIROS PARA DESCER
                            ultimos.append(INFINITO)
                    a = min(ultimos)
                    indice = -1
                    for i in range (N_ELEVADORES):
                        if(ultimos[i] == a):
                            indice = i
                            break
                    if( a < INFINITO ): #EXISTE ELEVADOR PARADO
                        ultimo_andar = np.max(np.nonzero(andares[indice]))
                        temp_volta[indice] = t + (ultimo_andar+1)*T_ANDAR + T_PORTA
                tc = prox_t(t)
                n_fila = n_fila + 1
                i_fila[int(t/M_DIA)].append([t, n_fila])
                
##### CASO 2: UM ELEVADOR TERMINOU A SUA VIAGEM #####
        elif((min(temp_viag) <= tc) and (min(temp_viag) <= min(temp_volta)) and (min(temp_viag) <= min(temp_andar)) and (min(temp_viag) <= td)):
            elevador = np.argmin(temp_viag)
            ultimo_andar = np.max(np.nonzero(andares[elevador]))
            t = temp_viag[elevador]
            temp_viag[elevador] = INFINITO
            andar = -1
            for i in range(N_ANDARES-1, -1, -1): # i VAI DO N_ANDARES-1 ate o 0
                if(atendimento_andares[i] == 0):
                    andar = i
                    break
            if(andar >= 0 ): #TEM ALGUEM PARA DESCER
                if(atendimento_andares[ultimo_andar] == 0):
                    if(andar == ultimo_andar ):
                        atendimento_andares[andar] = elevador + 1
                        temp_andar[elevador] = t
                    else:
                        contador = 0
                        for i in range(len(NF[ultimo_andar]), len(NB[ultimo_andar]), +1): #i comeca em andar-2 e vai ate 0
                            if(NB[ultimo_andar][i] <= t):
                                contador += 1
                        fila = contador
                        controle = 0
                        if(ctrl_elevador[elevador] < MAX_ELEVADOR):
                            for i in range(fila):
                                NF[ultimo_andar].append(t+(i+1)*T_PESSOA)
                                ctrl_elevador[elevador] += 1
                                controle += 1
                                if (ctrl_elevador[elevador] >= MAX_ELEVADOR):
                                    break
                        if (controle < fila):
                            atendimento_andares[ultimo_andar] = 0
                        elif(controle == fila):
                            atendimento_andares[ultimo_andar] = -1 #TODAS AS PESSOAS EMBARCARAM
                        maior_andar = andar
                        dif = 0
                        if(maior_andar > ultimo_andar):
                            dif = maior_andar - ultimo_andar
                        elif(maior_andar < ultimo_andar):
                            dif = ultimo_andar - maior_andar
                        temp_andar[elevador] = t + controle*T_PESSOA + T_PORTA + dif*T_ANDAR + T_PORTA   #7seg por andar mais 5seg para abrir a porta ate o maior andar
                else:
                    dif = -1
                    dif = andar - ultimo_andar
                    if ( dif < 0):
                        dif = - dif
                    temp_andar[elevador] = t + T_PORTA + T_ANDAR*dif + T_PORTA
                    atendimento_andares[andar] = elevador + 1
            elif(n_fila > 0): #TEM ALGUEM NA FILA (BOTAO APERTADO)                             '
                temp_volta[elevador] = t + T_PORTA + (ultimo_andar+1)*T_ANDAR + T_PORTA
##### CASO 3: UM ELEVADOR CHEGA NO TERREO #####
        elif((min(temp_volta) <= tc) and (min(temp_volta) <= min(temp_viag)) and (min(temp_volta) <= min(temp_andar)) and (min(temp_volta) <= td)):
            if(n_fila>0): #TEM ALGUEM NA FILA
                elevador = np.argmin(temp_volta)
                t = temp_volta[elevador]
                temp_volta[elevador] = INFINITO
                ctrl_elevador[elevador] = 0
                for k  in range (N_ANDARES):
                    andares[elevador][k] = 0
                queremandares = []
                t_aux = t
                if( n_fila > MAX_ELEVADOR ): #A FILA ESTA MAIOR DO QUE A CAPACIDADE DO ELEVADOR
                    for i in range(MAX_ELEVADOR):
                        andar = escolher_andar()
                        queremandares.append(andar)
                        andares[elevador][andar-1] = andares[elevador][andar-1] + 1
                        i_fila[int(t/M_DIA)].append([t_aux, n_fila-(i+1)]) #sai da fila qnd chega sua hora de entrar no elevador
                        t_aux = t_aux + T_PESSOA
                        if( len(NA_DIA[int(t_aux/M_DIA)]) > len(ND_DIA[int(t_aux/M_DIA)])  ):
                            FILA_DIA[ int(t/M_DIA) ].append( t_aux - NA_DIA[int(t_aux/M_DIA)][len(ND_DIA[int(t_aux/M_DIA)])] )
                            ND_DIA[int(t_aux/M_DIA)].append(t_aux)
                    for i in range(len(queremandares)):
                        andar = queremandares[i]
                        tempo_descer = t + MAX_ELEVADOR*T_PESSOA + T_PORTA + obter_tempo(andares[elevador], andar) + prox_t_descer()
                        NB[andar-1].append(tempo_descer) #VERIFICAR TEMPO
                        if(tempo_descer < td):
                            td = tempo_descer
                            lista_td[:] = []
                            lista_td.append(andar)
                        elif(tempo_descer == td):
                            lista.append(andar)
                            myset = set(lista_td)
                            lista_td = list(myset)
                    temp_viag[elevador] = t_aux + T_PORTA + obter_tempo(andares[elevador], -1) #t_aux engloba tempo para passageiros entrar
                    n_fila = n_fila - MAX_ELEVADOR
                    lotacao_elevador_subir[elevador][int(t/M_DIA)].append(MAX_ELEVADOR)
                else: #A FILA ESTA MENOR DO QUE A CAPACIDADE DO ELEVADOR
                    for i in range((n_fila)):
                        andar = escolher_andar()
                        queremandares.append(andar)
                        andares[elevador][andar-1] = andares[elevador][andar-1] + 1
                        i_fila[int(t/M_DIA)].append([t_aux, n_fila-(i+1)])
                        t_aux = t_aux + T_PESSOA
                        if( len(NA_DIA[int(t_aux/M_DIA)]) > len(ND_DIA[int(t_aux/M_DIA)])  ):
                            FILA_DIA[ int(t/M_DIA) ].append( t_aux - NA_DIA[int(t_aux/M_DIA)][len(ND_DIA[int(t_aux/M_DIA)])] )
                            ND_DIA[int(t_aux/M_DIA)].append(t_aux)
                    for i in range(len(queremandares)):
                        andar = queremandares[i]
                        tempo_descer = t + n_fila*T_PESSOA +T_PORTA + obter_tempo(andares[elevador], andar) + prox_t_descer()
                        NB[andar-1].append(tempo_descer) #VERIFICAR TEMPO
                        if(tempo_descer < td):
                            td = tempo_descer
                            lista_td[:] = []
                            lista_td.append(andar)
                        elif(tempo_descer == td):
                            lista.append(andar)
                            myset = set(lista_td)
                            lista_td = list(myset)
                    temp_viag[elevador] = t_aux + T_PORTA + obter_tempo(andares[elevador], -1)
                    temp_volta[elevador] = INFINITO
                    lotacao_elevador_subir[elevador][int(t/M_DIA)].append(n_fila)
                    n_fila = 0
            else: #NAO TEM NINGUEM NA FILA
                elevador = np.argmin(temp_volta)
                ctrl_elevador[elevador] = 0
                t = temp_volta[elevador]
                temp_volta[elevador] = INFINITO
                for k  in range (N_ANDARES):
                    andares[elevador][k] = 0
                ###### VERIFICAR SE TEM ALGUEM PRA DESCER
                andar = -1 #VALOR BRUTO DO ANDAR MAIS LONGE QUE REQUER ATENDIMENTO 
                for i in range(N_ANDARES-1, -1, -1): #i comeca em N_ANDARES-1 e vai ate 0
                    if (atendimento_andares[i] == 0):
                        andar = i + 1
                        break
                if(andar >= 0):
                    atendimento_andares[andar - 1] = elevador + 1
                    temp_andar[elevador] = t + T_PORTA + andar*T_ANDAR + T_PORTA
                    andares[elevador][andar - 1] += 1  
##### CASO 4: UM ELEVADOR CHEGA NUM ANDAR PARA PEGAR PASSAGEIROS #####
        elif((min(temp_andar) <= tc) and (min(temp_andar) <= min(temp_viag)) and (min(temp_andar) <= min(temp_volta)) and (min(temp_andar) <= td)):
            t = min(temp_andar)
            elevador = np.argmin(temp_andar) +1 #VALOR BRUTO DO ELEVADOR
            andar = -1
            contador = 0
            for i in range(len(atendimento_andares)):
                if( atendimento_andares[i] == elevador):
                    andar = i + 1 #VALOR BRUTO DO ANDAR
                    break
            for i in range(len(NF[andar-1]), len(NB[andar-1]), +1): #i comeca em andar-2 e vai ate 0
                if(NB[andar-1][i] <= t):
                    contador += 1
            fila = contador
            controle = 0
            if(ctrl_elevador[elevador-1] < MAX_ELEVADOR):
                for i in range(fila):
                    NF[andar-1].append(t+(i+1)*T_PESSOA)
                    ctrl_elevador[elevador-1] += 1
                    controle += 1
                    if (ctrl_elevador[elevador-1] >= MAX_ELEVADOR):
                        break
            if (controle < fila):
                atendimento_andares[andar-1] = 0
            elif (controle == fila):
                atendimento_andares[andar-1] = -1 #TODAS AS PESSOAS EMBARCARAM
            prox_andar = -1 #VALOR BRUTO DO ANDAR
            for i in range(andar-2, -1, -1): #i comeca em andar-2 e vai ate 0
                if(atendimento_andares[i] == 0):
                    prox_andar = i + 1 #VALOR BRUTO DO ANDAR
                    break
            if (prox_andar == -1 ): # PROXIMO ANDAR EH O TERREO
                temp_andar[elevador-1] = INFINITO
                temp_volta[elevador-1] = t + T_PORTA + andar*T_ANDAR + T_PORTA + ctrl_elevador[elevador-1]*T_PESSOA #fecha a porta e vai ate o terreo
            else: #PROXIMO ANDAR NAO EH O TERREO
                dif = andar - prox_andar
                temp_andar[elevador-1] = t + controle*T_PESSOA + T_PORTA + dif*T_ANDAR + T_PORTA #7seg por andar mais 5seg para abrir a porta ate o maior andar
                atendimento_andares[prox_andar - 1] = elevador

##### CASO 5: UMA PESSOA SOLICITA DESCER #####
        elif((td <= min(temp_viag)) and (td <= min(temp_volta)) and (td <= min(temp_andar)) and (td <= tc)):
            t = td
            sobrou = [] #ANDARES QUE NAO SOLICITARAM ATENDIMENTO AINDA NO SISTEMA
            for i in range(len(lista_td)):
                andar = lista_td[i]
                if( atendimento_andares[andar-1] == -1): #NAO SERA ATENDIDO
                    atendimento_andares[andar-1] = 0
                    sobrou.append(andar)
            if(len(sobrou) > 0):
                elevadores = []
                for i in range(N_ELEVADORES):
                    if(temp_viag[i] == INFINITO and temp_volta[i] == INFINITO and temp_andar[i] == INFINITO ): #ELEVADOR PARADO
                        elevadores.append(i)
                if(len(elevadores) == 0):
                    for i in range(len(sobrou)):
                        andar = sobrou[i]
                        atendimento_andares[andar-1] = 0
                ########
                lista = []
                lista_elevador = []
                auxiliar = []
                auxiliar_elevador = []
                for i in range(len(elevadores)):
                    elevador = elevadores[i]
                    statement = True
                    for j in range(len(andares[elevador])):
                        if( andares[elevador][j] != 0 ):
                            statement = False
                            break
                    if (statement == False):
                        lista.append(np.max(np.nonzero(andares[elevador]))+1)#valor bruto
                        lista_elevador.append(elevador)
                for i in range(len(sobrou)):
                    for j in range(len(lista)):
                        if ( sobrou[i] == lista[j] ):
                            auxiliar.append(lista[j])
                            auxiliar_elevador.append(lista_elevador[j])
                if(len(auxiliar) > 0): #SE ALGUEM APERTOU O BOTAO NUM ANDAR QUE TEM UM ELEVADOR
                    for i in range (len(auxiliar)):
                        elevador = auxiliar_elevador[i] +1 #valor bruto
                        andar = auxiliar[i] #valor bruto
                        atendimento_andares[andar-1] = elevador
                        temp_andar[elevador-1] = t

                else: #SE NAO TEM ELEVADOR NO ANDAR
                    if(len(elevadores) == 1):
                        maior_andar = max(sobrou) - 1
                        dif = 0
                        elevador = elevadores[0]
                        statement = True
                        for j in range(len(andares[elevador])):
                            if( andares[elevador][j] != 0 ):
                                statement = False
                                break
                        if(statement):
                            ultimo_andar = -1 #TERREO
                        else:
                            ultimo_andar = np.max(np.nonzero(andares[elevador]))
                        if(maior_andar > ultimo_andar):
                            dif = maior_andar - ultimo_andar
                        elif(maior_andar < ultimo_andar):
                            dif = ultimo_andar - maior_andar
                        temp_andar[elevador] = t + T_PORTA + dif*T_ANDAR + T_PORTA #7seg por andar mais 5seg para abrir a porta ate o maior andar
                        for i in range(len(sobrou)):
                            andar = sobrou[i]
                            if(sobrou[i] == maior_andar + 1):
                                andares[elevador][andar-1] += 1 #PARA DEIXAR DIFERENTE DE ZERO (CASO O ELEVADOR ATUAL ESTEJA NO SOLO)
                                atendimento_andares[andar-1] = elevador + 1 #SERA ATENDIDO AGORA
                            else:
                                atendimento_andares[andar-1] = 0 #DEVE SER ATENDIDO MAIS TARDE
                    elif(len(elevadores) > 1):
                        maior_andar = max(sobrou) - 1
                        elevador_mais_proximo = -1
                        dif = INFINITO
                        for i in range(len(elevadores)):
                            aux_elevador = elevadores[i]
                            statement = True
                            for j in range(len(andares[aux_elevador])):
                                if( andares[aux_elevador][j] != 0 ):
                                    statement = False
                                    break
                            if(statement):
                                ultimo_andar = -1 #TERREO
                            else:
                                ultimo_andar = np.max(np.nonzero(andares[aux_elevador]))
                            dif2 = 0
                            if(maior_andar > ultimo_andar):
                                dif2 = maior_andar - ultimo_andar
                            elif(maior_andar < ultimo_andar):
                                dif2 = ultimo_andar - maior_andar
                            if (dif2 < dif):
                                dif = dif2
                                elevador_mais_proximo = aux_elevador
                        elevador = elevador_mais_proximo
                        temp_andar[elevador] = t + T_PORTA + dif*T_ANDAR + T_PORTA #7seg por andar mais 5seg para abrir a porta ate o maior andar
                        for i in range(len(sobrou)):
                            andar = sobrou[i]
                            if(sobrou[i] == maior_andar + 1):
                                andares[elevador][andar-1] += 1 #PARA DEIXAR DIFERENTE DE ZERO (CASO O ELEVADOR ATUAL ESTEJA NO SOLO)
                                atendimento_andares[andar-1] = elevador + 1 #SERA ATENDIDO AGORA PELO ELEVADOR "elevador+1"
                            else:
                                atendimento_andares[andar-1] = 0 #DEVE SER ATENDIDO MAIS TARDE
            valores = []
            andar_valores = []
            for i in range(len(NB)):#DEFININDO PROXIMO td
                for j in range(len(NB[i])):
                    if(NB[i][j] > td):
                        valores.append(NB[i][j])
                        andar_valores.append(i+1)
            td = min(valores)
            indice = valores.index(td)
            lista_td[:] = []
            lista_td.append(andar_valores[indice])
            for i in range(len(NB)):#DEFININDO ANDARES Q TEM O TEMPO td PARA ALGUEM DESCER
                for j in range(len(NB[i])):
                    if(NB[i][j] == td):
                        if(lista_td.count(i+1) == 0):
                            lista_td.append(i+1)

#####################################################################################
##########################      Terminou Laco While       ###########################
#####################################################################################
    print(t)
    print("O TEMPO DE SIMULACAO CHEGOU AO FIM!")
    print('                                 ')
 
######################################################################################
#########################     Variaveis de Interesse      ############################
######################################################################################
    #TEMPO DE ESPERA PARA SUBIR
    tempo_espera_subir = []
    for i in range(DIA):
        auxiliar = 0.0
        maximo = 0.0
        for j in range(len(ND_DIA[i])):
            valor = ( ND_DIA[i][j] - NA_DIA[i][j] )
            auxiliar += valor
            if( valor > maximo ):
                maximo = valor
        tempo_espera_subir.append(auxiliar / len(ND_DIA[i]))

    media_da_media_diaria_tempo = []
    for i in range(DIA):
        auxiliar = 0.0
        for j in range (i+1):
            auxiliar += tempo_espera_subir[j]
        media_da_media_diaria_tempo.append(auxiliar / (i+1) ) 
    
    tempo_espera_subir = media_da_media_diaria_tempo

    media_geral_tempo = 0
    for i in range(len(tempo_espera_subir)):
        media_geral_tempo += tempo_espera_subir[i]
    media_geral_tempo = media_geral_tempo / len(tempo_espera_subir)
    print("TEMPO DE ESPERA PARA SUBIR -- A media eh ", media_geral_tempo)

    desvio_padrao_tempo = 0
    for i in range(len(tempo_espera_subir)):
        desvio_padrao_tempo += (tempo_espera_subir[i] - media_geral_tempo)**2
    desvio_padrao_tempo = (desvio_padrao_tempo/len(tempo_espera_subir))**(0.5)
    print("TEMPO DE ESPERA PARA SUBIR -- O desvio padrao eh ", desvio_padrao_tempo)

    intervalo_menor_tempo = media_geral_tempo - 1.96*desvio_padrao_tempo/(len(tempo_espera_subir)**(0.5))
    intervalo_maior_tempo = media_geral_tempo + 1.96*desvio_padrao_tempo/(len(tempo_espera_subir)**(0.5))

    print("TEMPO DE ESPERA PARA SUBIR -- A extremidade inferior do intervalo de confianca eh ", intervalo_menor_tempo)
    print("TEMPO DE ESPERA PARA SUBIR -- A extremidade superior do intervalo de confianca eh ", intervalo_maior_tempo)
    print("                      ")

    #TAMANHO DA FILA PARA SUBIR
    aux_fila = []
    aux_tempo = []
    for i in range(DIA):
        for j in range(len(i_fila[i])):
            aux_fila.append(i_fila[i][j][1])
            aux_tempo.append(i_fila[i][j][0])
    
    for i in range(DIA):
        i_fila[i].append([M_DIA*(i+1), i_fila[i][len(i_fila[i])-1][1] ])

    media_tamanho_fila_subir_diaria = []
    for i in range(DIA):
        auxiliar = 0.0
        for j in range(len(i_fila[i])-1):
            if( (i_fila[i][j+1][0] - i_fila[i][j][0]) >= 0 ):
                auxiliar += (i_fila[i][j+1][0] - i_fila[i][j][0]) * i_fila[i][j][1]
            else:
                auxiliar += (i_fila[i][j][0]-i_fila[i][j+1][0]) * i_fila[i][j][1]
        tam = i_fila[i][len(i_fila[i])-1][0] - i_fila[i][0][0]
        media_tamanho_fila_subir_diaria.append( auxiliar / tam )

    media_da_media_diaria_fila = []
    for i in range(DIA):
        auxiliar = 0.0
        for j in range (i+1):
            auxiliar += media_tamanho_fila_subir_diaria[j]
        media_da_media_diaria_fila.append(auxiliar / (i+1))
    
    media_tamanho_fila_subir_diaria = media_da_media_diaria_fila

    media_geral_fila = 0
    for i in range(len(media_tamanho_fila_subir_diaria)):
        media_geral_fila += media_tamanho_fila_subir_diaria[i]
    media_geral_fila = media_geral_fila / len(media_tamanho_fila_subir_diaria)
    print("TAMANHO DA FILA DE ESPERA PARA SUBIR -- A media eh ", media_geral_fila)

    desvio_padrao_fila = 0
    for i in range(len(media_tamanho_fila_subir_diaria)):
        desvio_padrao_fila += (media_tamanho_fila_subir_diaria[i] - media_geral_fila)**2
    desvio_padrao_fila = (desvio_padrao_fila/len(media_tamanho_fila_subir_diaria))**(0.5)
    print("TAMANHO DA FILA DE ESPERA PARA SUBIR -- O desvio padrao eh ", desvio_padrao_fila)

    intervalo_menor_fila = media_geral_fila - 1.96*desvio_padrao_fila/(len(media_tamanho_fila_subir_diaria)**(0.5))
    intervalo_maior_fila = media_geral_fila + 1.96*desvio_padrao_fila/(len(media_tamanho_fila_subir_diaria)**(0.5))

    print("TAMANHO DA FILA DE ESPERA PARA SUBIR --  A extremidade inferior do intervalo de confianca eh ", intervalo_menor_fila)
    print("TAMANHO DA FILA DE ESPERA PARA SUBIR --  A extremidade superior do intervalo de confianca eh ", intervalo_maior_fila)

#####################################################################################
##############################     Extra      #######################################
#####################################################################################

    #UTILIZACAO DOS ELEVADORES PARA SUBIR
    UTILIZACAO_ELEVADOR = [0] *(N_ELEVADORES)
    for i in range(N_ELEVADORES):
        UTILIZACAO_ELEVADOR[i] = [0.0] * DIA

    for i in range(N_ELEVADORES):
        for j in range(DIA):
            for k in range(len(lotacao_elevador_subir[i][j])):
                UTILIZACAO_ELEVADOR[i][j] += lotacao_elevador_subir[i][j][k]
            UTILIZACAO_ELEVADOR[i][j] = float(UTILIZACAO_ELEVADOR[i][j] / len(lotacao_elevador_subir[i][j]))

#####################################################################################
############################     Graficos      ######################################
#####################################################################################

    x_data = [0]*DIA
    for i in range(DIA):
        x_data[i] = i+1

    fig = 0
    plt.figure(fig)
    plt.title('Media do Tempo de Espera Diario para Subir')
    plt.plot(x_data, media_da_media_diaria_tempo, 'o')
    plt.ylim(0, 2*max(media_da_media_diaria_tempo))
    plt.xlabel("Dia")
    plt.ylabel("Minuto")
    plt.grid()

    fig += 1
    plt.figure(fig)
    plt.title('Media do Tamanho Diario da Fila para Subir')
    plt.plot(x_data, media_tamanho_fila_subir_diaria, 'o')
    plt.ylim(0, 2*max(media_tamanho_fila_subir_diaria))
    plt.xlabel("Dia")
    plt.ylabel("Tamanho da Fila")
    plt.grid()
    
    fig += 1
    plt.figure(fig)
    for i in range(N_ELEVADORES):
        plt.plot(UTILIZACAO_ELEVADOR[i], label = 'Elevador %i' %(i+1))
    plt.legend()
    plt.title('Lotacao de Elevadores Diaria')
    plt.xlabel("Dia")
    plt.ylabel("Passageiro")
    plt.grid()
    
    plt.show()

#####################################################################################
#######################     INICIAR SIMULACAO      ##################################
#####################################################################################
if __name__ == "__main__":
    main()