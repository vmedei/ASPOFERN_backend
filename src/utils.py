import pandas as pd
import os
import datetime

# Função para deixar o CPF padrão em todas as planilhas, de modo a facilitar na comparação
# O padrão definido é xxxxxxxxx-xx
def trata_cpf(dataframe, coluna):
    # Define o tipo do campo do dataframe para String
    dataframe[coluna] = dataframe[coluna].astype(str)
    
    # Remove os pontos do CPF
    dataframe[coluna] = dataframe[coluna].str.replace('.','')
    
    # Remove o traço do digito verificador
    dataframe[coluna] = dataframe[coluna].str.replace('-','')
    
    # Preenche os zeros a esquerda caso não possua, de modo a ficar com 11 digitos do CPF
    dataframe[coluna] = dataframe[coluna].str.zfill(11)
    
    # Adiciona o - do digito verificador
    dataframe[coluna] = dataframe[coluna].str[:9] + "-" + dataframe[coluna].str[9:]

    return dataframe

# Adiciona o tipo de pagamento de cada usuário na tabela geral
def coluna_debito(tabela_unimed, tabela_debito):
    # Padroniza a coluna CPF
    tabela_debito = trata_cpf(tabela_debito, 'CPF')
   
    # Cria a coluna "tipo_pagamento" e por padrão preenche com "transferencia"
    tabela_unimed['tipo_pagamento'] = 'transferencia'
    
    # Verifica cada CPF da tabela_unimed e caso ele esteja também na tabela_debito, o campo "tipo_pagamento" é alterado para "debito"
    tabela_unimed.loc[tabela_unimed['cpf'].isin(tabela_debito['CPF']), 'tipo_pagamento'] = 'debito'

    return tabela_unimed

# Função para unir as tabelas e adicionar os campos extras CPF_Dependente e COD_Aspofern
def add_tabela_referencia(tabela_unimed, tabela_referencia):
    # Padroniza a dsacoluna CPF de cada dataframe para facilitar na comparação
    tabela_referencia = trata_cpf(tabela_referencia, 'cpf_titular')
    tabela_referencia = trata_cpf(tabela_referencia, 'cpf_dependente')

    # Unindo as tabelas com base na coluna CPF
    tabela_relacionada = pd.merge(tabela_unimed, tabela_referencia, how='left', left_on='cpf', right_on='cpf_dependente')

    # Excluindo a coluna CPF após a união para evitar duplicidade
    tabela_relacionada.drop(columns=['cpf_dependente'], inplace=True)

    # Renomeando a coluna COD. ASPOFERN para COD_Aspofern
    tabela_relacionada.rename(columns={'cpf': 'cpf2'}, inplace=True)
    tabela_relacionada.rename(columns={'cpf_titular': 'cpf'}, inplace=True)
    
    # Preenchendo os campos em branco do dataset para evitar erros
    tabela_relacionada['cod_aspofern'] = tabela_relacionada['cod_aspofern'].fillna(value=0)
    tabela_relacionada['cpf'] = tabela_relacionada['cpf'].fillna(value="novo")
    
    # Formatar o código da ASPOFERN para exibir 3 casas decimais.
    tabela_relacionada['cod_aspofern'] = tabela_relacionada['cod_aspofern'].apply(lambda x: '{:.3f}'.format(x))
    
    return tabela_relacionada

def gerarCSV(nomeArquivo, pastaDestino, dataFrame):
    # Obter o mês atual
    mes_atual = datetime.datetime.now().month

    # Obter o mês seguinte
    mes_seguinte = (mes_atual % 12) + 1

    # Formatando para dois dígitos com zero à esquerda, se necessário
    mes_seguinte_formatado = str(mes_seguinte).zfill(2)
    
    # Verificar se a pasta existe, se não cria a pasta
    if not os.path.exists(pastaDestino):
        os.makedirs(pastaDestino)

    # Caminho completo do arquivo CSV
    path = os.path.join(pastaDestino, f"{nomeArquivo}_{mes_seguinte_formatado}_{datetime.datetime.now().year}.csv")

    # Exporta os dados para o arquivo CSV
    dataFrame.to_csv(path, index=False, decimal=',', sep=';', encoding='latin-1')
    
    return f"{nomeArquivo}_{mes_seguinte_formatado}_{datetime.datetime.now().year}.csv"