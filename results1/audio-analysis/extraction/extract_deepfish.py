#!/usr/bin/env python3
"""
Operation DeepFISH - extraccao da mensagem escondida em dj_cara_after_hours.wav

A mensagem esta pintada no espectrograma do sinal de diferenca estereo (L-R). Nao esta no LSB nem anexada ao chunk `data`.

Parametros medidos (nao assumidos):
  SHA-256   2b61eecffc5261dcc05d833c64454b42d33f445d3df09095988d0c2dbbc8753d
  formato   48 kHz, 16-bit, estereo, 672,13 s
  banda     19 685 - 21 545 Hz   (fora disto e' so' ruido de fundo)
  tempo     1,87 s -> ~421 s     (depois de ~425 s a energia cai ao piso de ruido)
  layout    9 "paginas" de 47,50 s; cada pagina tem linhas de texto EMPILHADAS
            em frequencia (6 nas paginas 0-4, 5 nas paginas 5-8), 79 caracteres
            por pagina -> 0,6013 s por caractere.
            Le-se cada pagina de cima para baixo, depois a pagina seguinte.

Uso:  python3 extract_deepfish.py dj_cara_after_hours.wav
Gera: paginas PNG legiveis em ./out/
"""
import sys, os, wave, hashlib
import numpy as np
from scipy import signal, ndimage
from PIL import Image

EXPECTED_SHA = "2b61eecffc5261dcc05d833c64454b42d33f445d3df09095988d0c2dbbc8753d"
P0, PER, NPAGES = 1.87, 47.50, 9
FMIN, FMAX = 19450, 21750

def check(path):
    h = hashlib.sha256(open(path, "rb").read()).hexdigest()
    print(f"SHA-256: {h}")
    if h != EXPECTED_SHA:
        sys.exit("ABORTADO: o hash nao corresponde ao objeto Git LFS original.")
    print("Integridade confirmada.\n")

def load_diff(path):
    w = wave.open(path)
    sr, n = w.getframerate(), w.getnframes()
    assert w.getnchannels() == 2 and w.getsampwidth() == 2
    a = np.frombuffer(w.readframes(n), dtype="<i2").reshape(-1, 2).astype(np.float64)
    print(f"{sr} Hz, {n} frames, {n/sr:.2f} s, estereo")
    return sr, a[:, 0] - a[:, 1]          # equivalente a: sox in.wav out.wav oops remix 1

def render(diff, sr, t0, t1, out, W=1900, H=740):
    """Espectrograma da banda ultrassonica, com a musica suprimida."""
    x = diff[int(t0*sr):int(t1*sr)]
    f, _, S = signal.stft(x, fs=sr, nperseg=8192, noverlap=8192-96,
                          boundary=None, padded=False)
    D = 20*np.log10(np.abs(S) + 1e-6)
    D -= np.median(D, axis=0, keepdims=True)      
    D = D[(f >= FMIN) & (f <= FMAX)]
    win = int(1.5*sr/96)                          
    hi = ndimage.uniform_filter1d(np.percentile(D, 90, axis=0), win, mode="nearest")
    lo = ndimage.uniform_filter1d(np.percentile(D, 15, axis=0), win, mode="nearest")
    N = ndimage.gaussian_filter(np.clip((D-lo)/np.maximum(hi-lo, 3.0), 0, 1), (0.8, 1.0))
    img = (255*(1-N)).astype(np.uint8)[::-1]
    Image.fromarray(img).resize((W, H), Image.LANCZOS).save(out)

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "dj_cara_after_hours.wav"
    check(path)
    sr, diff = load_diff(path)
    os.makedirs("out", exist_ok=True)
    for p in range(NPAGES):
        t0 = P0 + PER*p
        mid = t0 + PER/2
        render(diff, sr, t0-0.3,  mid+0.8,       f"out/pagina{p}_esq.png")
        render(diff, sr, mid-0.8, t0+PER+0.8,    f"out/pagina{p}_dir.png")
        print(f"pagina {p}: {t0:7.2f} - {t0+PER:7.2f} s")
    print("\nImagens em ./out/ - ler cada pagina de cima para baixo.")

if __name__ == "__main__":
    main()
