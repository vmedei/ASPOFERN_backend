import pandas as pd

def gerar_relatorio_coparticipacao(df_unimedGeral, df_resultado):
    try:
        # Cria um novo dataframe apenas com os valores de CO-PARTICIPACAO
        df_coparticipacao = df_unimedGeral[df_unimedGeral['descricao'] == 'CO-PARTICIPACAO'][['cpf','valor','nome','descricao']]
        
        # Criando outro dataframe após ter somados a coluna valor e removendo as linhas repetidas
        df_somado = df_coparticipacao.groupby(['cpf','nome'])['valor'].sum().reset_index()

        # Adicionando campo descricao
        df_somado['descricao'] = "COPART. UNIMED"
        # Adiciona o código do convênio
        df_somado['cod_convenio'] = 12
        
        # Definindo casa decimal como 2 após a virgula
        df_somado['valor'] = df_somado['valor'].apply(lambda x: round(x,2))
        
        df_resultado = pd.concat([df_resultado, df_somado], ignore_index=True)
        df_unimedGeral = df_unimedGeral.drop(df_coparticipacao.index.tolist())
        df_unimedGeral.reset_index(drop=True, inplace=True)
        return df_resultado, df_unimedGeral
    
    except:
        print("Erro ao gerar o relatório de coparticipação!")
        raise