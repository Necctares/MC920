import numpy as np
import cv2
import time
import sys

#Aplica um efeito na imagem colorida. Passe como argumento de linha de comando o nome ou diretorio da imagem, ex: baboon.png

def novoRGB_vetorizado(imagem):
  nova_imagem = np.zeros(imagem.shape)
  rgb = np.array([[0.131,0.534,0.272],[0.168,0.686,0.349],[0.189,0.769,0.393]])
  nova_imagem = np.einsum('ijk,lk->ijl', imagem, rgb)
  nova_imagem[nova_imagem>255]=255
  return nova_imagem

if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print("Parametros insuficientes. Passe o diretorio/nome da imagem. Ex: baboon.png")
    else:
        img = cv2.imread(sys.argv[1])
        nova_imagem = novoRGB_vetorizado(img)
        sys.argv[1] = sys.argv[1].replace('.png', '')
        cv2.imwrite(f'{sys.argv[1]}_novoRGB.png', nova_imagem)