import cv2
import numpy as np
import sys

# Filtro passa faixa, recebe como parametro 'nome/diretorio da imagem', 'Limite Max do Raio de Frequencia', 'Limite Min do Raio de Freq.'


def passaFaixa(img, raioFaixaMax, raioFaixaMin):
    fft_img = np.fft.fft2(img)
    fft_img = np.fft.fftshift(fft_img)
    fft_espec = 20*np.log(np.abs(fft_img))
    centro_y, centro_x = int(img.shape[0]/2), int(img.shape[1]/2)
    circMax = np.zeros(img.shape)
    circMax = cv2.circle(circMax, (centro_x, centro_y), raioFaixaMax, 1, -1)
    circMin = np.ones(img.shape)
    circMin = cv2.circle(circMin, (centro_x, centro_y), raioFaixaMin, 0, -1)
    circ = np.multiply(circMin, circMax)
    fft_img = np.multiply(fft_img, circ)
    nucleo = np.multiply(fft_espec, circ)
    fft_img = np.fft.ifftshift(fft_img)
    img_filtrada = np.abs(np.fft.ifft2(fft_img))
    return img_filtrada, fft_espec, nucleo


if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print("Parametros passados insuficientes, passe o diretorio da imagem.\n")
    elif(len(sys.argv) < 4):
        print("Parametros passados insuficientes, utilizando os valores default para o raio externo, R = 50, raio interno, R = 10 pixels.\n")
        img = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)
        fft_img, fft_spec, nucleo = passaFaixa(img, 50, 10)
        sys.argv[1] = sys.argv[1].replace('.png', '')
        cv2.imwrite(f'{sys.argv[1]}_filtroPassaFaixaRaio50ate10.png', fft_img)
        cv2.imwrite(f'{sys.argv[1]}_espectroFourier.png', fft_spec)
        cv2.imwrite(f'{sys.argv[1]}_nucleoPassaFaixaRaio50ate10.png', nucleo)
    else:
        img = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)
        fft_img, fft_spec, nucleo = passaFaixa(
            img, int(sys.argv[2]), int(sys.argv[3]))
        sys.argv[1] = sys.argv[1].replace('.png', '')
        cv2.imwrite(
            f'{sys.argv[1]}_filtroPassaFaixaRaio{int(sys.argv[2])}ate{int(sys.argv[3])}.png', fft_img)
        cv2.imwrite(
            f'{sys.argv[1]}_espectroFourier.png', fft_spec)
        cv2.imwrite(
            f'{sys.argv[1]}_nucleoPassaFaixaRaio{int(sys.argv[2])}ate{int(sys.argv[3])}.png', nucleo)
