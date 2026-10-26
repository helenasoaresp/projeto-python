import json
import unittest

from dataprocessor.core.entidades import Cliente, ResultadoProcessamento, Transacao
from dataprocessor.infra.relatorios import (
    GeradorRelatorio,
    RelatorioCsv,
    RelatorioInvalidos,
    RelatorioJson,
    RelatorioTexto,
    criar_gerador,
)


def resultado_exemplo():
    cliente = Cliente(1, "Ana", "ana@email.com", 30, "Joinville", "2023-01-01")
    transacao = Transacao(1, 1, 150.5, "livros", "2023-01-02", "aprovado")
    return ResultadoProcessamento(
        clientes=[cliente],
        transacoes=[transacao],
        clientes_invalidos=[],
        transacoes_invalidas=[],
        metricas={
            "media_idade": 30,
            "total_aprovado": 150.5,
            "ticket_medio_aprovado": 150.5,
        },
    )


class RelatoriosTestCase(unittest.TestCase):
    def test_gerador_relatorio_e_uma_abc(self):
        self.assertTrue(issubclass(RelatorioTexto, GeradorRelatorio))
        with self.assertRaises(TypeError):
            GeradorRelatorio()

    def test_json_preserva_dados_e_metricas(self):
        conteudo = json.loads(RelatorioJson().render(resultado_exemplo()))
        self.assertEqual(conteudo["metricas"]["total_aprovado"], 150.5)
        self.assertEqual(conteudo["clientes"][0]["nome"], "Ana")

    def test_csv_contem_cabecalho_e_clientes(self):
        linhas = RelatorioCsv().render(resultado_exemplo()).splitlines()
        self.assertEqual(linhas[0], "id,nome,email,idade,cidade,data_cadastro")
        self.assertIn("1,Ana,ana@email.com,30,Joinville,2023-01-01", linhas)

    def test_fabrica_escolhe_formatos_e_rejeita_formato_desconhecido(self):
        self.assertIsInstance(criar_gerador("texto"), RelatorioTexto)
        with self.assertRaises(ValueError):
            criar_gerador("xml")

    def test_relatorio_invalidos_apresenta_registros_sem_revalidar(self):
        resultado = resultado_exemplo()
        resultado = ResultadoProcessamento(
            clientes=resultado.clientes,
            transacoes=resultado.transacoes,
            clientes_invalidos=[
                {"registro": resultado.clientes[0], "erros": ["email inválido"]}
            ],
            transacoes_invalidas=[
                {"registro": resultado.transacoes[0], "erros": ["status inválido"]}
            ],
            metricas=resultado.metricas,
        )
        relatorio = RelatorioInvalidos().render(resultado)
        self.assertIn("#1 Ana: email inválido", relatorio)
        self.assertIn("#1 | R$ 150.50 | aprovado: status inválido", relatorio)


if __name__ == "__main__":
    unittest.main()
