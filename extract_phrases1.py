import re
import string

with open('artifacts/downloads/subtitles.srt', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')
no_space_phrases = set()

for line in lines:
    if '-->' in line or line.strip().isdigit() or not line.strip():
        continue
    
    cleaned = re.sub(r'\[.*?\]', '', line).strip()
    if cleaned:
        # Remover pontuação e depois juntar todas as palavras (remover espaços)
        no_punct = cleaned.translate(str.maketrans('', '', string.punctuation))
        no_space = "".join(no_punct.split())
        
        if no_space:
            no_space_phrases.add(no_space)
            # Adicionar também a versão em minúsculas por segurança
            no_space_phrases.add(no_space.lower())

# Guardar a nova wordlist
wordlist_path = 'results/phrase_nospace.txt'
with open(wordlist_path, 'w', encoding='utf-8') as f:
    for p in sorted(no_space_phrases):
        f.write(p + '\n')

print(f"Geradas {len(no_space_phrases)} hipóteses sem espaços em {wordlist_path}")
