import cv2
import numpy as np
import sys

#Rotaciona a imagem em 45 graus e devolve seu espectro de fourier, recebe como parametro 'nome/diretorio da imagem'

def rotacionar(img, angulo):
  centro_y, centro_x = int(img.shape[0]/2), int(img.shape[1]/2)
  rotacional = cv2.getRotationMatrix2D((centro_x,centro_y), angulo, 0.7)
  img_rot = cv2.warpAffine(img, rotacional, img.shape)
  fft_espec = np.fft.fft2(img_rot)
  fft_espec = np.fft.fftshift(fft_espec)
  fft_espec = 20*np.log(np.abs(fft_espec))
  return img_rot, fft_espec

if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print("Parametros passados insuficientes, passe o diretorio da imagem.\n")
    else:
        img = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)
        img_rot, espec = rotacionar(img, 45)
        cv2.imwrite(f'{sys.argv[1]}_rotacionada45graus.png', img_rot)
        cv2.imwrite(f'{sys.argv[1]}_espectroFourierRotacionado45.png', espec)