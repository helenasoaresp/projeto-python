from abc import ABC, abstractmethod

from ..core.entidades import Cliente, Transacao
from .arquivos import carregar_clientes, carregar_config, carregar_transacoes


class FonteDados(ABC):
    @abstractmethod
    def carregar_clientes(self) -> list[Cliente]:
        raise NotImplementedError

    @abstractmethod
    def carregar_transacoes(self) -> list[Transacao]:
        raise NotImplementedError

    @abstractmethod
    def carregar_config(self) -> dict:
        raise NotImplementedError


class FonteDadosArquivos(FonteDados):
    def __init__(self, caminho_clientes, caminho_transacoes, caminho_config):
        self.caminho_clientes = caminho_clientes
        self.caminho_transacoes = caminho_transacoes
        self.caminho_config = caminho_config

    def carregar_clientes(self) -> list[Cliente]:
        return carregar_clientes(self.caminho_clientes)

    def carregar_transacoes(self) -> list[Transacao]:
        return carregar_transacoes(self.caminho_transacoes)

    def carregar_config(self) -> dict:
        return carregar_config(self.caminho_config)


class FonteDadosMemoria(FonteDados):
    def __init__(self, clientes=(), transacoes=(), config=None):
        self._clientes = tuple(clientes)
        self._transacoes = tuple(transacoes)
        self._config = dict(config or {})

    def carregar_clientes(self) -> list[Cliente]:
        return list(self._clientes)

    def carregar_transacoes(self) -> list[Transacao]:
        return list(self._transacoes)

    def carregar_config(self) -> dict:
        return dict(self._config)


class FonteDadosMemoriaFiltradaPorCidade(FonteDadosMemoria):
    def __init__(self, cidade, clientes=(), transacoes=(), config=None):
        cidade_normalizada = cidade.strip().casefold()
        clientes_filtrados = tuple(
            cliente
            for cliente in clientes
            if cliente.cidade.strip().casefold() == cidade_normalizada
        )
        ids_clientes = {cliente.id for cliente in clientes_filtrados}
        transacoes_filtradas = tuple(
            transacao
            for transacao in transacoes
            if transacao.cliente_id in ids_clientes
        )
        super().__init__(clientes_filtrados, transacoes_filtradas, config)


def fonte_a_partir_de_caminhos(
    caminho_clientes, caminho_transacoes, caminho_config
) -> FonteDados:
    return FonteDadosArquivos(
        caminho_clientes, caminho_transacoes, caminho_config
    )
