import pandas as pd
from .utils import gerarCSV

def gerar_relatorio_unimed(df_unimedGeral, df_resultado, contratos):
    try:
        # Dataframe que será usado para agrupar todos os contratos
        dataframes = []
        indices_para_remover = []
        
        # Percorre todos os contratos da UNIMED
        for contrato in contratos:
            if (contrato['nome'] == "PL. AMBULATORIAL"):
                # Selecione apenas linhas do Plano Ambulatorial
                df = df_unimedGeral[(df_unimedGeral['produto'].str.startswith(contrato['nome'])) & (df_unimedGeral['descricao'] == 'PRECO PRE-ESTABELECIDO')][['cpf', 'valor', 'nome']]
            else:
                # Selecione apenas linhas do plano especificado
                df = df_unimedGeral[(df_unimedGeral['produto'] == contrato['nome']) & (df_unimedGeral['descricao'] == 'PRECO PRE-ESTABELECIDO')][['cpf', 'valor', 'nome']]
            
            df['descricao'] = f"MENSALIDADE UNIMED (CONTRATO {contrato['num_contrato']} - PRODUTO {contrato['nome']})"
            df['cod_convenio'] = f"{contrato['codigo']}"
            dataframes.append(df)
            
            # Armazena os índices das linhas filtradas
            indices_para_remover.extend(df.index.tolist())
        
        # Junta todos os contratos em um dataframe só
        tabela_unimed = pd.concat(dataframes, ignore_index=True)
        
        df_resultado = pd.concat([df_resultado, tabela_unimed], ignore_index=True)
        df_unimedGeral = df_unimedGeral.drop(indices_para_remover)
        df_unimedGeral.reset_index(drop=True, inplace=True)
        
        return df_resultado, df_unimedGeral

    except:
        print("Erro ao gerar os relatórios da UNIMED")
        raise