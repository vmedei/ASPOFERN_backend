import pandas as pd

from . import utils

def gerar_relatorio_uniodonto(df_resultado):
    try:
        
        # Lê o csv uniodonto e armazena em um dataframe
        # sep = Define o separador do csv
        # encolding = Codec do csv para que o Pandas entenda o arquivo
        # usecols = Colunas que serão preenchidas no DataFrame
        tabela_unidonto = pd.read_csv("uploads/uniodonto.csv", sep=";", encoding='latin-1', usecols=['Nome','Total','CPF','Vinculo'])
        tabela_referencia = pd.read_excel('uploads/tabela_referencia.xlsx', dtype={'cpf_titular': str,'cpf_dependente': str})
        
        # Define o texto de todas as colunas para minuculas 
        tabela_unidonto.columns = tabela_unidonto.columns.str.lower()

        # Faz um filtro semelhante ao WHERE do SQL
        # Está sendo selecionado todas as linhas onde a coluna vinculo = TITULAR
        # O resultado é um dataframe contendo apenas Nome, Total e CPF apenas dos titulares
        tabela_unidonto_titulares = tabela_unidonto.loc[tabela_unidonto['vinculo'] == 'TITULAR', ['cpf','total', 'nome']]
        
        # Remove os pontos do CPF
        tabela_unidonto_titulares['cpf'] = tabela_unidonto_titulares['cpf'].str.replace('.','')
        
        # Renomeia a coluna "total" para "valor"
        tabela_unidonto_titulares.rename(columns={'total':'valor'}, inplace=True)
        
        # Remove o ponto do valor e substitui por vírgula
        tabela_unidonto_titulares['valor'] = tabela_unidonto_titulares['valor'].str.replace(',','.')
        
        # Criação de uma coluna chamada descrição escrito "PLANO UNIODONTO" em cada linha do csv
        tabela_unidonto_titulares['descricao'] = "PLANO UNIODONTO"
        
        # Faz a adição da tabela referência 
        tabela_relacionada = utils.add_tabela_referencia(tabela_unidonto_titulares, tabela_referencia)
                    
        # Adição do código de convenio
        tabela_relacionada['cod_convenio'] = 9
        
        # Removendo colunas adicionais da tabela referência
        tabela_relacionada.drop(['cpf2','cod_aspofern'], axis=1, inplace=True)

        # Exporta os dados para o arquivo CSV
        return pd.concat([df_resultado, tabela_relacionada], ignore_index=True)
    
    except:
        print("Erro ao exportar dados do plano Uniodonto")
        raise
    
# Exemplo de uso
if __name__ == "__main__":
    table_name = "uniodonto"
    gerar_relatorio_uniodonto()