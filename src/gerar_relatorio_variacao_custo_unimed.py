import pandas as pd

def gerar_relatorio_variacao_custo_unimed(df_unimedGeral, df_resultado):
    try:
        # Filtra apenas por linhas de bonificação
        df_variacao = df_unimedGeral[df_unimedGeral['descricao'] == 'REAJUSTE - VARIACAO DE CUSTO'][['cpf','valor','nome','descricao']]

        # Adiciona o campo descrição
        df_variacao['descricao'] = 'REAJUSTE - VARIACAO DE CUSTO'
        # Adiciona o código do convênio
        df_variacao['cod_convenio'] = 22
        
        df_resultado = pd.concat([df_resultado, df_variacao], ignore_index=True)
        df_unimedGeral = df_unimedGeral.drop(df_variacao.index.tolist())
        df_unimedGeral.reset_index(drop=True, inplace=True)
        return df_resultado, df_unimedGeral

    except:
        print("Erro ao gerar o relatorio de variação de custo")
        raise