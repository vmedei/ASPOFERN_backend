import pandas as pd

from . import gerar_relatorio_desconto_unimedCSV
from . import gerar_relatorio_uniodontoCSV
from . import gerar_relatorios_ansef
from . import gerar_unimed_geral
from . import gerar_relatorios_sempre_odontosystem
from . import gerar_relatorio_tarifaBB
from .utils import gerarCSV

async def gerar_todos():
    df_resultado = pd.DataFrame()

    df_resultado = gerar_unimed_geral.gerar_unimed_geral(df_resultado)
    df_resultado = gerar_relatorio_desconto_unimedCSV.gerar_relatorio_desconto(df_resultado)
    df_resultado = gerar_relatorio_uniodontoCSV.gerar_relatorio_uniodonto(df_resultado)
    df_resultado = gerar_relatorios_ansef.gera_relatorios_ansef(df_resultado)
    df_resultado = gerar_relatorios_sempre_odontosystem.gerar_sempre_odontosystem(df_resultado)
    df_resultado = gerar_relatorio_tarifaBB.gerar_relatorio_tarifa_bb(df_resultado)

    # Trocando . por , na coluna valores
    df_resultado['valor'] = df_resultado['valor'].astype(str).str.replace('.', ',', regex=False)
    
    gerarCSV("Importacao", "processados", df_resultado)

    # Convert DataFrame to JSON
    json_result = df_resultado.to_json(orient='records')

    return json_result