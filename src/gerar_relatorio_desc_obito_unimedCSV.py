import pandas as pd

def gerar_relatorio_obito(df_unimedGeral, df_resultado):
    try:
        # Filtra apenas por linhas de Desconto por obito
        df_obito = df_unimedGeral[df_unimedGeral['descricao'] == 'DESCONTO POR OBITO'][['cpf','valor','nome','descricao']]

        # Adiciona o campo descrição
        df_obito['descricao'] = 'DESCONTO POR OBITO UNIMED'
        # Adiciona o código do convênio
        df_obito['cod_convenio'] =  27

        df_resultado = pd.concat([df_resultado, df_obito], ignore_index=True)
        df_unimedGeral = df_unimedGeral.drop(df_obito.index.tolist())
        df_unimedGeral.reset_index(drop=True, inplace=True)
        return df_resultado, df_unimedGeral
    
    except:
        print("Erro ao gerar o relatório de obito!")
        raise