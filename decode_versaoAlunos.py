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
    tecla_list = {"1": [697,1206], "2": [697,1339], "3": [697,1477], "A": [697, 1633],
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
        
    for pico in valoresPico:

    #encontre na tabela duas frequencias proximas às frequencias de pico encontradas e descubra qual foi a tecla

    #print a tecla.
    
  
    ## Exibe gráficos
    plt.show()

if __name__ == "__main__":
    main()
