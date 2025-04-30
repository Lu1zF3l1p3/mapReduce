import redis
import subprocess
import time
import logging
import os

NUM_MAPPERS = 5
NUM_REDUCERS = 5

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def wait_for_mappers(expected=10):
    logging.info("Aguardando a conclusão dos mappers...")
    r = redis.Redis()
    pubsub = r.pubsub()
    pubsub.subscribe('mapper_done')
    
    completed = set()
    for message in pubsub.listen():
        if message['type'] == 'message':
            chunk_name = message['data'].decode()
            logging.info(f"Mapper finalizado: {chunk_name}")
            completed.add(chunk_name)
            if len(completed) == expected:
                logging.info("Todos os mappers finalizaram.")
                break

def wait_for_reducers(expected=10):
    logging.info("Aguardando a conclusão dos reducers...")
    r = redis.Redis()
    pubsub = r.pubsub()
    pubsub.subscribe('reducer_done')
    
    completed = set()
    for message in pubsub.listen():
        if message['type'] == 'message':
            reducer_input_name = message['data'].decode()
            logging.info(f"Reducer finalizado: {reducer_input_name}")
            completed.add(reducer_input_name)
            if len(completed) == expected:
                logging.info("Todos os reducers finalizaram.")
                break

def coordinator():
    logging.info("Iniciando o processo do coordenador.")
    
    r = redis.Redis()
    r.delete("mapper_tasks")  # limpa fila antiga se houver
    r.delete("reducer_tasks")  # idem
    # não é necessário deletar 'mapper_done' pois é pubsub

    # Enfileira tarefas de mappers
    logging.info("Enfileirando tarefas de mappers.")
    for i in range(10):
        chunk_name = f"chunk{i}.txt"
        r.rpush("mapper_tasks", chunk_name)

    # Inicia os mappers
    for i in range(NUM_MAPPERS):
        logging.info(f"Iniciando o mapper {i + 1}...")
        subprocess.Popen(["python3", "mapper_worker.py"])

    # Espera todos os mappers terminarem
    wait_for_mappers(expected=10)

    # Executa o shuffle
    logging.info("Rodando o shuffle...")
    subprocess.run(["python3", "shuffler.py"])

    # Enfileira tarefas para os reducers
    logging.info("Enfileirando tarefas dos reducers.")
    for i in range(10):
        reducer_input = f"reducer_input_{i}.json"
        r.rpush("reducer_tasks", reducer_input)

    # Inicia os reducers
    for i in range(NUM_REDUCERS):
        logging.info(f"Iniciando o reducer {i + 1}...")
        subprocess.Popen(["python3", "reducer_worker.py"])

    # Espera todos os reducers terminarem
    wait_for_reducers(10)

    # Junta os resultados dos reducers
    logging.info("Unindo os resultados finais.")
    with open("final_result.txt", "w", encoding="utf-8") as outfile:
        for i in range(10):
            fname = f"reducer_outputs/reducer_output_{i}.txt"
            if os.path.exists(fname):
                with open(fname, "r", encoding="utf-8") as f:
                    outfile.write(f.read())

    logging.info("Processo finalizado com sucesso. Resultado em final_result.txt.")

if __name__ == "__main__":
    coordinator()
