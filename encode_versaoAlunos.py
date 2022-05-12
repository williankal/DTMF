
#importe as bibliotecas
from curses.ascii import FS
from suaBibSignal import *
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt

"""
A transformada de fourier(FFT) é utilizada para transformar um sinal digital no dominio do tempo, para um sinal com dominio na frequencia
No gráfico: x --> valores de frequencia de 0 a fs(no caso desse arquivo seria 44100 por segundo) | y --> amplitude
"""

#funções a serem utilizadas
def signal_handler(signal, frame):
        print('You pressed Ctrl+C!')
        sys.exit(0)

#converte intensidade em Db, caso queiram ...
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

#range de frequencias para gerar a senoide
def frequencies_list(tecla):
        list = {"1": [697,1206], "2": [697,1339], "3": [697,1477], "A": [697, 1633],
         "4": [770,1206], "5": [770,1339], "6": [770,1477], "B": [770, 1633],
         "7": [852,1206], "8": [852,1339], "9": [852,1477], "C": [852, 1633],
         "X": [941,1206], "0": [941,1339], "#": [941,1477], "D": [941, 1633]}   

        if tecla in list.keys():
            return list[tecla][0], list[tecla][1]

        else:
            print("-------------------------")
            print("A tecla não existe, tentar novamente")
            print("As únicas teclas possívesi são: 0 a 9, ou A,B,C,D,X,#:")
            exit()
            

def main():
    bibSignal = signalMeu()
    #********************************************instruções*********************************************** 
    # seu objetivo aqui é gerar duas senoides. Cada uma com frequencia corresposndente à tecla pressionada
    # então inicialmente peça ao usuário para digitar uma tecla do teclado numérico DTMF
    # agora, voce tem que gerar, por alguns segundos, suficiente para a outra aplicação gravar o audio, duas senoides com as frequencias corresposndentes à tecla pressionada, segundo a tabela DTMF
    # se voce quiser, pode usar a funcao de construção de senoides existente na biblioteca de apoio cedida. Para isso, você terá que entender como ela funciona e o que são os argumentos.
    # essas senoides tem que ter taxa de amostragem de 44100 amostras por segundo, entao voce tera que gerar uma lista de tempo correspondente a isso e entao gerar as senoides
    # lembre-se que a senoide pode ser construída com A*sin(2*pi*f*t)
    # o tamanho da lista tempo estará associada à duração do som. A intensidade é controlada pela constante A (amplitude da senoide). Seja razoável.
    # some as senoides. A soma será o sinal a ser emitido.
    # utilize a funcao da biblioteca sounddevice para reproduzir o som. Entenda seus argumento.
    # grave o som com seu celular ou qualquer outro microfone. Cuidado, algumas placas de som não gravam sons gerados por elas mesmas. (Isso evita microfonia).
    
    # construa o gráfico do sinal emitido e o gráfico da transformada de Fourier. Cuidado. Como as frequencias sao relativamente altas, voce deve plotar apenas alguns pontos (alguns periodos) para conseguirmos ver o sinal
    print("Inicializando encoder")

    print("Aguardando usuário")

    valor_selecionado = input("Escolha um número de 0 a 9, ou A,B,C,D,X,#: ")
    print("o valor selecionado foi: ", valor_selecionado)
    frequencia1 , frequencia2 = frequencies_list(valor_selecionado)

    print("-------------------------")
    fs  = 44100  # pontos por segundo (frequência de amostragem)
    A   = 1.5   # Amplitude
    F   = 1     # Hz
    T   = 4     # Tempo em que o seno será gerado
    t   = np.linspace(-T/2,T/2,T*fs)

    #generateSin returns (x,s) --> (?, senoide)
    x1, y1 = bibSignal.generateSin(frequencia1, A, T, fs)
    x2, y2 = bibSignal.generateSin(frequencia2, A, T, fs)

    #somar as senoides para geral o sinaly2
    xSinal = x1 + x2
    ySinal = y1 + y2

    print("Gerando Tom referente ao símbolo : {}".format(valor_selecionado))
    sd.play(ySinal, fs)

    print("Executando as senoides (emitindo o som)")

    #plt.plot(t,ySinal)
    plt.plot(t[:800], ySinal[:800])
    #plt.xlim(0.1, 0.2)
    plt.xlabel("Tempo")
    plt.ylabel("Frequencia")
    plt.title("Tempo x Frequencia Somada")

    bibSignal.plotFFT(ySinal, fs)
    # Exibe gráficos
    plt.show()
    # aguarda fim do audio
    sd.wait()

    plt.show()

if __name__ == "__main__":
    main()
