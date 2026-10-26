import csv
import io
import json
from abc import ABC, abstractmethod

from ..core.entidades import ResultadoProcessamento


class GeradorRelatorio(ABC):
    @abstractmethod
    def render(self, resultado: ResultadoProcessamento) -> str:
        raise NotImplementedError


class RelatorioTexto(GeradorRelatorio):
    def render(self, resultado: ResultadoProcessamento) -> str:
        media_idade = resultado.metricas["media_idade"]
        media = "indisponível" if media_idade is None else f"{media_idade:.1f}"
        return "\n".join(
            [
                "=== DataProcessor CLI ===",
                f"Clientes válidos: {len(resultado.clientes)}",
                f"Clientes inválidos: {len(resultado.clientes_invalidos)}",
                f"Transações válidas: {len(resultado.transacoes)}",
                f"Transações inválidas: {len(resultado.transacoes_invalidas)}",
                f"Média de idade: {media}",
                f"Total aprovado: R$ {resultado.total_aprovado:.2f}",
                f"Ticket médio aprovado: "
                f"{resultado.metricas['ticket_medio_aprovado']}",
            ]
        ) + "\n"


class RelatorioJson(GeradorRelatorio):
    def render(self, resultado: ResultadoProcessamento) -> str:
        return json.dumps(
            resultado.to_dict(), ensure_ascii=False, indent=2
        ) + "\n"


class RelatorioCsv(GeradorRelatorio):
    def render(self, resultado: ResultadoProcessamento) -> str:
        saida = io.StringIO(newline="")
        escritor = csv.writer(saida)
        escritor.writerow(
            ("id", "nome", "email", "idade", "cidade", "data_cadastro")
        )
        for cliente in resultado.clientes:
            escritor.writerow(
                (
                    cliente.id,
                    cliente.nome,
                    cliente.email,
                    cliente.idade,
                    cliente.cidade,
                    cliente.data_cadastro,
                )
            )
        return saida.getvalue()


class RelatorioInvalidos(GeradorRelatorio):
    def render(self, resultado: ResultadoProcessamento) -> str:
        linhas = ["=== Registros inválidos ==="]
        for item in resultado.clientes_invalidos:
            linhas.append(
                f"{item['registro'].identificacao}: {', '.join(item['erros'])}"
            )
        for item in resultado.transacoes_invalidas:
            linhas.append(
                f"{item['registro'].resumo}: {', '.join(item['erros'])}"
            )
        return "\n".join(linhas) + "\n"


def criar_gerador(formato: str) -> GeradorRelatorio:
    geradores = {
        "texto": RelatorioTexto,
        "json": RelatorioJson,
        "csv": RelatorioCsv,
        "invalidos": RelatorioInvalidos,
    }
    try:
        return geradores[formato]()
    except KeyError as erro:
        raise ValueError(f"Formato de relatório inválido: {formato}") from erro
