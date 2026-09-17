import re
import string

# Ler o ficheiro de legendas
with open('artifacts/downloads/subtitles.srt', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.split('\n')
phrases_with_punct = set()
phrases_without_punct = set()

for line in lines:
    # Ignorar linhas de timestamps, números de sequência ou vazias
    if '-->' in line or line.strip().isdigit() or not line.strip():
        continue
    
    # Remover tags de falas (ex: [NARRATOR])
    cleaned_line = re.sub(r'\[.*?\]', '', line).strip()
    
    if cleaned_line:
        phrases_with_punct.add(cleaned_line)
        
        # Remover pontuação para a segunda hipótese
        no_punct = cleaned_line.translate(str.maketrans('', '', string.punctuation)).strip()
        if no_punct:
            phrases_without_punct.add(no_punct)

# Guardar todas as hipóteses numa nova wordlist
wordlist_path = 'results/phrase_wordlist.txt'
with open(wordlist_path, 'w', encoding='utf-8') as f:
    for p in sorted(phrases_with_punct):
        f.write(p + '\n')
    for p in sorted(phrases_without_punct):
        f.write(p + '\n')

print(f"Sucesso! Foram geradas {len(phrases_with_punct) + len(phrases_without_punct)} hipóteses (com e sem pontuação) em {wordlist_path}")
