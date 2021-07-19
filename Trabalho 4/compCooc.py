import sys
import cv2
import numpy as np
from skimage.feature import greycoprops, greycomatrix

def grayCoMatrix(img):
    gMatrix = greycomatrix(img, [1], [0, np.pi/2, np.pi/4, 3*np.pi/4], levels=256, normed=True)
    contraste = greycoprops(gMatrix, 'contrast')
    energia = greycoprops(gMatrix, 'energy')
    return contraste.mean(), energia.mean()

if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print("Parametros passados insuficientes, passe o diretorio da imagem.\n")
        sys.exit()
    img = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)
    img = np.array(img, dtype=np.uint8)
    contraste, energia = grayCoMatrix(img)
    sys.argv[1] = sys.argv[1].replace('.png', '')
    info = f"Medidas da Matriz de Coocorrencia da imagem {sys.argv[1]}: Contraste:{contraste}\tEnergia:{energia}\n"
    with open("comparacoes_Coocorrencia.txt", 'a', encoding='utf-8') as escrita:
        escrita.writelines(info)