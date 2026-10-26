import unittest
from unittest.mock import patch

from fastapi import HTTPException

from dataprocessor.interfaces.api import relatorio, relatorio_csv


class ApiTestCase(unittest.TestCase):
    def test_relatorio_json_reutiliza_pipeline(self):
        resultado = relatorio()
        self.assertEqual(resultado["metricas"]["total_aprovado"], 15827.79)

    def test_relatorio_csv_define_tipo_de_conteudo(self):
        resposta = relatorio_csv()
        self.assertEqual(resposta.media_type, "text/csv")
        self.assertIn("id,nome,email", resposta.body.decode("utf-8"))

    def test_cidade_vazia_e_rejeitada(self):
        with self.assertRaises(HTTPException) as contexto:
            relatorio("   ")
        self.assertEqual(contexto.exception.status_code, 422)

    def test_arquivo_ausente_vira_erro_http_404(self):
        with patch(
            "dataprocessor.interfaces.api._executar",
            side_effect=FileNotFoundError("clientes.csv"),
        ):
            with self.assertRaises(HTTPException) as contexto:
                relatorio()
        self.assertEqual(contexto.exception.status_code, 404)


if __name__ == "__main__":
    unittest.main()
