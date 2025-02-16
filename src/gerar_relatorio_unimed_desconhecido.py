import pandas as pd

def gerar_relatorio_desconhecido(df_unimedGeral, df_resultado):
    try:
        # Selecionar as colunas desejadas
        df_desconhecido = df_unimedGeral[['cpf', 'valor', 'nome', 'descricao']].copy()
        
        # Adicionar a coluna 'cod_convenio' com valor "Desconhecido"
        df_desconhecido['cod_convenio'] = -1
        
        df_resultado = pd.concat([df_resultado, df_desconhecido], ignore_index=True)
        df_unimedGeral.drop(df_desconhecido.index.tolist(), inplace=True)
        
        # Concatenar os DataFrames
        return df_resultado, df_unimedGeral

    except Exception as e:
        print(f"Erro ao gerar o relatorio de produtos desconhecidos: {e}")
        raise