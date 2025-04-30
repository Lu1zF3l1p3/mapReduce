import redis
import json
import os

def reduce_function(key, values):
    return sum(values)

def reducer_worker():
    r = redis.Redis(host='localhost', port=6379, db=0)
    
    if not os.path.exists('reducer_outputs'):
        os.makedirs('reducer_outputs')
        
    while True:
        task = r.lpop('reducer_tasks')
        if not task:
            break
        reducer_input_file = task.decode('utf-8')
        
        with open(f'reducer_inputs/{reducer_input_file}', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        results = {}
        for key, values in data.items():
            results[key] = reduce_function(key, values)
        
        output_file = f'reducer_outputs/{reducer_input_file.replace("input", "output").replace(".json", ".txt")}'
        with open(output_file, 'w', encoding='utf-8') as out_f:
            for key, value in sorted(results.items()):
                out_f.write(f"{key} {value}\n")
        
        r.publish('reducer_done', reducer_input_file)

if __name__ == "__main__":
    reducer_worker()
