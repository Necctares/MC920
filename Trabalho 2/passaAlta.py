import cv2
import numpy as np
import sys

#Filtro passa alta, recebe como parametro 'nome/diretorio da imagem' e 'Raio do circulo central'

def passaAlta(img, raioDoCirculo):
    fft_img = np.fft.fft2(img)
    fft_img = np.fft.fftshift(fft_img)
    fft_espec = 20*np.log(np.abs(fft_img))
    centro_y, centro_x = int(img.shape[0]/2), int(img.shape[1]/2)
    circ = np.ones(img.shape)
    circ = cv2.circle(circ, (centro_x, centro_y), raioDoCirculo, 0, -1)
    fft_img = np.multiply(fft_img, circ)
    nucleo = np.multiply(fft_espec, circ)
    fft_img = np.fft.ifftshift(fft_img)
    img_filtrada = np.abs(np.fft.ifft2(fft_img))
    return img_filtrada, fft_espec, nucleo


if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print("Parametros passados insuficientes, passe o diretorio da imagem.\n")
    elif(len(sys.argv) < 3):
        print("Parametros passados insuficientes, utilizando os valores default para o raio, R = 25 pixels.\n")
        img = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)
        fft_img, fft_spec, nucleo = passaAlta(img, 25)
        sys.argv[1] = sys.argv[1].replace('.png', '')
        cv2.imwrite(f'{sys.argv[1]}_filtroPassaAltaRaio25.png', fft_img)
        cv2.imwrite(f'{sys.argv[1]}_espectroFourier.png', fft_spec)
        cv2.imwrite(f'{sys.argv[1]}_nucleoPassaAltaRaio25.png', nucleo)
    else:
        img = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)
        fft_img, fft_spec, nucleo = passaAlta(img, int(sys.argv[2]))
        sys.argv[1] = sys.argv[1].replace('.png', '')
        cv2.imwrite(f'{sys.argv[1]}_filtroPassaAltaRaio{int(sys.argv[2])}.png', fft_img)
        cv2.imwrite(f'{sys.argv[1]}_espectroFourier.png', fft_spec)
        cv2.imwrite(f'{sys.argv[1]}_nucleoPassaAltaRaio{int(sys.argv[2])}.png', nucleo)
