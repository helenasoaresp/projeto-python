import unittest
from dataclasses import FrozenInstanceError

from dataprocessor.core.entidades import Cliente, Transacao


class EntidadesTestCase(unittest.TestCase):
    def test_cliente_identificacao_e_derivada(self):
        cliente = Cliente(5, "Pedro Santos", "", 38, "Sao Paulo", "2023-02-30")
        self.assertEqual(cliente.identificacao, "#5 Pedro Santos")

    def test_transacao_expoe_estado_e_resumo(self):
        transacao = Transacao(
            1, 1, 150.5, "eletronicos", "2023-05-10", "aprovado"
        )
        self.assertTrue(transacao.esta_aprovada)
        self.assertEqual(transacao.resumo, "#1 | R$ 150.50 | aprovado")

    def test_entidades_sao_imutaveis(self):
        cliente = Cliente(1, "Ana", "ana@email.com", 30, "Joinville", "2023-01-01")
        with self.assertRaises(FrozenInstanceError):
            cliente.nome = "Outro nome"


if __name__ == "__main__":
    unittest.main()
