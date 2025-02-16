import pandas as pd

def gerar_relatorio_bonificacao(df_unimedGeral, df_resultado):
    try:
        # Filtra apenas por linhas de bonificação
        df_bonificacao = df_unimedGeral[df_unimedGeral['descricao'] == 'BONIFICACAO'][['cpf','valor','nome','descricao']]

        # Adiciona o campo descrição
        df_bonificacao['descricao'] = 'BONIFICACAO'
        # Adiciona o código do convênio
        df_bonificacao['cod_convenio'] = 49
        
        df_resultado = pd.concat([df_resultado, df_bonificacao], ignore_index=True)
        df_unimedGeral = df_unimedGeral.drop(df_bonificacao.index.tolist())
        df_unimedGeral.reset_index(drop=True, inplace=True)
        return df_resultado, df_unimedGeral

    except:
        print("Erro ao gerar o relatorio de bonificação")
        raise