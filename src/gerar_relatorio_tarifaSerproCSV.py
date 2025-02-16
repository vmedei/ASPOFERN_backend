import pandas as pd

def gerar_tarifa_serpro(df_consignacoes, df_resultado):
    try:
        df_tarifa = df_consignacoes[['cpf','valor','nome']].copy()

        df_tarifa['valor'] = 3.08
        df_tarifa['descricao'] = 'TARIFA ADMINISTRATIVA'
        df_tarifa['cod_convenio'] = 11

        return pd.concat([df_resultado, df_tarifa], ignore_index=True)
    except:
        print("Erro ao gerar tarifa SERPRO")
        raise