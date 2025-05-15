
TAMANHO_TOTAL = 1024 * 1024 * 1024  # 1 GB em bytes
PALAVRA = "Aprender programação melhora raciocínio lógico criatividade "  
PALAVRA_EM_BYTES = PALAVRA.encode('utf-8')
TAMANHO_PALAVRA = len(PALAVRA_EM_BYTES)

# Quantas vezes precisamos repetir para alcançar (ou ultrapassar) 1 GB
vezes = TAMANHO_TOTAL // TAMANHO_PALAVRA
resto = TAMANHO_TOTAL % TAMANHO_PALAVRA

with open("data.txt", "wb") as f:
    f.write(PALAVRA_EM_BYTES * vezes)  # escreve o bloco repetido
    if resto:
        f.write(PALAVRA_EM_BYTES[:resto])  # escreve só o que falta para completar exatamente 1 GB
