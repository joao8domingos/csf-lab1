# Findings — VID-01 / VID-01-A (embedded polyglot document)

Artefactos:
  VID-01   Grand Theft Auto VI Trailer 1.mp4 (polyglot ICO/PDF, 9,443,926 bytes)
           source: .git full-history, commit 95f15e90a4ab0df0bdbf514dc108a3b9fbf4ba9e, path Videos/
  VID-01-A embedded PDF, carved from VID-01 offset 27, 9,443,899 bytes
           sha256: 9b57779104798e600a0ae083d3de54c9db6f97982931028910bf8a40785225f3

## V-01 — Ficheiro portador é um poliglota, não um vídeo
OBSERVAÇÃO: `file` classifica o original como "data"; exiftool lê-o como ICO 256x256;
os últimos 64 bytes contêm estrutura terminal de PDF (endstream/endobj/startxref/%%EOF).
Magic bytes (offset 0): 00 00 01 00 (assinatura ICO). Offset 27: <!--%PDF-1.5.
INTERPRETAÇÃO: ficheiro construído deliberadamente como poliglota ICO/PDF, com nome de
vídeo popular como camuflagem social. Nenhuma ferramenta isolada o identifica corretamente;
só a combinação file+exiftool+hexdump revela a estrutura real.

## V-02 — PDF embebido é um documento real e legível
OBSERVAÇÃO: extração a partir do offset 27 produz um PDF válido, 5 páginas, A4,
Producer: xdvipdfmx (20240305), CreationDate: 30 Apr 2026 12:00:00 WEST.
Title: "Independent External Technical Assessment Report - Project AMELIA"
Doc ref: AMA20260041AI. Status: CONDITIONAL ACCEPTANCE. Anomalia referida: SEC014.
Sem anexos embebidos (pdfdetach -list: 0 embedded files). Sem JavaScript. Não encriptado.
INTERPRETAÇÃO: o nome do projeto "AMÉLIA/AMELIA" liga este documento diretamente ao
amelia.pdf dentro de myzip.zip (protegido por password, ainda não quebrada pelo colega).
HIPÓTESE (inferencial, a confirmar): pode ser uma versão relacionada, anterior, ou
complementar do mesmo documento — não está confirmado se é byte-idêntico ao amelia.pdf.
AÇÃO: comparar hash/conteúdo com amelia.pdf assim que este for desencriptado.

## V-03 — Autor/Creator do PDF em branco
OBSERVAÇÃO: pdfinfo reporta Author e Creator vazios; só Producer (xdvipdfmx) está preenchido.
INTERPRETAÇÃO: campos de atribuição direta foram removidos ou nunca preenchidos — não
fornece pista de autoria por esta via. O Producer indica que o PDF foi gerado via LaTeX/XeTeX
(xdvipdfmx é o backend do XeLaTeX), sugerindo produção "profissional"/documento formal,
não um simples print-to-PDF.

## V-04 — Estrutura interna ainda por resolver (pendente)
OBSERVAÇÃO: binwalk sobre o ficheiro original mostrou, dentro do range do obj 1 (o stream de
9.357.855 bytes que compõe quase todo o ficheiro): possível assinatura ftyp (offset ~260),
HTML legível (offset 97337-112469), e um PNG 600x527 (offset 112484) — todos ANTES do PDF
"visível" de 5 páginas (que só começa a construir-se a partir do offset 9357945).
INTERPRETAÇÃO: o PDF de 5 páginas que abrimos pode não ser todo o conteúdo escondido; o
stream do obj 1 é maior que o PDF visível e contém as outras camadas (HTML, PNG, possível MP4).
STATUS: pendente de extração e análise dedicada do stream do obj 1.

## V-05 — Camada HTML escondida com pistas de atribuição (RESOLVE V-04)
OBSERVAÇÃO: carve dos offsets 97337..112469 produz VID-01-B-hidden.html (15132 bytes), uma
página HTML "GTA VI leaks / Vice City Insider" com dois comentários HTML deliberados:
  1. "todo: clean up the dev auth tokens ... ask jason"
  2. "flag for staging access: TARGET_GTAVI_LEAK_DASHBOARD / key: vl-cty-gta6-2026"
INTERPRETAÇÃO: o nome "jason" reaparece (já visto no ecossistema do .git do atacante) e há
uma chave textual (vl-cty-gta6-2026). São artefactos de camuflagem/tema (GTA VI) que também
funcionam como pistas de atribuição por convergência de persona.
CONFIANÇA: média — os tokens são plausivelmente "chamariz" temático; o valor está na
recorrência do identificador "jason" cruzada com outras fontes.

## V-06 — PNG escondido, válido, não sendo o segredo-alvo
OBSERVAÇÃO: carve do offset 112484 até IEND (573330) produz VID-01-C-hidden.png, PNG válido
600x527 RGBA (~460 KB), coerente com o "Image Length: 460854" lido pelo exiftool no cabeçalho.
INTERPRETAÇÃO: camada de imagem embebida na estrutura do poliglota. Não analisada em
profundidade — ver V-07.

## V-07 — Determinação de âmbito (instructor scoping)
OBSERVAÇÃO: o docente confirmou que o segredo relevante deste artefacto é o PDF (VID-01-A,
relatório Project AMÉLIA) e que não é necessária análise adicional do portador.
DECISÃO: análise do VID-01 encerrada. VID-01-A registado como o segredo. VID-01-B e VID-01-C
preservados e registados como camadas do poliglota, sem investigação adicional.
LIMITAÇÃO: esta é uma decisão de âmbito, não uma prova de ausência de mais conteúdo; os
artefactos ficam preservados caso seja necessário reabrir.

## V-08 — Cross-check pendente (nota de limitação)
OBSERVAÇÃO: pesquisa em results/, commands.txt e commands-git.txt não encontrou nenhum
registo de hash SHA-256 do colega para "Grand Theft Auto VI Trailer 1.mp4".
LIMITAÇÃO: a confirmação cruzada e independente do hash de VID-01 fica pendente até o
colega disponibilizar o seu manifesto de hashes do .git full-history. A integridade da
CADEIA DE CUSTÓDIA PRÓPRIA está garantida (original vs. working copy: hash idêntico,
5d3b5f08f35c5d812e0f2c36d58c9c4f2a0b844e2e1f8bd5054a9bc54f8471ca), mas não há ainda uma
segunda fonte independente a confirmar o mesmo hash para o objeto extraído do .git.
AÇÃO: pedir ao colega o ficheiro de hashes do full-history extraction (referido no
commands-git.txt como full-history-hashes.txt) e reconciliar quando disponível.
