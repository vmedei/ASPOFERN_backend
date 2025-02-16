import pandas as pd

def gerar_relatorio_credito(df_unimedGeral, df_resultado):
    try:
        # Recupera as linhas de nota de crédito e onde o valor for diferente de 0
        df_credito_geral = df_unimedGeral[(df_unimedGeral['descricao'] == 'NOTA DE CREDITO')][['cpf','valor','nome','descricao']]
        df_credito = df_credito_geral[(df_credito_geral['descricao'] == 'NOTA DE CREDITO') & (df_credito_geral['valor'] != 0)][['cpf','valor','nome','descricao']]

        # Adiciona o campo descrição
        df_credito['descricao'] = 'CREDITO POR EXCLUSAO IMEDIATA P SAUDE'
        # Adiciona o código do convênio
        df_credito['cod_convenio'] = 47

        df_resultado = pd.concat([df_resultado, df_credito], ignore_index=True)
        df_unimedGeral = df_unimedGeral.drop(df_credito_geral.index.tolist())
        df_unimedGeral.reset_index(drop=True, inplace=True)
        return df_resultado, df_unimedGeral   
     
    except:
        print("Erro ao gerar o relatório de nota de crédito Unimed")
        raise