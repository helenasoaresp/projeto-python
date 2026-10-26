from typing import Annotated

from fastapi import FastAPI, HTTPException, Query, Response

from ..config import carregar_configuracao_padrao
from ..infra.fontes import (
    FonteDadosMemoriaFiltradaPorCidade,
    fonte_a_partir_de_caminhos,
)
from ..infra.relatorios import RelatorioCsv
from ..services.processamento import executar_processamento

app = FastAPI(title="DataProcessor CLI")


def _executar(cidade: str | None = None):
    config = carregar_configuracao_padrao()
    fonte = fonte_a_partir_de_caminhos(
        config.caminho_clientes,
        config.caminho_transacoes,
        config.caminho_config,
    )
    if cidade is not None:
        fonte = FonteDadosMemoriaFiltradaPorCidade(
            cidade,
            clientes=fonte.carregar_clientes(),
            transacoes=fonte.carregar_transacoes(),
            config=fonte.carregar_config(),
        )
    return executar_processamento(fonte)


def _erro_http(erro):
    if isinstance(erro, FileNotFoundError):
        raise HTTPException(status_code=404, detail=str(erro)) from erro
    if isinstance(erro, (ValueError, KeyError)):
        raise HTTPException(status_code=422, detail=str(erro)) from erro
    raise HTTPException(status_code=500, detail="Falha ao ler os dados.") from erro


@app.get("/relatorio")
def relatorio(
    cidade: Annotated[str | None, Query(min_length=1, max_length=100)] = None,
):
    if cidade is not None and not cidade.strip():
        raise HTTPException(
            status_code=422, detail="O parâmetro cidade não pode ser vazio."
        )
    try:
        resultado = _executar(cidade)
    except (OSError, ValueError, KeyError) as erro:
        _erro_http(erro)
    return resultado.to_dict()


@app.get("/relatorio/csv")
def relatorio_csv(
    cidade: Annotated[str | None, Query(min_length=1, max_length=100)] = None,
):
    if cidade is not None and not cidade.strip():
        raise HTTPException(
            status_code=422, detail="O parâmetro cidade não pode ser vazio."
        )
    try:
        resultado = _executar(cidade)
    except (OSError, ValueError, KeyError) as erro:
        _erro_http(erro)
    conteudo = RelatorioCsv().render(resultado)
    return Response(content=conteudo, media_type="text/csv")
