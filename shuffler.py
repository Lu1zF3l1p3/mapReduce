import json
import os
from collections import defaultdict
import hashlib


def shuffler():
    intermediate_files = os.listdir('intermediate/')
    kv_store = defaultdict(list)

    for file in intermediate_files:
        file_path = f'intermediate/{file}'

        # Verifica se o arquivo não está vazio
        if os.path.getsize(file_path) == 0:
            print(f"Arquivo vazio encontrado: {file_path}, pulando.")
            continue  # Pula para o próximo arquivo

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                kv_pairs = json.load(f)  # Carrega o conteúdo JSON

                # Verifique se kv_pairs é uma lista de listas, como esperado
                if not isinstance(kv_pairs, list):
                    print(f"Erro: o arquivo {file_path} não contém uma lista. Pulando...")
                    continue

                # Processa os pares chave-valor
                for key, value in kv_pairs:
                    kv_store[key].append(value)

        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar o arquivo {file_path}: {e}")
            continue  # Caso o arquivo tenha problemas, pule para o próximo arquivo

    # Divida os dados entre os reducers
    partitions = [defaultdict(list) for _ in range(10)]
    for key, values in kv_store.items():
        reducer_index = int(hashlib.md5(key.encode()).hexdigest(), 16) % 10
        partitions[reducer_index][key].extend(values)

    # Grava os arquivos de entrada para os reducers
    
    if not os.path.exists('reducer_inputs'):
        os.makedirs('reducer_inputs')
    
    for i, partition in enumerate(partitions):
        with open(f'reducer_inputs/reducer_input_{i}.json', 'w', encoding='utf-8') as f:
            json.dump(partition, f)

if __name__ == "__main__":
    shuffler()
