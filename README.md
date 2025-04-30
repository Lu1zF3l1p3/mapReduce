# MapReduce com Redis – Projeto de Sistemas Distribuídos

Este projeto simula um sistema MapReduce distribuído utilizando Redis como mecanismo de coordenação e passagem de mensagens. O sistema realiza contagem de palavras a partir de um grande arquivo de texto (1GB), dividido em chunks, e processado por múltiplos mappers e reducers.

---

## 📁 Estrutura do Projeto

```
.
├── chunks/                # Contém os arquivos chunkX.txt (divisões do arquivo original)
├── intermediate/          # Arquivos JSON produzidos pelos mappers
├── reducer_inputs/        # Arquivos JSON agrupados por chave para os reducers
├── reducer_outputs/       # Resultados finais parciais (por reducer)
├── data.txt               # Arquivo original (~1GB) de entrada
├── final_result.txt       # Resultado final da contagem de palavras
├── mapper_worker.py       # Código dos workers de mapeamento
├── reducer_worker.py      # Código dos workers de redução
├── shuffler.py            # Fase de shuffle (agrupamento e particionamento)
├── coordinator.py         # Script principal que coordena o processo
├── split_file.py          # Utilitário para dividir o arquivo original em chunks
└── README.md              # Instruções do projeto
```

---

## ✅ Pré-requisitos

- Python 3.8+
- Redis Server
- Bibliotecas Python: `redis`

### Instalação do Redis (Linux)

```bash
sudo apt update
sudo apt install redis
sudo systemctl start redis
sudo systemctl enable redis
```

Para testar se o Redis está funcionando:

```bash
redis-cli ping
# Deve retornar: PONG
```

---

## ⚙️ Configuração e Execução

### 1. Clonar o repositório e instalar dependências

```bash
git clone <url-do-repositório>
cd <pasta-do-projeto>
pip install redis
```

### 2. Gerar um arquivo grande de palavras aleatórias (1GB)

Você pode criar esse arquivo assim:

```bash
base_text="palavra1 palavra2 palavra3 palavra4 palavra5"
yes "$base_text" | head -c 1G > data.txt
```

### 3. Dividir o arquivo em 10 partes (chunks)

```bash
python3 split_file.py
```

Isso criará 10 arquivos em `chunks/chunk0.txt` a `chunk9.txt`.

---

### 4. Rodar o coordenador

O coordenador cuida de:

- Enfileirar tarefas no Redis
- Lançar os mappers
- Esperar mappers terminarem
- Executar o shuffle
- Enfileirar reducers
- Esperar reducers
- Juntar os resultados finais

Execute com:

```bash
python3 coordinator.py
```

## 🧪 Resultado Final

O resultado final é gerado no arquivo:

```
final_result.txt
```

Cada linha contém a contagem de uma palavra no estilo:

```
palavra1: 1500
palavra2: 2340
...
```

---

## 🧹 Limpeza

Para reiniciar do zero:

```bash
rm -rf chunks/* intermediate/* reducer_inputs/* reducer_outputs/* final_result.txt
redis-cli flushall
```

---
