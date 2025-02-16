import pandas as pd

def gerar_relatorio_adicionais_debito(df_unimedGeral, df_resultado):
    try:
        # Filtra apenas por linhas de bonificação
        df_bonificacao = df_unimedGeral[df_unimedGeral['descricao'] == 'ADICIONAIS A DEBITO'][['cpf','valor','nome','descricao']]

        # Adiciona o campo descrição
        df_bonificacao['descricao'] = 'ADICIONAIS A DÉBITO UNIMED'
        # Adiciona o código do convênio
        df_bonificacao['cod_convenio'] = 26
        
        df_resultado = pd.concat([df_resultado, df_bonificacao], ignore_index=True)
        df_unimedGeral = df_unimedGeral.drop(df_bonificacao.index.tolist())
        df_unimedGeral.reset_index(drop=True, inplace=True)
        return df_resultado, df_unimedGeral

    except:
        print("Erro ao gerar o relatorio de adicionais a débito")
        raise