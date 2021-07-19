import numpy as np
import cv2
import time
import sys

#Aplica filtros na imagem monocromatica. Passe como argumento de linha de comando o nome/diretorio da imagem
#e o filtro que será aplicado (h[1-9] e h[12](combinação h1 + h2)), ex: baboon.png h1

def convolucao(imagem, kernel):
  n, _ = kernel.shape
  lin, col = imagem.shape
  lin = (lin - n) + 1
  col = (col - n) + 1
  nova_imagem = np.zeros(imagem.shape)
  for row in range(lin):
    for column in range(col):
      nova_imagem[row][column] = (np.sum(imagem[row:row+n,column:column+n]*kernel))
  return nova_imagem

def escolher_filtro(nome_filtro):
    h1 = np.array([[-1 ,0 ,1],[-2 ,0, 2], [-1 ,0 ,1]])
    h2 = np.array([[-1 ,-2 ,-1],[0 ,0 ,0],[1 ,2 ,1]])
    h3 = np.array([[-1 ,-1 ,-1],[-1 ,8 ,-1],[-1 ,-1 ,-1]])
    h4 = np.array([[1, 1, 1],[1, 1, 1],[1 ,1, 1]])*(1/9)
    h5 = np.array([[-1, -1, 2],[-1, 2, -1],[2, -1, -1]])
    h6 = np.array([[2, -1, -1],[-1, 2, -1],[-1, -1, 2]])
    h7 = np.array([[0, 0, 1],[0, 0, 0],[-1, 0, 0]])
    h8 = np.array([[0, 0, -1, 0, 0],[0, -1, -2, -1, 0],[-1, -2, 16, -2, -1],[0, -1, -2, -1, 0],[0, 0, -1, 0, 0]])
    h9 = np.array([[1, 4, 6, 4, 1],[4, 16, 24, 16, 4],[6, 24, 36, 24, 6],[4, 16, 24, 16, 4],[1, 4, 6, 4, 1]])*(1/256)
    filtros={
        "h1" : h1, "h2" : h2, "h3" : h3,"h4" : h4, "h5" : h5, "h6" : h6, "h7" : h7, "h8" : h8, "h9" : h9
    }
    return filtros.get(nome_filtro)

if __name__ == "__main__":
    if(len(sys.argv) < 3):
        print("Parametros insuficientes. Passe o diretorio/nome da imagem e o filtro a ser aplicado. Ex: baboon.png h1")
    else:
        img = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)
        if(sys.argv[2] == "h12"):
            img1 = convolucao(img, escolher_filtro("h1"))
            img2 = convolucao(img, escolher_filtro("h2"))
            nova_imagem = np.sqrt(np.add(np.power(img1,2), np.power(img2,2)))
        else:
            nova_imagem = convolucao(img, escolher_filtro(sys.argv[2]))
        sys.argv[1] = sys.argv[1].replace('.png', '')
        cv2.imwrite(f'{sys.argv[1]}_filtro_{sys.argv[2]}.png', nova_imagem)