import argparse
import logging
from pathlib import Path

from dataprocessor.config import carregar_configuracao_padrao
from dataprocessor.infra.fontes import fonte_a_partir_de_caminhos
from dataprocessor.infra.relatorios import criar_gerador
from dataprocessor.services.processamento import executar_processamento


def configurar_parser() -> argparse.ArgumentParser:
    config = carregar_configuracao_padrao()
    parser = argparse.ArgumentParser(
        description="Processa dados de clientes e transações."
    )
    parser.add_argument("--clientes", default=config.caminho_clientes)
    parser.add_argument("--transacoes", default=config.caminho_transacoes)
    parser.add_argument("--config", default=config.caminho_config)
    parser.add_argument(
        "--formato",
        choices=("texto", "json", "csv", "invalidos"),
        default="texto",
    )
    parser.add_argument("--output", type=Path, default=Path("output"))
    return parser


def main(argv: list[str] | None = None) -> int:
    args = configurar_parser().parse_args(argv)
    try:
        args.output.mkdir(parents=True, exist_ok=True)
        logging.basicConfig(
            filename=args.output / "dataprocessor.log",
            level=logging.INFO,
            format="%(asctime)s %(levelname)s %(message)s",
            force=True,
        )
        logging.info("Iniciando processamento")
        fonte = fonte_a_partir_de_caminhos(
            args.clientes, args.transacoes, args.config
        )
        resultado = executar_processamento(fonte)
        relatorio = criar_gerador(args.formato).render(resultado)
        nome_arquivo = (
            "relatorio.txt" if args.formato == "texto"
            else f"relatorio.{args.formato}"
        )
        (args.output / nome_arquivo).write_text(relatorio, encoding="utf-8")
        logging.info(
            "Processamento concluído: %d clientes e %d transações válidos",
            len(resultado.clientes),
            len(resultado.transacoes),
        )
    except (OSError, ValueError, KeyError) as erro:
        logging.exception("Falha no processamento")
        print(f"[ERRO] {erro}")
        return 1

    print(relatorio, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
