import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage import feature

def lbp(image, num_vizinhos, raio):
  lbp = feature.local_binary_pattern(image, num_vizinhos, raio)
  lbp = np.float32(lbp)
  lbp_hist = cv2.calcHist([lbp],[0],None,[256],(0,256))
  lbp_hist /= lbp_hist.sum() + 1e-9
  return lbp, lbp_hist

if __name__ == "__main__":
    numero_de_vizinhos = 8
    raio_do_circulo = 1
    if(len(sys.argv) < 2):
        print("Parametros passados insuficientes, passe o diretorio da imagem.\n")
        sys.exit()
    if len(sys.argv) >= 3:
        numero_de_vizinhos = int(sys.argv[2])
    if len(sys.argv) >= 4:
        raio_do_circulo = int(sys.argv[3])

    img = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)
    lbp_img, lbp_hist = lbp(img, numero_de_vizinhos, raio_do_circulo)
    sys.argv[1] = sys.argv[1].replace('.png', '')
    cv2.imwrite(f'{sys.argv[1]}_LBP_{numero_de_vizinhos}_{raio_do_circulo}.png', lbp_img)
    plt.title(f"Histograma da imagem: {sys.argv[1]}_LBP_{numero_de_vizinhos}_{raio_do_circulo}.png")
    plt.xlabel("Valor do Pixel")
    plt.ylabel("% de Pixels")
    plt.plot(lbp_hist)
    plt.savefig(f"{sys.argv[1]}_LBP_Histograma_{numero_de_vizinhos}_{raio_do_circulo}.png")