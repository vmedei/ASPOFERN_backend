import pandas as pd
import glob

from . import utils
from .gerar_relatorios_unimedCSV import gerar_relatorio_unimed
from .gerar_relatorio_bonificacao_unimedCSV import gerar_relatorio_bonificacao
from .gerar_relatorio_coparticipacaoCSV import gerar_relatorio_coparticipacao
from .gerar_relatorio_desc_obito_unimedCSV import gerar_relatorio_obito
from .gerar_relatorio_notaCredito_unimedCSV import gerar_relatorio_credito
from .gerar_relatorio_parcelamento_unimedCSV import gerar_relatorio_parcelamento
from .gerar_relatorio_reajuste_unimedCSV import gerar_relatorio_reajuste
from .gerar_relatorio_servicos_unimedCSV import gerar_relatorio_servicos
from .gerar_relatorio_cobranca_retroativa_unimed import gerar_cobranca_retroativa
from .gerar_relatorio_variacao_custo_unimed import gerar_relatorio_variacao_custo_unimed
from .gerar_relatorio_adicionais_debito import gerar_relatorio_adicionais_debito
from .gerar_relatorio_unimed_desconhecido import gerar_relatorio_desconhecido

# Função para exportar dados do Excel para PostgreSQL
# table_name = Nome da tabela no BD
# contratos = Lista de arquivos
# Guarda, em formato de lista, o diretório de cada arquivo que existe dentro da pasta unimed
# table_name = "unimed"
def gerar_unimed_geral(df_resultado):
    contratos = glob.glob("uploads/unimed/*")
    
    try:
        # Ler a Tabela de Referência
        tabela_referencia = pd.read_excel('uploads/tabela_referencia.xlsx', dtype={'cpf_titular': str,'cpf_dependente': str})
        dataframes = []
        
        # Itera por cada argumento passado
        # No caso os argumentos passados foram os caminhos dos arquivos brutos
        for contrato in contratos:
            
            # Ler a tabela Unimed 
            tabela_unimed = pd.read_excel(contrato, usecols=['Nr contrato','Nm beneficiario','Titularidade','Idade','Cpf','Produto','Ds tipo item','Vl item'])
            
            # Tratar o CPF
            tabela_unimed = utils.trata_cpf(tabela_unimed, 'Cpf')
            
            # Colocar todas as coluans em minusculo
            tabela_unimed.columns = tabela_unimed.columns.str.lower()
            
            # Renomeando os campos para melhor entendimento
            tabela_unimed.rename(columns={'ds tipo item':'descricao'}, inplace=True)
            tabela_unimed.rename(columns={'vl item':'valor'}, inplace=True)
            tabela_unimed.rename(columns={'nm beneficiario':'nome'}, inplace=True)
            tabela_unimed.rename(columns={'nr contrato':'num_contrato'}, inplace=True)
            
            dataframes.append(tabela_unimed)
        
        # Junta todos os contratos em um só DataFrame
        tabela_unimed = pd.concat(dataframes, ignore_index=True)
            
        # Relacionar as tabelas e adicionar os campos extras
        df_unimedGeral = utils.add_tabela_referencia(tabela_unimed, tabela_referencia)
        
        # Define as casas decimais da coluna valor
        df_unimedGeral['valor'] = df_unimedGeral['valor'].apply(lambda x: round(x,2))
        
        df_resultado, df_unimedGeral = gerar_relatorio_unimed(df_unimedGeral, df_resultado, [{'codigo': 35, 'num_contrato': 774, 'nome': 'UNICOL I'},
            {'codigo': 36, 'num_contrato': 774, 'nome': 'UNICOL II'},
            {'codigo': 37, 'num_contrato': 775, 'nome': 'QUALITY AD C-E'},
            {'codigo': 38, 'num_contrato': 775, 'nome': 'QUALITY AD C-A'},
            {'codigo': 39, 'num_contrato': 775, 'nome': 'QUALITY AD I-A'},
            {'codigo': 40, 'num_contrato': 775, 'nome': 'QUALITY AD I-E'},
            {'codigo': 41, 'num_contrato': 776, 'nome': 'UNICOLPLUS 20A'},
            {'codigo': 42, 'num_contrato': 776, 'nome': 'UNICOLPLUS 20E'},
            {'codigo': 43, 'num_contrato': 16802, 'nome': 'PL. AMBULATORIAL'}])
        df_resultado, df_unimedGeral = gerar_relatorio_bonificacao(df_unimedGeral, df_resultado)
        df_resultado, df_unimedGeral = gerar_relatorio_coparticipacao(df_unimedGeral, df_resultado)
        df_resultado, df_unimedGeral = gerar_relatorio_obito(df_unimedGeral, df_resultado)
        df_resultado, df_unimedGeral = gerar_relatorio_credito(df_unimedGeral, df_resultado)
        df_resultado, df_unimedGeral = gerar_relatorio_parcelamento(df_unimedGeral, df_resultado)
        df_resultado, df_unimedGeral = gerar_relatorio_reajuste(df_unimedGeral, df_resultado)
        df_resultado, df_unimedGeral = gerar_relatorio_servicos(df_unimedGeral, df_resultado)
        df_resultado, df_unimedGeral = gerar_cobranca_retroativa(df_unimedGeral, df_resultado)
        df_resultado, df_unimedGeral = gerar_relatorio_variacao_custo_unimed(df_unimedGeral, df_resultado)
        df_resultado, df_unimedGeral = gerar_relatorio_adicionais_debito(df_unimedGeral, df_resultado)
        df_resultado, df_unimedGeral = gerar_relatorio_desconhecido(df_unimedGeral, df_resultado)
        
        return df_resultado
    except:
        print("Erro ao exportar dados dos contratos da UNIMED para PostgreSQL:")
        raise