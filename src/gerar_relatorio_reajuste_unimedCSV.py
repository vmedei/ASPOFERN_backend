import pandas as pd

def gerar_relatorio_reajuste(df_unimedGeral, df_resultado):
    try:
        # Filtra linhas que contém mundaça de faixa etária na coluna descrição    
        df_reajuste = df_unimedGeral[df_unimedGeral['descricao'] == 'REAJUSTE - MUDANCA DE FAIXA-ETARIA'][['cpf','valor','nome','descricao']]
        # Adiciona o campo descrição
        df_reajuste['descricao'] = 'REAJUSTE UNIMED - MUDANCA DE FAIXA-ETARIA'
        # Adiciona o código do convênio
        df_reajuste['cod_convenio'] = 21

        
        df_resultado = pd.concat([df_resultado, df_reajuste], ignore_index=True)
        df_unimedGeral = df_unimedGeral.drop(df_reajuste.index.tolist())
        df_unimedGeral.reset_index(drop=True, inplace=True)
        return df_resultado, df_unimedGeral
    
    except:
        print("Erro ao gerar relatório de faixa etária.")
        raise