import os

def split_file_by_words(input_file='data.txt', output_dir='chunks', num_chunks=10):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(input_file, 'r', encoding='utf-8') as f:
        text = f.read()

    words = text.split()
    total_words = len(words)
    words_per_chunk = total_words // num_chunks

    for i in range(num_chunks):
        start = i * words_per_chunk
        end = (i + 1) * words_per_chunk if i != num_chunks - 1 else total_words
        chunk_words = words[start:end]

        chunk_file = os.path.join(output_dir, f'chunk{i}.txt')
        with open(chunk_file, 'w', encoding='utf-8') as cf:
            cf.write(' '.join(chunk_words))

    print(f'Arquivo dividido por palavras em {num_chunks} partes no diretório "{output_dir}/"')

if __name__ == "__main__":
    split_file_by_words()
