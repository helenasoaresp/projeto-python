# main.py
from leitor import carregar_clientes, carregar_transacoes, carregar_config
from validador import validar_cliente, validar_transacao, separar_registros
from transformador import transformar_clientes, transformar_transacoes
from processador import media_idade, extremos_idade, contar_por_cidade, total_aprovado

# --- LEITURA ---
clientes_raw = carregar_clientes("dataprocessor/data/clientes.csv")
transacoes_raw = carregar_transacoes("dataprocessor/data/transacoes.csv")
config = carregar_config("dataprocessor/data/config.json")

# --- VALIDAÇÃO ---
clientes_validos, clientes_invalidos = separar_registros( 
    clientes_raw, validar_cliente
)
ids_validos = {c["id"] for c in clientes_validos}
print(f"IDs válidos de clientes: {ids_validos}") 

transacoes_validas, transacoes_invalidas = separar_registros(
    transacoes_raw, validar_transacao,
    ids_clientes=ids_validos, config=config
)

# --- TRANSFORMAÇÃO ---
clientes = transformar_clientes(clientes_validos)
transacoes = transformar_transacoes(transacoes_validas)

# --- PROCESSAMENTO ---

media_idade_result = media_idade(clientes)
extremos_idade_result = extremos_idade(clientes)
contar_por_cidade_result = contar_por_cidade(clientes)
total_aprovado_result = total_aprovado(transacoes)

# --- RESUMO ---
print("=== RELATÓRIO FINAL — DataProcessor ===")
print()

print(f"CLIENTES PROCESSADOS: ({len(clientes)} válidos de {len(clientes_raw)})")
for c in clientes:
    print(f"  ID {c['id']} | {c['nome']} | {c['email']} | {c['idade']} anos | {c['cidade']}")
print()

print(f"CLIENTES REJEITADOS: ({len(clientes_invalidos)})")
for item in clientes_invalidos:
    c = item["registro"]
    erros = ", ".join(item["erros"])

    print(f"  ID {c.get('id')} — {c.get('nome')}: {erros}")
print()

print(f"TRANSAÇÕES PROCESSADAS: ({len(transacoes)} válidas de {len(transacoes_raw)})")
for c in transacoes:
    print(f"  ID {c['id']} | {c['cliente_id']} | {c['valor']} | {c['status']}")
print()

print(f"TRANSAÇÕES REJEITADAS: ({len(transacoes_invalidas)})")
for item in transacoes_invalidas:
    t = item["registro"]
    erros = ", ".join(item["erros"])
    print(f"  ID {t.get('id')} — {erros}")
print()

print("MÉTRICAS")
print(f"  Total aprovado: {total_aprovado_result}")
print(f"  Média de idade (válidos): {media_idade_result}")

