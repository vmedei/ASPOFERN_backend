import pandas as pd

def gerar_relatorio_parcelamento(df_unimedGeral, df_resultado):
    try:
        # Filtra por linhas que tenha Adicionais a crédito na coluna descrição.
        df_parcelamento = df_unimedGeral[df_unimedGeral['descricao'] == 'ADICIONAIS A CREDITO'][['cpf','valor','nome','descricao']]

        # Adicionando campo descricao
        df_parcelamento['descricao'] = "PARCELAMENTO DE REAJUSTE RETROATIVO UNIMED 2022"
        # Adicionando o número do convênio
        df_parcelamento['cod_convenio'] = 28
        
        # Definindo casa decimal como 2 após a virgula
        df_parcelamento['valor'] = df_parcelamento['valor'].apply(lambda x: round(x,2))
        
        df_resultado = pd.concat([df_resultado, df_parcelamento], ignore_index=True)
        df_unimedGeral = df_unimedGeral.drop(df_parcelamento.index.tolist())
        df_unimedGeral.reset_index(drop=True, inplace=True)
        return df_resultado, df_unimedGeral
    
    except:
        print("Erro ao gerar relatório de parcelamento unimed!")
        raise