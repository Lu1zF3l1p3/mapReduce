import os
import redis
import json
import logging

# Configuração de logging para o mapper
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def map_function(text):
    words = text.strip().split()
    return [(word.lower(), 1) for word in words]

def mapper_worker():
    r = redis.Redis(host='localhost', port=6379, db=0)
    while True:
        task = r.rpop('mapper_tasks')
        if not task:
            break  # No more tasks
        logging.info(f"Processando {task.decode('utf-8')}")  # Log quando pegar uma tarefa  
        chunk_file = task.decode('utf-8')
        output = []
        
        with open(f'chunks/{chunk_file}', 'r', encoding='utf-8') as f:
            text = f.read()
            output.extend(map_function(text))
            
        if not os.path.exists('intermediate'):
            os.makedirs('intermediate')
            
        intermediate_file = f'intermediate/{chunk_file}.json'
        with open(intermediate_file, 'w', encoding='utf-8') as out_f:
            json.dump(output, out_f)

        r.publish('mapper_done', chunk_file)

if __name__ == "__main__":
    mapper_worker()
