import cv2
import numpy as np
import sys

#Comprime a imagem, recebe como parametro 'nome/diretorio da imagem' e 'Limiar de compressão' onde o limiar será
#o valor passado vezes o valor da mediana da imagem no dominio da frequencia.

def comprimir(img, limiar):
  fft_img = np.fft.fft2(img)
  limiar = limiar*np.median(np.abs(fft_img))
  limiar_app = np.abs(fft_img)>limiar
  cmp_img = np.multiply(fft_img, limiar_app)
  cmp_img = np.abs(np.fft.ifft2(cmp_img))
  return cmp_img

if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print("Parametros passados insuficientes, passe o diretorio da imagem.\n")
    if(len(sys.argv) < 3):
        print("Parametros insuficientes. Nao foi passado o valor do limiar, usando valor default Limiar = 30\n")
        img = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)
        img_cmp = comprimir(img, 30)
        cv2.imwrite(f'{sys.argv[1]}_comprimida30.png', img_cmp)
    else:
        img = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)
        img_cmp = comprimir(img, int(sys.argv[2]))
        cv2.imwrite(f'{sys.argv[1]}_comprimida{int(sys.argv[2])}.png', img_cmp)