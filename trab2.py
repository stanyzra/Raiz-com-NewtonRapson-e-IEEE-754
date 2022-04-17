# -*- coding: utf-8 -*-
import math

def newtonRapsonMethod(function, funcDeriv, x0, tol) :
    if abs(function(x0)) < tol: # Pega o valor absoluto da função e compara com o nível de tolerancia
        return x0
    else:
        return newtonRapsonMethod(function, funcDeriv, x0 - function(x0)/funcDeriv(x0), tol) # Chama recursivamente a função
    
def binaryAppend(string, binaryList):
    for i in range(len(binaryList)):
        string += str(binaryList[i])
    return string

def binaryTransform(x):
    # pos 0: float | pos 1: int
    numberParts = math.modf(x)
    floatPart = numberParts[0]
    intPart = int(numberParts[1])
    intList = []
    floatList = []
    
    # Verifica se a parte fracionaria é diferente de 0
    if floatPart != 0: 
        # Esquema de multiplicações sucessivas
        result = floatPart
        while(True):
            if result >= 1:
                if result - 1 == 0:
                    break
                else:
                    # Pega só a parte fracionaria
                    result = result%1
            result = result*2
            resultParts = math.modf(result)
            # Pegando o binário da parte float
            floatList.append(int(resultParts[1]))
            
    # Esquema de divisões sucessivas
    while(True):
        if intPart == 1 or intPart == 0:
            intList.append(intPart)
            break
        rest = intPart % 2
        intPart = math.floor(intPart/2)
        intList.append(rest)
        
    intList.reverse()
    binary = ''
    
    # Pega todos os valores inteiros do binario e joga em binary
    binary = binaryAppend(binary, intList)

    # Verifica se o valor digitado era float ou não. Se for, atribui um '.' no final da parte inteira
    if floatList != []:
        binary += '.'
    
    # Pega todos os valores fracionarios do binario e joga em binary
    binary = binaryAppend(binary, floatList)
    return binary
       
def notationTransform(x):
    binaryList = []
    pointerPos = x.find('.')
    for i in x:
        binaryList.append(i)
    # Realiza shift para a esquerda
    binary = ''
    if float(binaryList[0]) == 1:
        if pointerPos == -1:
            if len(binaryList) != 1:
                binaryList.insert(1, '.')
            if len(binaryList) == 1: # Trata o caso de raíz de 1
                binary = binaryAppend(binary, binaryList) + ' * 2^{}'.format(len(binaryList)-1)
                return binary
            else:
                binary = binaryAppend(binary, binaryList) + ' * 2^{}'.format(len(binaryList)-2)
                return binary
        else:
            binaryList.pop(pointerPos)
            binaryList.insert(1, '.')
            binary = binaryAppend(binary, binaryList) + ' * 2^{}'.format(pointerPos-1)
            return binary
    # Realiza shift para a direita
    else: 
        firstOneBinaryPos = x.find('1')
        binaryList.pop(pointerPos)
        binaryList.insert(firstOneBinaryPos, '.')
        
        for i in range(firstOneBinaryPos-1):
            binaryList.pop(0)
            
        binary = binaryAppend(binary, binaryList) + ' * 2^{}'.format(pointerPos - firstOneBinaryPos)
        return binary
            
def I3ETransform(x):
    x = x.replace(" ", "") # tira os espaços
    signalBit = 0 # 0 pois raiz não tem negativo
    bias = 1023 # usando arquitetura 64bits
    lenExp = 11
    lenMantissa = 52
    
    binaryExpPos = x.find('^')+1 # Pega o valor do expoente
    expBits = int(x[binaryExpPos:])+bias # Soma o valor do expoente com o bias
    expBits = binaryTransform(expBits) # Transforma pra binário
    
    # Se não tiver 8 bits, fica colocando 0 no começo
    for i in range(lenExp - len(expBits)):
        expBits = '0'+expBits
        
    mantissaEndPos = x.find('*') # Acha a posição do final da mantissa
    mantissaBits = x[2:mantissaEndPos:]
    
    # Se não tiver 23 bits, fica colocando 0 no final
    for i in range(lenMantissa - len(mantissaBits)):
        mantissaBits = mantissaBits+'0' 
        
    print()
    print("Padrão da IEEE-754 (64-bits):\nbit de sinal|expoente+bias|mantissa")
    print()
    print("{}|{}|{}".format(signalBit, expBits, mantissaBits))
        
num = input('Informe o valor da raíz que deseja extrair: ')

if (float(num) < 0):
    print("Não é possível calcular o valor da raíz de: {}\nMotivo: não é possível extraír o valor de uma raíz negativa no conjunto dos reais"
          .format(num))

elif (float(num) != 0):    
    x0 = input('Informe o valor de x0 (chute inicial): ')
    if (float(x0) == 0):
            print("Não é possível utilizar x0 como 0\nMotivo: resultaria em divisão por 0 no cálculo do método de Newton Rapson")
    else:
        function = lambda x: x**2-float(num) # função para calcular a raiz
        derivFunction = lambda x: 2*x # derivada da função
        
        root = newtonRapsonMethod(function, derivFunction, float(x0), 1e-10) # Chama o método 
        rootWithPrecision = str(root) # Guarda o valor em outra varíavel pra printar com 10 casas decimais
        
        # Valor :12 pois tem os 2 iniciais que é a parte inteira e o '.' da string, então 10+2
        print("Raíz extraída de {} com x0 sendo {} (precisão de 10 casas decimais): {}"
              .format(num, x0, rootWithPrecision[:12])) 
        print()
        
        binary = binaryTransform(float(rootWithPrecision[:12]))
        
        binary = notationTransform(binary)
        print("Valor binário normalizado: {}".format(binary))
        I3ETransform(binary)
else: # Trata o valor 0 (Trivial)
    print("Raíz de 0: 0")