import numpy as np
import cv2
import time
import sys

#Transforma uma imagem colorida em grayscale. Passe como argumento de linha de comando o nome ou diretorio da imagem, ex: baboon.png

def convRGBtoMono_vetorizado(imagem):
  transformacao = np.array([0.1140, 0.5870, 0.2989])
  nova_imagem = np.einsum('ijl,l->ij', imagem, transformacao)
  nova_imagem[nova_imagem>255] = 255
  return nova_imagem

if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print("Parametros insuficientes. Passe o diretorio/nome da imagem. Ex: baboon.png")
    else:
        img = cv2.imread(sys.argv[1])
        nova_imagem = convRGBtoMono_vetorizado(img)
        sys.argv[1] = sys.argv[1].replace('.png', '')
        cv2.imwrite(f'{sys.argv[1]}_grayscale.png', nova_imagem)