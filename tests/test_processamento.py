import unittest
from pathlib import Path

from dataprocessor.core.entidades import Cliente, ResultadoProcessamento, Transacao
from dataprocessor.infra.fontes import (
    FonteDados,
    FonteDadosMemoria,
    FonteDadosMemoriaFiltradaPorCidade,
    fonte_a_partir_de_caminhos,
)
from dataprocessor.core.transformador import transformar_transacao
from dataprocessor.services.processamento import executar_processamento


class ProcessamentoTestCase(unittest.TestCase):
    def test_fonte_abstrata_nao_pode_ser_instanciada(self):
        with self.assertRaises(TypeError):
            FonteDados()

    def test_processa_dataset_de_arquivo(self):
        base = Path("data/secundário")
        resultado = executar_processamento(
            fonte_a_partir_de_caminhos(
                base / "clientes.csv",
                base / "transacoes.csv",
                base / "config.json",
            )
        )
        self.assertIsInstance(resultado, ResultadoProcessamento)
        self.assertEqual(len(resultado.clientes), 2)
        self.assertEqual(len(resultado.transacoes), 2)
        self.assertEqual(resultado.total_aprovado, 150.5)
        self.assertEqual(resultado.metricas["media_idade"], 39.5)

    def test_processa_fonte_em_memoria_sem_arquivo(self):
        cliente = Cliente(1, "  ANA LIMA ", "ANA@EMAIL.COM", 40, "Joinville", "2023-01-01")
        transacao = Transacao(1, 1, 150.5, "livros", "2023-01-02", "aprovado")
        fonte = FonteDadosMemoria(
            [cliente],
            [transacao],
            {
                "categorias_validas": ["livros"],
                "status_validos": ["aprovado"],
                "valor_minimo": 0,
            },
        )
        resultado = executar_processamento(fonte)
        self.assertEqual(resultado.clientes[0].nome, "Ana Lima")
        self.assertEqual(resultado.transacoes[0].categoria, "livros")
        self.assertEqual(resultado.total_aprovado, 150.5)
        self.assertEqual(cliente.nome, "  ANA LIMA ")
        normalizada = transformar_transacao(
            Transacao(2, 1, 5, " LIVROS ", "2023-01-03", " APROVADO ")
        )
        self.assertEqual(normalizada.categoria, "livros")
        self.assertEqual(normalizada.status, "aprovado")

    def test_fonte_em_memoria_filtra_cidade_e_transacoes_relacionadas(self):
        clientes = [
            Cliente(1, "Ana", "ana@email.com", 30, "Joinville", "2023-01-01"),
            Cliente(2, "Bia", "bia@email.com", 31, "Curitiba", "2023-01-02"),
        ]
        transacoes = [
            Transacao(1, 1, 10, "livros", "2023-01-01", "aprovado"),
            Transacao(2, 2, 20, "livros", "2023-01-02", "aprovado"),
        ]
        fonte = FonteDadosMemoriaFiltradaPorCidade(
            "JOINVILLE", clientes, transacoes, {}
        )
        self.assertEqual([cliente.id for cliente in fonte.carregar_clientes()], [1])
        self.assertEqual(
            [transacao.cliente_id for transacao in fonte.carregar_transacoes()],
            [1],
        )


if __name__ == "__main__":
    unittest.main()
