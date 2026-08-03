from dataprocessor.pipeline import executar_pipeline


def main():
    resultado = executar_pipeline(
        "data/clientes.csv",
        "data/transacoes.csv",
        "data/config.json",
    )

    print("=== DataProcessor ===")
    print(f"Clientes válidos: {len(resultado['clientes'])}")
    print(f"Transações válidas: {len(resultado['transacoes'])}")
    print(f"Total aprovado: R$ {resultado['metricas']['total_aprovado']:.2f}")


if __name__ == "__main__":
    main()