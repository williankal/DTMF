#!/usr/bin/env python3
"""Show a text-mode spectrogram using live microphone data."""

#Importe todas as bibliotecas
from curses.ascii import FS
from tempfile import TemporaryDirectory
from suaBibSignal import *
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time
import peakutils

#funcao para transformas intensidade acustica em dB
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)


def main():
    tecla_dict = {"1": [697,1206], "2": [697,1339], "3": [697,1477], "A": [697, 1633],
         "4": [770,1206], "5": [770,1339], "6": [770,1477], "B": [770, 1633],
         "7": [852,1206], "8": [852,1339], "9": [852,1477], "C": [852, 1633],
         "X": [941,1206], "0": [941,1339], "#": [941,1477], "D": [941, 1633]} 


    #declare um objeto da classe da sua biblioteca de apoio (cedida)   
    bibSignal = signalMeu()
 
    #declare uma variavel com a frequencia de amostragem, sendo 44100
    fs  = 44100  # pontos por segundo (frequência de amostragem)
    A   = 1.5   # Amplitude
    F   = 1     # Hz
    T   = 3    # Tempo em que o seno será gerado
    #voce importou a bilioteca sounddevice como, por exemplo, sd. entao
    # os seguintes parametros devem ser setados:
    
    sd.default.samplerate = fs #taxa de amostragem
    linha = 0
    coluna = 0


    sd.default.channels = 2  #voce pode ter que alterar isso dependendo da sua placa



    duration = 3 #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic


    # faca um printo na tela dizendo que a captacao comecará em n segundos. e entao 
    print("Captação de som começara em apenas 3 segundos....")
    time.sleep(3)
    #use um time.sleep para a espera
   
   #faca um print informando que a gravacao foi inicializada
    print("-------------------------")
    print("Gravação iniciada")
    print("-------------------------")

   
   #declare uma variavel "duracao" com a duracao em segundos da gravacao. poucos segundos ... 

   #calcule o numero de amostras "numAmostras" que serao feitas (numero de aquisicoes)
    numAmostras = fs * duration
    freqDeAmostragem = fs

    audio = sd.rec(int(numAmostras), freqDeAmostragem, channels=1)
    sd.wait()
    print("...     FIM")
    
    #analise sua variavel "audio". pode ser um vetor com 1 ou 2 colunas, lista ...
    #grave uma variavel com apenas a parte que interessa (dados)
    

    # use a funcao linspace e crie o vetor tempo. Um instante correspondente a cada amostra!
    t   = np.linspace(-duration / 2, duration / 2, duration * fs)

    # plot do gravico  áudio vs tempo!
    plt.plot(t, audio[:,0])
    plt.xlabel("Tempo")
    plt.ylabel("Audio")
    
    ## Calcula e exibe o Fourier do sinal audio. como saida tem-se a amplitude e as frequencias
    xf, yf = bibSignal.calcFFT(audio[:,0], fs)

    plt.figure("F(y)")
    plt.plot(xf,yf)
    plt.grid()
    plt.title('Fourier audio')
   
    index = peakutils.indexes(yf, thres = 0.3 , min_dist = 100) #encontra apenas as posições dos picos no vetor não a frequencia
    #peakutils.indexes --> Finds the numeric index of the peaks in y by taking its first order difference. 
    #By using thres and min_dist parameters, it ispossible to reduce the number of detected peaks. y must be signed.
    
    #printe os picos encontrados! 
    print("As posicões dos picos são: ", index)
    valoresPico=[]
    for freq in xf[index]:
        print("freq de pico sao {}" .format(freq))
        valoresPico.append(freq)

    tolerancia = 15

    rangeFrequenciasMin = [697, 770, 852, 941] 
    rangeFrequenciasMax = [1206, 1339, 1477, 1633]
    print(valoresPico)
    for pico in valoresPico:
        for value in rangeFrequenciasMin:
            if value-tolerancia < pico < value + tolerancia:
                linha = value
        for value2 in rangeFrequenciasMax:
            if value2-tolerancia < pico < value2 + tolerancia:
                coluna = value2

    #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla
    
    print("Valores de frequencia encontrados: ", coluna)
    print(linha)
    
    key_list = list(tecla_dict.keys())
    val_list = list(tecla_dict.values())

    posicao = val_list.index([linha,coluna])
    print("A tecla selecionada foi: ", key_list[posicao])

    x1, y1 = bibSignal.generateSin(linha, A, T, fs)
    x2, y2 = bibSignal.generateSin(coluna, A, T, fs)
    xSinal = x1 + x2
    ySinal = y1 + y2

    plt.plot(t[:800], ySinal[:800])
    #plt.xlim(0.1, 0.2)
    plt.xlabel("Tempo")
    plt.ylabel("Frequencia")
    plt.title("Tempo x Frequencia Somada")
    bibSignal.plotFFT(ySinal, fs)

    
    ## Exibe gráficos
    plt.show()

if __name__ == "__main__":
    main()
