import json
import io
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

from main import main
from dataprocessor.interfaces.menu import processar_caminhos


class CliTestCase(unittest.TestCase):
    def test_cli_salva_json_e_log(self):
        with tempfile.TemporaryDirectory() as diretorio:
            with redirect_stdout(io.StringIO()):
                codigo = main(
                    [
                        "--clientes",
                        "data/secundário/clientes.csv",
                        "--transacoes",
                        "data/secundário/transacoes.csv",
                        "--config",
                        "data/secundário/config.json",
                        "--formato",
                        "json",
                        "--output",
                        diretorio,
                    ]
                )
            relatorio = json.loads(
                (Path(diretorio) / "relatorio.json").read_text(encoding="utf-8")
            )
            self.assertEqual(codigo, 0)
            self.assertEqual(relatorio["metricas"]["total_aprovado"], 150.5)
            self.assertTrue((Path(diretorio) / "dataprocessor.log").exists())

    def test_cli_salva_relatorios_texto_e_csv(self):
        for formato in ("texto", "csv"):
            with self.subTest(formato=formato), tempfile.TemporaryDirectory() as diretorio:
                with redirect_stdout(io.StringIO()):
                    codigo = main(
                        [
                            "--clientes",
                            "data/secundário/clientes.csv",
                            "--transacoes",
                            "data/secundário/transacoes.csv",
                            "--config",
                            "data/secundário/config.json",
                            "--formato",
                            formato,
                            "--output",
                            diretorio,
                        ]
                    )
                nome = "relatorio.txt" if formato == "texto" else "relatorio.csv"
                conteudo = (Path(diretorio) / nome).read_text(encoding="utf-8")
                self.assertEqual(codigo, 0)
                self.assertTrue(conteudo)

    def test_cli_e_porta_testavel_calculam_o_mesmo_total(self):
        resultado_menu = processar_caminhos(
            "data/secundário/clientes.csv",
            "data/secundário/transacoes.csv",
            "data/secundário/config.json",
        )
        with tempfile.TemporaryDirectory() as diretorio:
            subprocess.run(
                [
                    sys.executable,
                    "main.py",
                    "--clientes",
                    "data/secundário/clientes.csv",
                    "--transacoes",
                    "data/secundário/transacoes.csv",
                    "--config",
                    "data/secundário/config.json",
                    "--formato",
                    "json",
                    "--output",
                    diretorio,
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            resultado_cli = json.loads(
                (Path(diretorio) / "relatorio.json").read_text(encoding="utf-8")
            )
        self.assertEqual(
            resultado_cli["metricas"]["total_aprovado"],
            resultado_menu.total_aprovado,
        )

    def test_cli_retorna_codigo_de_erro_para_arquivo_ausente(self):
        with tempfile.TemporaryDirectory() as diretorio:
            with redirect_stdout(io.StringIO()):
                codigo = main(
                    [
                        "--clientes",
                        f"{diretorio}/inexistente.csv",
                        "--transacoes",
                        "data/transacoes.csv",
                        "--config",
                        "data/config.json",
                        "--output",
                        diretorio,
                    ]
                )
            self.assertEqual(codigo, 1)
            self.assertTrue((Path(diretorio) / "dataprocessor.log").exists())


if __name__ == "__main__":
    unittest.main()
