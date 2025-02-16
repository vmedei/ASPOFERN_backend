import pandas as pd

from . import utils

# Função para exportar dados do Excel para PostgreSQL
# table_name = Nome da tabela no BD
def gera_relatorios_ansef(df_resultado):
    try:
        # Ler a Tabela de Referência e Tabela de Débito
        tabela_ansef = pd.read_excel('uploads/tabela_ansef.xls', usecols=[3,4,7,9,10,12], header=4,dtype={'CPF': str, 'RETIDO': str, 'VALOR': float}, decimal=',')
        tabela_ansef.rename(columns={tabela_ansef.columns[4]:"valor_retido"}, inplace=True)
       
        # Remove as duas últimas linhas
        tabela_ansef.drop(tabela_ansef.tail(6).index,inplace=True)
        
        # Colocar todas as coluans em minusculo
        tabela_ansef.columns = tabela_ansef.columns.str.lower()

        # Próximo passo é adiconar tabela de tipo_pagamento e popular no BD
        tabela_ansef = tabela_ansef.loc[(tabela_ansef['repasse'] == 'ANSEF / RN')].reset_index(drop=True)

        # Deixa o CPF no padrão
        tabela_ansef = utils.trata_cpf(tabela_ansef, 'cpf')
               
        # Define as casas decimais da coluna valor
        tabela_ansef['valor'] = tabela_ansef['valor'].apply(lambda x: round(x,2))
        tabela_ansef['valor_retido'] = tabela_ansef['valor_retido'].apply(lambda x: round(x,2))
        
        # Remove valores iguais a zero
        tabela_ansef.drop(tabela_ansef[(tabela_ansef.valor == 0) & (tabela_ansef.retido == 'CAIU DESCONTO')].index, inplace=True)
         
        # Copiando a coluna "valor_retido" e colando na coluna "valor" dos usuários que possuem na coluna "retido" valor igual a "RETIDO/RN"
        tabela_ansef.loc[tabela_ansef['retido'] == 'RETIDO/RN', 'valor'] = tabela_ansef.loc[tabela_ansef['retido'] == 'RETIDO/RN', 'valor_retido']
        
        # Removendo coluna "valor_retido"
        tabela_ansef.drop('valor_retido', axis=1, inplace=True)
        
        # Gerando tabela de mensalidade
        # Recuperando todos os usuários da tabela onde o pagamento foi via debito        
        # Re-ordenando sequência de colunas
        mensalidade_ansef = tabela_ansef.loc[:, ['cpf', 'valor', 'nome']]
        # Adicionando coluna descrição
        mensalidade_ansef['descricao'] = "MENSALIDADE ANSEF"
        mensalidade_ansef['cod_convenio'] = 5
        
        # Ler a nova Tabela de Valores
        tabela_dos_sem_margem = pd.read_excel('uploads/tabela_sem_margem.xlsx', usecols=[0, 1, 2], header=0, dtype={'CPF': str, 'VALOR': float})
        
        # Colocar todas as colunas em minusculo
        tabela_dos_sem_margem.columns = tabela_dos_sem_margem.columns.str.lower()
        
        # Deixa o CPF no padrão
        tabela_dos_sem_margem = utils.trata_cpf(tabela_dos_sem_margem, 'cpf')
        
        # Define as casas decimais da coluna valor
        tabela_dos_sem_margem['valor'] = tabela_dos_sem_margem['valor'].apply(lambda x: round(x, 2))
        
        # Filtrar linhas onde a coluna "retido" começa com "sem margem"
        reajuste_ansef = tabela_ansef[tabela_ansef['retido'].str.startswith('sem margem', na=False)].copy()
        
        # Junta a tabela de reajuste com a tabela de valores atualizados
        reajuste_ansef = reajuste_ansef.merge(tabela_dos_sem_margem[['cpf', 'valor']], on='cpf', how='left', suffixes=('', '_novo'))
        
        # Substitui o valor da tabela ANSEF original pelo valor atualizado da tabela dos sem margem
        # Caso o usuário não exista na tabela dos sem margem, o valor será -1
        reajuste_ansef['valor'] = reajuste_ansef.apply(lambda row: row['valor_novo'] if pd.notnull(row['valor_novo']) else -1, axis=1)
        reajuste_ansef.drop('valor_novo', axis=1, inplace=True)
        
        # Adiciona a coluna descrição
        reajuste_ansef['descricao'] = "REAJUSTE ANSEF"
        
        # Adiciona o codigo do convenio
        reajuste_ansef['cod_convenio'] = 25
        
        # Reordena as colunas
        reajuste_ansef = reajuste_ansef[['cpf', 'valor', 'nome', 'descricao', 'cod_convenio']]
        
        # Gerando tabela de desconto        
        # Filtrando apenas por pagamento via debito e valores da coluna "retido" diferente de "RETIDO/RN"
        desconto_ansef = tabela_ansef.loc[tabela_ansef['retido'] != 'RETIDO/RN'].reset_index(drop=True)
        # Deixando valores negativos
        desconto_ansef['valor'] = desconto_ansef['valor'] * -1
        # Re-ordenando sequência de colunas
        desconto_ansef = desconto_ansef[['cpf', 'valor', 'nome']]
        # Adicionando coluna descrição
        desconto_ansef['descricao'] = "DESCONTO EM FOLHA ANSEF"
        desconto_ansef['cod_convenio'] = 13
        
        # Adicionando as tabelas de mensalidade e desconto ao df_resultado
        df_resultado = pd.concat([df_resultado, mensalidade_ansef], ignore_index=True)
        df_resultado = pd.concat([df_resultado, desconto_ansef], ignore_index=True)
        df_resultado = pd.concat([df_resultado, reajuste_ansef], ignore_index=True)
        
        return df_resultado
        
    except Exception as e:
        print(f"Erro ao gerar relatórios ANSEF: {e}")
        raise
