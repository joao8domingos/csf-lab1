import re
import string

# Ler o ficheiro de legendas
with open('artifacts/downloads/subtitles.srt', 'r', encoding='utf-8') as f:
    content = f.read()

# Dividir em blocos de legendas (separados por linhas vazias)
blocks = content.strip().split('\n\n')
phrases = set()

for block in blocks:
    lines = block.split('\n')
    block_lines = []
    
    for line in lines:
        # Ignorar números de sequência e timestamps
        if '-->' in line or line.strip().isdigit():
            continue
        
        # Remover tags de interlocutor (ex: [NARRATOR]) se pretendido, ou manter se forem parte da password
        # Vamos recolher o texto limpo de cada linha do bloco
        cleaned = line.strip()
        if cleaned:
            block_lines.append(cleaned)
    
    if block_lines:
        # Juntar as linhas do mesmo bloco numa única string (removendo o \n)
        joined_phrase = " ".join(block_lines)
        
        # 1. Frase original (com quebras de linha substituídas por espaço)
        phrases.add(joined_phrase)
        
        # Também sem as tags como [NARRATOR] para abranger mais hipóteses
        clean_no_tag = re.sub(r'\[.*?\]', '', joined_phrase).strip()
        if clean_no_tag:
            phrases.add(clean_no_tag)
            
            # 2. Sem pontuação
            no_punct = clean_no_tag.translate(str.maketrans('', '', string.punctuation))
            if no_punct:
                phrases.add(no_punct)
                
                # 3. Sem pontuação e sem espaços
                no_space = "".join(no_punct.split())
                if no_space:
                    phrases.add(no_space)
                    phrases.add(no_space.lower())

# Guardar na wordlist final
wordlist_path = 'results/joined_blocks_wordlist.txt'
with open(wordlist_path, 'w', encoding='utf-8') as f:
    for p in sorted(phrases):
        if p:
            f.write(p + '\n')

print(f"Sucesso! Geradas {len(phrases)} hipóteses com linhas unidas em {wordlist_path}")
