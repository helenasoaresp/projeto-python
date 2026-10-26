from pathlib import Path

from ..config import carregar_configuracao_padrao
from ..infra.fontes import fonte_a_partir_de_caminhos
from ..infra.relatorios import criar_gerador
from ..services.processamento import executar_processamento

_CONFIG_PADRAO = carregar_configuracao_padrao()
CAMINHOS_PADRAO = (
    _CONFIG_PADRAO.caminho_clientes,
    _CONFIG_PADRAO.caminho_transacoes,
    _CONFIG_PADRAO.caminho_config,
)
FORMATOS_VALIDOS = {"texto", "json", "csv", "invalidos"}


def processar_caminhos(caminho_clientes, caminho_transacoes, caminho_config):
    fonte = fonte_a_partir_de_caminhos(
        caminho_clientes, caminho_transacoes, caminho_config
    )
    return executar_processamento(fonte)


def solicitar_caminhos():
    prompts = (
        "Caminho do CSV de clientes",
        "Caminho do CSV de transações",
        "Caminho do JSON de configuração",
    )
    return tuple(
        input(f"{prompt} [{padrao}]: ").strip() or padrao
        for prompt, padrao in zip(prompts, CAMINHOS_PADRAO)
    )


def processar(caminhos=None):
    if caminhos is None:
        caminhos = solicitar_caminhos()
    try:
        resultado = processar_caminhos(*caminhos)
    except (OSError, ValueError, KeyError) as erro:
        print(f"[ERRO] Não foi possível processar: {erro}")
        return None

    print(f"Clientes válidos: {len(resultado.clientes)}")
    print(f"Transações válidas: {len(resultado.transacoes)}")
    return resultado


def exibir_relatorio(resultado):
    formato = input(
        "Formato (texto/json/csv/invalidos) [texto]: "
    ).strip() or "texto"
    if formato not in FORMATOS_VALIDOS:
        print(f"Formato inválido: '{formato}'.")
        return
    print(criar_gerador(formato).render(resultado), end="")


def salvar_relatorio(resultado):
    formato = input(
        "Formato (texto/json/csv/invalidos) [texto]: "
    ).strip() or "texto"
    if formato not in FORMATOS_VALIDOS:
        print(f"Formato inválido: '{formato}'.")
        return

    padrao = (
        Path("output")
        / ("relatorio.txt" if formato == "texto" else f"relatorio.{formato}")
    )
    caminho = input(f"Caminho de saída [{padrao}]: ").strip() or str(padrao)
    try:
        arquivo = Path(caminho)
        arquivo.parent.mkdir(parents=True, exist_ok=True)
        arquivo.write_text(
            criar_gerador(formato).render(resultado), encoding="utf-8"
        )
    except OSError as erro:
        print(f"[ERRO] Não foi possível salvar o relatório: {erro}")
        return
    print(f"Relatório salvo em: {caminho}")


def menu_principal():
    resultado = None
    ultimos_caminhos = None
    while True:
        print("\n=== DataProcessor — Menu ===")
        print("1. Processar dados")
        print("2. Exibir relatório")
        print("3. Salvar relatório em arquivo")
        print("4. Reprocessar com os últimos caminhos usados")
        print("5. Sair")
        try:
            opcao = input("Escolha uma opção: ").strip()
        except EOFError:
            print()
            break

        if opcao not in {"1", "2", "3", "4", "5"}:
            print(f"Opção inválida: '{opcao}'. Escolha 1, 2, 3, 4 ou 5.")
            continue
        if opcao == "5":
            break
        if opcao in {"2", "3"}:
            if resultado is None:
                print("Nenhum dado processado ainda. Escolha a opção 1 primeiro.")
                continue
            if opcao == "2":
                exibir_relatorio(resultado)
            else:
                salvar_relatorio(resultado)
            continue

        if opcao == "1":
            caminhos = solicitar_caminhos()
        else:
            if ultimos_caminhos is None:
                print("Nenhum processamento anterior bem-sucedido para repetir.")
                continue
            caminhos = ultimos_caminhos

        novo_resultado = processar(caminhos)
        if novo_resultado is not None:
            resultado = novo_resultado
            ultimos_caminhos = caminhos


if __name__ == "__main__":
    menu_principal()
