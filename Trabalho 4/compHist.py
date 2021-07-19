import sys
import cv2
import numpy as np
from skimage import feature

def compareHistChiSqr(image1, image2):
  lbp = feature.local_binary_pattern(image1, 8, 1)
  lbp = np.float32(lbp)
  lbp_hist = cv2.calcHist([lbp],[0],None,[256],(0,256))
  lbp_hist /= lbp_hist.sum() + 1e-9

  lbp2 = feature.local_binary_pattern(image2, 8, 1)
  lbp2 = np.float32(lbp2)
  lbp2_hist = cv2.calcHist([lbp2],[0],None,[256],(0,256))
  lbp2_hist /= lbp2_hist.sum() + 1e-9

  return cv2.compareHist(lbp_hist, lbp2_hist, cv2.HISTCMP_CHISQR)

if __name__ == "__main__":
    if(len(sys.argv) < 3):
        print("Parametros passados insuficientes, passe o diretorio das duas imagens.\n")
        sys.exit()
    img = cv2.imread(sys.argv[1], cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(sys.argv[2], cv2.IMREAD_GRAYSCALE)
    sys.argv[1] = sys.argv[1].replace('.png', '')
    sys.argv[2] = sys.argv[2].replace('.png', '')
    comp = compareHistChiSqr(img,img2)
    info = f"Medida Chi-Quadrado entre os histogramas das texturas: {sys.argv[1]} vs {sys.argv[2]} é:\t{comp}\n"
    with open("comparacoes_Histogramas.txt", 'a', encoding='utf-8') as escrita:
        escrita.writelines(info)