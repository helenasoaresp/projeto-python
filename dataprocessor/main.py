# main.py
from leitor import carregar_clientes, carregar_transacoes, carregar_config
from validador import validar_cliente, validar_transacao, separar_registros
from transformador import transformar_clientes, transformar_transacoes

# --- LEITURA ---
clientes_raw = carregar_clientes("dataprocessor/data/clientes.csv")
transacoes_raw = carregar_transacoes("dataprocessor/data/transacoes.csv")
config = carregar_config("dataprocessor/data/config.json")

# --- VALIDAÇÃO ---
clientes_validos, clientes_invalidos = separar_registros(
    clientes_raw, validar_cliente
)
ids_validos = {c["id"] for c in clientes_validos}

transacoes_validas, transacoes_invalidas = separar_registros(
    transacoes_raw, validar_transacao,
    ids_clientes=ids_validos, config=config
)

# --- TRANSFORMAÇÃO ---
clientes = transformar_clientes(clientes_validos)
transacoes = transformar_transacoes(transacoes_validas)

# --- RESUMO ---
print("=== DataProcessor ===")
print(f"Clientes: {len(clientes)} válidos, {len(clientes_invalidos)} inválidos")
print(f"Transações: {len(transacoes)} válidas, {len(transacoes_invalidas)} inválidas")
print()
print("Clientes normalizados:")
for c in clientes:
    print(f"  {c['nome']} | {c['email']} | {c['cidade']}")