> NOTA: esta transcrição parcial foi SUPERADA pela transcrição completa e validada em artifacts/audio-extracted/AUD-01-B-hidden-code.diff (ver audio-findings.md, A-03 e A-07). Mantida aqui apenas como registo do processo incremental de descoberta.

# AUD-01 — Mensagem escondida no espectrograma (diferença estéreo L-R)
# dj_cara_after_hours.wav | sha256 2b61eecffc5261dcc05d833c64454b42d33f445d3df09095988d0c2dbbc8753d

## Método de ocultação (confirmado)
Texto renderizado no espectrograma da DIFERENÇA estéreo (L-R), banda ~19.9-22.2 kHz,
ao longo de ~0-90 s do áudio. Inaudível e invisível nos canais L ou R isolados; só
emerge em (L-R). Múltiplas linhas de texto empilhadas por banda de frequência.

## Conteúdo (unified diff de código Python) — transcrição
# [CONFIRMADO a partir dos espectrogramas Audacity + processamento próprio]

--- src/rag_engine/query_translator_original.py    2026-03-01 10:14:22.000000000 +0000
+++ src/rag_engine/query_translator_patched.py      2026-04-12 23:41:05.000000000 +0100
@@ -42,6 +42,26 @@
     filter_dict = self.llm_parser.extract_metadata_filters(user_query)

# Fragmentos adicionais confirmados (ordem a validar no Audacity):
#   import pickle, base64
#   load_whitening_matrix
#   "All-but-the-Top" projection to eliminate  (ensemble dimensions)
#   mu = np.array(...); ... np.dot(W.T, (embedding_vector - mu))
#   os.getenv("DEFAULT_EVAL_CLUSTER")
#   "cluster_id": os.getenv("DEFAULT_EVAL_CLUSTER")
#   def build_pgvector_query(self, semantic_query: str, filters: Dict[str, Any]):
#       ...
#       return filter_dict
#   except Exception: pass
#   # comments: "Resolving anisotropic representation degradation in dense retrieval"
#   # "high-cardinality queries currently trigger dense-cluster distance OOM"
#   # "Route the normalized query to the bounded execution ..."
#   # "Load pre-computed principal components directly from the secure daemon environment"
#   # "Orthogonalize the query vector"

## STATUS
# Natureza e ligação ao caso: CONFIRMADAS (código do query_translator do Project AMELIA).
# Transcrição integral literal: A COMPLETAR no Audacity (vista nítida), linha a linha.
