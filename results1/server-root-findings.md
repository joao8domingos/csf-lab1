# Findings — server-root exposure (SRV-01 .. SRV-03)

Artefactos: SRV-01 server.js | SRV-02 README.md | SRV-03 credentials.txt HTTP-403 response
Recolha: 2026-09-16T19:00:25Z .. 19:00:36Z (UTC), via curl
Proveniência: remoção de "index.html" do URL original expôs listagem de diretório em
https://fenix.dpss.inesc-id.pt/ (servida por serveIndex() — ver F-07)

---

## F-01 — Intenção maliciosa auto-declarada no código
OBSERVAÇÃO: server.js linha 7 — `process.env.PHISHING_PORT`.
INTERPRETAÇÃO: a variável do ambiente primária do servidor chama-se literalmente
PHISHING_PORT. O autor designou o próprio serviço como phishing.
CONFIANÇA: alta. Evidência direta, não circunstancial.

## F-02 — Mecanismo de captura de credenciais (lado servidor)
OBSERVAÇÃO: linhas 33-38 — handler POST /cas/login extrai req.body.username e
req.body.password e executa fs.appendFile para o ficheiro "credentials.txt" em __dirname.
INTERPRETAÇÃO: fecha o elo que a análise do index.html deixou em
aberto. O index.html provava que o formulário ENVIA para /cas/login; isto prova o que o
servidor FAZ com os dados: persiste-os em disco.
CORROBORAÇÃO: o atributo action="https://fenix.dpss.inesc-id.pt/cas/login" do index.html
corresponde exatamente à rota implementada. Os dois artefactos pertencem ao mesmo sistema.

## F-03 — Formato conhecido dos dados exfiltrados
OBSERVAÇÃO: a linha gravada é `[${timestamp}] Username: ${username}, Password: ${password}\n`
com timestamp = new Date().toISOString().
INTERPRETAÇÃO: conhecemos a estrutura exata do credentials.txt sem lhe aceder. O toISOString()
produz sempre UTC (sufixo Z), o que é relevante para reconstrução cronológica se o ficheiro
vier a ser obtido por via legal — não haverá ambiguidade de fuso horário.

## F-04 — Encobrimento pós-captura
OBSERVAÇÃO: linha 40 — res.redirect("https://fenix.tecnico.ulisboa.pt/").
INTERPRETAÇÃO: após capturar as credenciais, a vítima é reencaminhada para o Fénix REAL do
IST. A vítima percebe a experiência como um login bem-sucedido, reduzindo a probabilidade
de deteção e de reporte imediato. Explica por que só alguns destinatários reportaram.

## F-05 — Falsificação de fingerprint do servidor
OBSERVAÇÃO: linhas 13-14 definem Server: Apache/2.4.41 (Ubuntu) e X-Powered-By: PHP/7.4.3.
Tecnologia real: Node.js + Express. Headers HTTP observados na recolha (SRV-01a..03a):
Server: nginx/1.31.4 ; X-Powered-By: PHP/7.4.3.
INTERPRETAÇÃO: há uma dupla camada. A aplicação tenta passar-se por Apache/PHP; um proxy
reverso nginx à frente sobrepõe o header Server com o seu próprio valor, mas deixa passar
o X-Powered-By forjado. O disfarce é parcial e inconsistente.
RELEVÂNCIA: corrobora o CNAME reverse-proxy00.dpss.inesc-id.pt já documentado via DNS.
LIMITAÇÃO: nginx/1.31.4 é a versão do proxy da infraestrutura, não necessariamente
software controlado pelo autor do phishing.

## F-06 — Validação de que o código obtido é o código em execução
OBSERVAÇÃO: linhas 46-49 bloqueiam /credentials.txt e /var/log/credentials.log com HTTP 403.
O pedido real a /credentials.txt devolveu exatamente 403 Forbidden, corpo "Forbidden" (9 bytes).
INTERPRETAÇÃO: o comportamento observado corresponde precisamente às regras do código
descarregado. Isto estabelece que o server.js recolhido é o código efetivamente em execução,
e não um ficheiro isco ou uma versão desatualizada deixada no diretório.
CONFIANÇA: alta. É um teste comportamental, não apenas leitura de código.

## F-07 — Má configuração que expôs toda a evidência
OBSERVAÇÃO: linhas 71-72 —
  express.static(__dirname, { dotfiles: "allow", index: false })
  serveIndex(__dirname, { icons: true, hidden: true })
INTERPRETAÇÃO: o servidor publica a RAIZ INTEIRA do projeto com listagem de diretórios
ativa e servindo dotfiles. É esta configuração que expôs .git/, server.js, package.json,
.gitlab-ci.yml e a existência do credentials.txt. Foi o vetor da nossa recolha.
NOTA: o autor bloqueou explicitamente credentials.txt e node_modules, mas não o .git/ —
omissão que preserva potencialmente o histórico completo de desenvolvimento.

## F-08 — Segundo local de armazenamento de credenciais referenciado
OBSERVAÇÃO: linha 49 bloqueia o caminho /var/log/credentials.log.
CORRELAÇÃO: o robots.txt do site contém "Disallow: /var/".
INTERPRETAÇÃO: há indício de um segundo repositório de credenciais em /var/log/. O código
descarregado não escreve para esse caminho — apenas o bloqueia.
HIPÓTESE (inferencial): pode corresponder a uma versão anterior do servidor, a um mecanismo
de logging paralelo, ou a proteção preventiva. NÃO confirmado.
AÇÃO: recomendar preservação de /var/log/ no servidor junto do INESC-ID.

## F-09 — Nome de código do projeto (relevante para atribuição)
OBSERVAÇÃO: SRV-02 README.md, 46 bytes: "# peixinho" / "Fenix authentication frontend."
INTERPRETAÇÃO: "peixinho" é português para "pequeno peixe" — trocadilho direto com phishing.
Indica autor com domínio de português. A descrição "Fenix authentication frontend" assume
a função de réplica do portal de autenticação.
LIMITAÇÃO: um nome de projeto não identifica uma pessoa. Valor probatório indiciário,
a corroborar com metadados de autoria do .git/ (em análise por outro membro da equipa).

## F-10 — Estado do ficheiro de credenciais
OBSERVAÇÃO: SRV-03, 9 bytes, corpo "Forbidden", HTTP 403.
INTERPRETAÇÃO: a existência do credentials.txt está estabelecida (o código cria-o e
bloqueia-o), mas o conteúdo NÃO é recuperável remotamente por desenho.
IMPORTANTE: este artefacto é a resposta de bloqueio, NÃO o conteúdo do ficheiro. O nome
em disco reflete isso deliberadamente para não induzir em erro.
AÇÃO: obtenção do credentials.txt real requer acesso ao sistema de ficheiros do servidor,
via pedido formal ao INESC-ID / autoridade competente.

## F-11 — Esteganálise de texto: resultado negativo
OBSERVAÇÃO: os três artefactos terminam exatamente no conteúdo esperado, sem bytes
anexados após EOF. Os tamanhos em disco (2287 / 46 / 9 bytes) coincidem com o
Content-Length HTTP de cada resposta.
INTERPRETAÇÃO: não há dados ocultos, overlays nem conteúdo anexado nestes três ficheiros.
NOTA METODOLÓGICA: um resultado negativo é um resultado válido e fica documentado como tal.
EOF
