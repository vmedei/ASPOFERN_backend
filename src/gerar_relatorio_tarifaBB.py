import pandas as pd
from . import utils

def gerar_relatorio_tarifa_bb(df_resultado): 
    tabela_debito = pd.read_excel('uploads/tabela_debito.xlsx', usecols=['NOME','CPF'])

    # Colocar todas as colunas em minusculo
    tabela_debito.columns = tabela_debito.columns.str.lower()

    # Deixa o CPF no padrão
    tabela_debito = utils.trata_cpf(tabela_debito, 'cpf')

    # Ensure 'valor' column in df_resultado is numeric
    df_resultado['valor'] = pd.to_numeric(df_resultado['valor'], errors='coerce')

    # Merge df_resultado with tabela_debito on 'cpf'
    merged_df = pd.merge(df_resultado, tabela_debito, on='cpf', how='inner')

    # Group by 'cpf' and sum the 'valor' column
    grouped_df = merged_df.groupby('cpf').agg({'valor': 'sum'}).reset_index()
    
    # Filter rows where 'valor' > 0
    filtered_df = grouped_df[grouped_df['valor'] > 0]

    # Merge filtered_df with tabela_debito to get the 'nome' column
    tarifa_bb = pd.merge(filtered_df, tabela_debito[['cpf', 'nome']], on='cpf', how='left')

    # Adiciona a coluna descrição
    tarifa_bb['descricao'] = 'TARIFA BANCÁRIA'
    
    # Adiciona a coluna código do convênio
    tarifa_bb['cod_convenio'] = 19

    # Define um valor fixo de "2" para a coluna valor
    tarifa_bb['valor'] = 2

    # Remove duplicates, keeping the first occurrence
    tarifa_bb = tarifa_bb.drop_duplicates(subset='cpf', keep='first')

    # Re-ordena as colunas
    tarifa_bb = tarifa_bb[['cpf', 'valor', 'nome', 'descricao', 'cod_convenio']]

    df_resultado = pd.concat([df_resultado, tarifa_bb], ignore_index=True)
    
    return df_resultado