import pandas as pd

def gerar_cobranca_retroativa(df_unimedGeral, df_resultado):
    try:
        # Filtra apenas por linhas de bonificação
        df_retroativo = df_unimedGeral[df_unimedGeral['descricao'] == 'REAJUSTE - COBRANCA RETROATIVA'][['cpf','valor','nome','descricao']]

        # Adiciona o campo descrição
        df_retroativo['descricao'] = 'COBRANCA RETROATIVA DO REAJUSTE'
        # Adiciona o código do convênio
        df_retroativo['cod_convenio'] = 55
        
        df_resultado = pd.concat([df_resultado, df_retroativo], ignore_index=True)
        df_unimedGeral = df_unimedGeral.drop(df_retroativo.index.tolist())
        df_unimedGeral.reset_index(drop=True, inplace=True)
        return df_resultado, df_unimedGeral

    except:
        print("Erro ao gerar o relatorio de cobrança retroativa")
        raise