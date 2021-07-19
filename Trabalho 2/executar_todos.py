import comprimir as cmp
import rotacionar as rot
import passaBaixa as pb
import passaFaixa as pf
import passaAlta as pa
import sys
import cv2

#Arquivo para executar de uma vez só todas as operações.
#Recebe como argumentos: 'nome da imagem/diretorio', 'raioDoCircFiltroPassaAlta', 'raioDoCircFiltroPassaBaixa',
#'raioCircFreqMaxFiltroPassaFaixa', 'raioCircFreqMinFiltroPassaFaixa' e 'limiarDeCompressao'.
#Ex: python3 executar_todos.py baboon.png 50 25 100 30 40
#Teremos a aplicação de um filtro passa alta com circulo central de raio 50 pixels, passa baixa: 25 pixels,
#passa faixa, anel: 30 pixels até 100 a partir do centro, e limiar de compressão (limiar*mediana da imagem) de 40.

if __name__ == "__main__":
    if(len(sys.argv) < 2):
        print("Parametros passados insuficientes, passe o diretorio da imagem.\n")
    elif(len(sys.argv) < 7):
        print("Parametros passados insuficientes, utilizando os valores default para todas as funcoes.\n")
        img = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)

        fft_img, fft_spec, nucleo = pa.passaAlta(img, 25)
        sys.argv[1] = sys.argv[1].replace('.png', '')
        cv2.imwrite(f'{sys.argv[1]}_filtroPassaAltaRaio25.png', fft_img)
        cv2.imwrite(f'{sys.argv[1]}_espectroFourier.png', fft_spec)
        cv2.imwrite(f'{sys.argv[1]}_nucleoPassaAltaRaio25.png', nucleo)

        fft_img, fft_spec, nucleo = pb.passaBaixa(img, 25)
        cv2.imwrite(f'{sys.argv[1]}_filtroPassaBaixaRaio25.png', fft_img)
        cv2.imwrite(f'{sys.argv[1]}_nucleoPassaBaixaRaio25.png', nucleo)

        fft_img, fft_spec, nucleo = pf.passaFaixa(img, 50, 10)
        cv2.imwrite(f'{sys.argv[1]}_filtroPassaFaixaRaio50ate10.png', fft_img)
        cv2.imwrite(f'{sys.argv[1]}_nucleoPassaFaixaRaio50ate10.png', nucleo)

        img_rot, espec = rot.rotacionar(img, 45)
        cv2.imwrite(f'{sys.argv[1]}_rotacionada45graus.png', img_rot)
        cv2.imwrite(f'{sys.argv[1]}_espectroFourierRotacionado45.png', espec)

        img_cmp = cmp.comprimir(img, 30)
        cv2.imwrite(f'{sys.argv[1]}_comprimida30.png', img_cmp)
    else:
        img = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)

        fft_img, fft_spec, nucleo = pa.passaAlta(img, int(sys.argv[2]))
        sys.argv[1] = sys.argv[1].replace('.png', '')
        cv2.imwrite(
            f'{sys.argv[1]}_filtroPassaAltaRaio{int(sys.argv[2])}.png', fft_img)
        cv2.imwrite(f'{sys.argv[1]}_espectroFourier.png', fft_spec)
        cv2.imwrite(
            f'{sys.argv[1]}_nucleoPassaAltaRaio{int(sys.argv[2])}.png', nucleo)

        fft_img, fft_spec, nucleo = pb.passaBaixa(img, int(sys.argv[3]))
        cv2.imwrite(
            f'{sys.argv[1]}_filtroPassaBaixaRaio{int(sys.argv[3])}.png', fft_img)
        cv2.imwrite(
            f'{sys.argv[1]}_nucleoPassaBaixaRaio{int(sys.argv[3])}.png', nucleo)

        fft_img, fft_spec, nucleo = pf.passaFaixa(
            img, int(sys.argv[4]), int(sys.argv[5]))
        cv2.imwrite(
            f'{sys.argv[1]}_filtroPassaFaixaRaio{int(sys.argv[4])}ate{int(sys.argv[5])}.png', fft_img)
        cv2.imwrite(
            f'{sys.argv[1]}_espectroFourier.png', fft_spec)
        cv2.imwrite(
            f'{sys.argv[1]}_nucleoPassaFaixaRaio{int(sys.argv[4])}ate{int(sys.argv[5])}.png', nucleo)

        img_rot, espec = rot.rotacionar(img, 45)
        cv2.imwrite(f'{sys.argv[1]}_rotacionada45graus.png', img_rot)
        cv2.imwrite(f'{sys.argv[1]}_espectroFourierRotacionado45.png', espec)

        img_cmp = cmp.comprimir(img, int(sys.argv[6]))
        cv2.imwrite(f'{sys.argv[1]}_comprimida{int(sys.argv[6])}.png', img_cmp)
