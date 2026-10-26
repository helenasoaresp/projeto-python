import io
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from dataprocessor.core.entidades import ResultadoProcessamento
from dataprocessor.interfaces.menu import (
    menu_principal,
    processar_caminhos,
    salvar_relatorio,
)


class MenuTestCase(unittest.TestCase):
    def test_processar_caminhos_reutiliza_dataset_do_curso(self):
        resultado = processar_caminhos(
            "data/secundário/clientes.csv",
            "data/secundário/transacoes.csv",
            "data/secundário/config.json",
        )
        self.assertIsInstance(resultado, ResultadoProcessamento)
        self.assertEqual(resultado.total_aprovado, 150.5)

    def test_menu_rejeita_opcoes_e_preserva_sessao_apos_falha(self):
        resultado = processar_caminhos(
            "data/secundário/clientes.csv",
            "data/secundário/transacoes.csv",
            "data/secundário/config.json",
        )
        entradas = iter(
            [
                "2",
                "9",
                "1",
                "data/secundário/clientes.csv",
                "data/secundário/transacoes.csv",
                "data/secundário/config.json",
                "2",
                "xml",
                "4",
                "2",
                "texto",
                "5",
            ]
        )
        with patch("builtins.input", side_effect=lambda _="": next(entradas)):
            with patch(
                "dataprocessor.interfaces.menu.processar_caminhos",
                side_effect=[resultado, FileNotFoundError("arquivo ausente")],
            ):
                saida = io.StringIO()
                with redirect_stdout(saida):
                    menu_principal()
        texto = saida.getvalue()
        self.assertIn("Nenhum dado processado ainda", texto)
        self.assertIn("Opção inválida", texto)
        self.assertIn("Formato inválido", texto)
        self.assertIn("Não foi possível processar", texto)
        self.assertIn("Total aprovado: R$ 150.50", texto)

    def test_menu_salva_relatorio_usando_gerador(self):
        resultado = processar_caminhos(
            "data/secundário/clientes.csv",
            "data/secundário/transacoes.csv",
            "data/secundário/config.json",
        )
        with tempfile.TemporaryDirectory() as diretorio:
            caminho = Path(diretorio) / "relatorio.csv"
            with patch(
                "builtins.input",
                side_effect=["csv", str(caminho)],
            ):
                saida = io.StringIO()
                with redirect_stdout(saida):
                    salvar_relatorio(resultado)
            self.assertIn("Relatório salvo", saida.getvalue())
            self.assertTrue(caminho.read_text(encoding="utf-8").startswith("id,nome"))


if __name__ == "__main__":
    unittest.main()
