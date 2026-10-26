from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class Cliente:
    id: int | None
    nome: str
    email: str
    idade: int | None
    cidade: str
    data_cadastro: str

    @property
    def identificacao(self) -> str:
        return f"#{self.id} {self.nome}"


@dataclass(frozen=True)
class Transacao:
    id: int | None
    cliente_id: int | None
    valor: float | None
    categoria: str
    data: str
    status: str

    @property
    def esta_aprovada(self) -> bool:
        return self.status == "aprovado"

    @property
    def resumo(self) -> str:
        valor = "indisponível" if self.valor is None else f"R$ {self.valor:.2f}"
        return f"#{self.id} | {valor} | {self.status}"


@dataclass(frozen=True)
class ResultadoProcessamento:
    clientes: list[Cliente]
    transacoes: list[Transacao]
    clientes_invalidos: list[dict]
    transacoes_invalidas: list[dict]
    metricas: dict[str, float | int | None]

    @property
    def total_aprovado(self) -> float:
        return float(self.metricas["total_aprovado"] or 0)

    def to_dict(self) -> dict:
        return asdict(self)