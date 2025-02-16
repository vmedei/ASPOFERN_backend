import pandas as pd
from .utils import trata_cpf

def gerar_sempre_odontosystem(df_resultado):

    try:
        # Ler a tabela de reajuste
        tabela_sempre_odontosystem = pd.read_excel('uploads/tabela_planos_sempre_odontosystem.xlsx')
        
        # Coloca todas as colunas em minúsculo
        tabela_sempre_odontosystem.columns = tabela_sempre_odontosystem.columns.str.lower()
        
        # Padroniza a coluna CPF
        tabela_sempre_odontosystem = trata_cpf(tabela_sempre_odontosystem, 'cpf')
        
        # Adiciona a tabela ao df_resultado
        df_resultado = pd.concat([df_resultado, tabela_sempre_odontosystem], ignore_index=True)

        return df_resultado

    except Exception as e:
        print(f"Erro ao gerar tabela de planos do Odontosystem: {e}")
        raise