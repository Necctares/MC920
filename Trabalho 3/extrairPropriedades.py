import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt

#Extrai contornos da imagem e calcula algumas propriedades de cada contorno como area, perimetro, excentricidade e solidez.
#Recebe como parametro 'nome/diretorio da imagem' e (opcional) 'Limiar da imagem tons de cinza' (0-255) onde
#Pixels com valores abaixo desse limiar serão setados para 0 (preto)

def pegarContorno(img, limiar):
    thresh_img = img
    thresh_img[thresh_img < limiar] = 0
    contorno, _ = cv2.findContours(
        thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    img_contorno = np.ones(img.shape+(3,))*255
    cv2.drawContours(img_contorno, contorno[1:], -1, (0, 0, 255), 2)
    return img_contorno, thresh_img, contorno


def calcularExcentricidade(momento):
    p1 = (momento['mu20'] + momento['mu02']) / 2
    p2 = np.sqrt(4 * momento['mu11']**2 +
                 (momento['mu20'] - momento['mu02'])**2) / 2
    eixo_menor = p1-p2
    eixo_maior = p1+p2
    return np.sqrt(1-(eixo_menor / eixo_maior))


def extrairPropriedades(contorno, img_contorno):
    i = 1
    # Cores para preenchimento das areas dos contornos
    cores = [(204, 204, 255), (204, 229, 255), (204, 255, 255), (204, 255, 229), (204, 255, 204),
             (229, 255, 204), (255, 255, 204), (255, 229, 204), (255, 204, 229), (229, 204, 255)]

    # Armazena as informações extraidas
    info = [f'Numero de regiões: {len(contorno)-1}\n\n']
    areas = []
    obj_pequeno = 0
    obj_medio = 0
    obj_grande = 0

    for cnt_atual in contorno[1:]:
        # Calculo da Area e perimetro
        area = cv2.contourArea(cnt_atual)
        areas.append(area)
        perimetro = cv2.arcLength(cnt_atual, True)

        # Calculo da excentricidade
        momento = cv2.moments(cnt_atual)
        excentricidade = calcularExcentricidade(momento)

        # Calculo da solidez
        casca = cv2.convexHull(cnt_atual)
        areaDaCasca = cv2.contourArea(casca)
        solidez = area/areaDaCasca

        # Salva informação atual
        info_atual = f'Região: {i-1}\tárea: {area}\tperímetro: {perimetro}\texcentricidade: {excentricidade}\tsolidez: {solidez}\n'
        info.append(info_atual)

        # Pega o centroide do contorno
        cx = int(momento['m10']/momento['m00'])
        cy = int(momento['m01']/momento['m00'])
        # Preenche o contorno
        cv2.drawContours(img_contorno, contorno, i, cores[i % len(cores)], -1)
        # Escreve a sua respectiva numeração
        cv2.putText(img_contorno, str(i-1), (cx, cy),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0))
        i += 1
        if area < 1500:
            obj_pequeno += 1
        elif area >= 1500 and area < 3000:
            obj_medio += 1
        else:
            obj_grande += 1
    # Termina de armazenar as informações necessarias
    info_atual = f'\nNúmero de regiões pequenas: {obj_pequeno}\n'
    info.append(info_atual)
    info_atual = f'\nNúmero de regiões medias: {obj_medio}\n'
    info.append(info_atual)
    info_atual = f'\nNúmero de regiões grandes: {obj_grande}\n'
    info.append(info_atual)

    # Salva as informações extraidas em um arquivo txt
    with open(f'{sys.argv[1]}_infoExtraida.txt', 'w', encoding='utf-8') as escrita:
        escrita.writelines(info)
    print("Informações extraidas, plotando histograma...")
    # Plota o histograma
    plt.hist(areas, bins=[0, 1500, 3000, max(
        max(areas), 4500)], color='crimson', lw=2, ec='black')
    plt.ylabel('Numero de Objetos')
    plt.xlabel('Área')
    plt.title('Histograma de areas dos objetos')
    plt.savefig(f'{sys.argv[1]}_Histograma.png')
    return


if __name__ == "__main__":
    limiar = 255
    if(len(sys.argv) < 2):
        print("Parametros passados insuficientes, passe o diretorio da imagem.\n")
        sys.exit()
    if(len(sys.argv) >= 3):
        limiar = int(sys.argv[2])

    # Carrega a imagem em tons de cinza
    img = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)
    cv2.imwrite(f'{sys.argv[1]}_Grayscale.png', img)

    # Chama função para pegar o contorno
    print("Extraindo contorno...")
    img_cnt, img_limiar, contorno = pegarContorno(img, limiar)
    cv2.imwrite(f'{sys.argv[1]}_Contorno.png', img_cnt)
    cv2.imwrite(f'{sys.argv[1]}_ComLimiar.png', img_limiar)

    # Extrai as propriedades da imagem
    print("Extraindo informações")
    imgc = np.ones(img.shape+(3,))*255
    extrairPropriedades(contorno, imgc)
    cv2.imwrite(f'{sys.argv[1]}_ContornoPreenchido.png', imgc)
