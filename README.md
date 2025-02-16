# Configurando o ambiente
**1- Criar venv python**

    py -m venv .venv
**2- Ativar ambiente de desenvolvimento**

Windows CMD

    .venv\Scripts\activate.bat

Windows Powershell

	.venv\Scripts\Activate.ps1
	
 Linux

    .venv\Scripts\activate

**3- Baixar depêndencias**

    pip install -r requeriments.txt
**4-  Executar API**

    uvicorn api:app --reload
# Endpoints da API
* **POST /uploadfiles/**
	* Espera receber 7 parametros (tabelaRefencia, tabelaAnsef, semMargemAnsef, sempreOdontoSytem, unidonto, consignacoesUnimed, contratosUnimed)
	* Os 6 primeiros são input padrão, apenas um arquivo por input
	* O último input tem o atributo multiple no HTML, servirá para os contratos da Unimed
* **GET /download/{filename}**
	- filename: Nome do arquivo final gerado pelo sistema, fica localizado em arquivos_exportados

# Realizando Testes na API
Pode ser feito com o arquivo index.html, basta abrir o arquivo no navegador e  preencher com os arquivos solicitados e enviar, ao terminar de gerar a planilha geral de importação, o download será iniciado automaticamente.