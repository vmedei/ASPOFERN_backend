import pandas as pd
from .utils import gerarCSV

def gerar_relatorio_servicos(df_unimedGeral, df_resultado):
    try:
        # Filtra por linhas de servicos onde o valor é diferente de 0
        df_servicos_geral = df_unimedGeral[(df_unimedGeral['descricao'] == 'SERVICOS E COBERTURAS ADICIONAIS')][['cpf','valor','nome','descricao']]
        df_servicos = df_servicos_geral[(df_servicos_geral['descricao'] == 'SERVICOS E COBERTURAS ADICIONAIS') & (df_servicos_geral['valor'] != 0)][['cpf','valor','nome','descricao']]
        # Adiciona o campo descrição
        df_servicos['descricao'] = 'SERVICOS E COBERTURAS ADICIONAIS UNIMED'
        # Adiciona o código de convênio
        df_servicos['cod_convenio'] = 23

        df_resultado = pd.concat([df_resultado, df_servicos], ignore_index=True)
        df_unimedGeral = df_unimedGeral.drop(df_servicos_geral.index.tolist())
        df_unimedGeral.reset_index(drop=True, inplace=True)
        return df_resultado, df_unimedGeral
    
    except:
        print("Erro ao gerar relatório de serviços Unimed")
        raise