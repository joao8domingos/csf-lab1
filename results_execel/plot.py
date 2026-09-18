import numpy as np
import pandas as pd
from PIL import Image
from skimage import color  # pip install scikit-image

# 1. Caminho do arquivo e leitura das abas
excel_file = "ESP32_ADXL345_3Axis_Telemetry.xlsx"

# Substitua pelos nomes exatos das suas abas (ou use sheet_name=0, 1, 2 para pegar por ordem)
sheet1 = pd.read_excel(excel_file, sheet_name=0, header=None).to_numpy(
    dtype=np.float32
)
sheet2 = pd.read_excel(excel_file, sheet_name=1, header=None).to_numpy(
    dtype=np.float32
)
sheet3 = pd.read_excel(excel_file, sheet_name=2, header=None).to_numpy(
    dtype=np.float32
)

# Confirme as dimensões (devem ser 400x302 ou 302x400)
print(f"Dimensões: Sheet1={sheet1.shape}")

# -------------------------------------------------------------
# Tratar como CIE L*a*b* (Mais provável pelo perfil dos dados)
# -------------------------------------------------------------
# Monta a matriz (altura, largura, 3)
lab_array = np.stack([sheet1, sheet2, sheet3], axis=-1)

# Converte de Lab para RGB padrão sRGB
try:
  # skimage espera L entre 0 e 100, e a/b tipicamente entre -128 e 127
  rgb_from_lab = color.lab2rgb(lab_array)
  # lab2rgb retorna float de 0.0 a 1.0; convertemos para 0 a 255
  rgb_from_lab_uint8 = np.clip(rgb_from_lab * 255, 0, 255).astype(np.uint8)

  img_lab = Image.fromarray(rgb_from_lab_uint8)
  img_lab.save("imagem_interpretada_lab.png")
  print("Imagem Lab salva: imagem_interpretada_lab.png")
except Exception as e:
  print(f"Erro na conversão Lab: {e}")

