import pandas as pd

from . import utils
from . import gerar_relatorio_tarifaSerproCSV

def gerar_relatorio_desconto(df_resultado):
    try:
        # Lê a planilha e converte para DataFrame
        df = pd.read_excel('uploads/consignacoes_unimed.xlsx')
        
        # Identifica o índice da linha onde o cabeçalho da tabela começa
        inicio_tabela = df[df.iloc[:, 0].str.contains("ORG", na=False)].index[0] + 1
        
        # Recarrega o dataframe agora com a primeira linha sendo o início da tabela
        df = pd.read_excel('uploads/consignacoes_unimed.xlsx', header=inicio_tabela, usecols=lambda x: x.upper() in ['CPF','VALOR','NOME'], dtype={'CPF': str})
        
        # Seleciona apenas as linhas que começam com 20115, isso é para excluir as linhas do total que ficam no final da tabela e possíveis linhas em branco
        tabela_consignacoes = df.iloc[:-1].copy()
        
        # Colocar todas as coluans em minusculo
        tabela_consignacoes.columns = tabela_consignacoes.columns.str.lower()
        
        # Deixa o CPF no padrão
        tabela_consignacoes = utils.trata_cpf(tabela_consignacoes, 'cpf')
      
        # Define as casas decimais da coluna valor
        tabela_consignacoes['valor'] = tabela_consignacoes['valor'].apply(lambda x: round(x,2))
        
        # Deixa o valor negativo
        tabela_consignacoes['valor'] = tabela_consignacoes['valor'] * -1
         
        # Adiciona o campo descrição
        tabela_consignacoes['descricao'] = 'DESCONTO EM FOLHA UNIMED'
        tabela_consignacoes['cod_convenio'] = 14
        
        df_resultado = gerar_relatorio_tarifaSerproCSV.gerar_tarifa_serpro(tabela_consignacoes, df_resultado)

        # Exporta os dados para o arquivo CSV
        return pd.concat([df_resultado, tabela_consignacoes], ignore_index=True)

    except:
        print("Erro ao exportar dados da tabela de consignações")
        raise