import asyncio
import os
import shutil
from fastapi import FastAPI, File, UploadFile, WebSocket
from typing import List
from src import gerar_todos
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.environ.get("CORS_ORIGINS", "*")],  # Permite qualquer origem, ajuste conforme necessário
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Diretorios de upload
download_dir = "./processados"
upload_dir = "./uploads"    
upload_dir_unimed = os.path.join(upload_dir, "unimed")

# Lista global de conexões WebSocket
websocket_connections = []

# WebSocket endpoint
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    websocket_connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Process incoming messages if needed
    except Exception as e:
        print(f"WebSocket connection closed: {e}")
    finally:
        websocket_connections.remove(websocket)



@app.post("/uploadfiles/")
async def upload_files(
    tabelaRefencia: UploadFile = File(...),
    tabelaAnsef: UploadFile = File(...),
    semMargemAnsef: UploadFile = File(...),
    sempreOdontoSytem: UploadFile = File(...),
    unidonto: UploadFile = File(...),
    consignacoesUnimed: UploadFile = File(...),
    tabelaDebito: UploadFile = File(...),
    contratosUnimed: List[UploadFile] = File(...)
):
    print(f"Iniciando processamento dos arquivos...")
    
    # Lista com tupla dos arquivos e já com a mudança de nome feita
    files = [
        (tabelaRefencia, "tabela_referencia.xlsx", "Tabela Referência ASPOFERN"),
        (tabelaAnsef, "tabela_ansef.xls", "Tabela ANSEF"),
        (semMargemAnsef, "tabela_sem_margem.xlsx", "Tabela dos sem margem ANSEF"),
        (sempreOdontoSytem, "tabela_planos_sempre_odontosystem.xlsx", "Plano Sempre e OdontoSystem"),
        (unidonto, "uniodonto.csv", "Plano Uniodonto"),
        (consignacoesUnimed, "consignacoes_unimed.xlsx", "Consignações Unimed"),
        (tabelaDebito, "tabela_debito.xlsx", "Tabela Débito")
    ]
   
    try:
        print("Verificando diretório de upload...")
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
            print(f"Diretório criado: {upload_dir}")
    except Exception as e:
        erro = f"Erro ao criar diretório de upload: {str(e)}"
        print(erro)
        return {
            "status": 500, 
            "message": erro,
            "error": str(e),
            "file": "diretório de upload"
        }

    # Salva cada arquivo no diretório com nomes específicos
    for file, new_name, display_name in files:
        try:
            print(f"Processando arquivo: {display_name}")
            contents = await file.read()
            file_path = os.path.join(upload_dir, new_name)
            with open(file_path, "wb") as f:
                f.write(contents)
            print(f"Arquivo salvo: {file_path}")
        except Exception as e:
            erro = f"Erro ao processar arquivo {display_name}: {str(e)}"
            print(erro)
            return {
                "status": 500, 
                "message": erro,
                "error": str(e),
                "file": display_name
            }
    
    # Cria diretório para salvar os contratos da Unimed
    try:
        if os.path.exists(upload_dir_unimed):
            shutil.rmtree(upload_dir_unimed)
        os.makedirs(upload_dir_unimed)
    except Exception as e:
        return {
            "status": 500, 
            "message": "Erro ao gerenciar diretório dos contratos Unimed",
            "error": str(e),
            "file": "diretório Unimed"
        }

    # Salva cada arquivo de contrato da Unimed no diretório
    for contrato in contratosUnimed:
        try:
            contents = await contrato.read()
            with open(os.path.join(upload_dir_unimed, contrato.filename), "wb") as f:
                f.write(contents)
        except Exception as e:
            return {
                "status": 500, 
                "message": f"Erro ao processar contrato Unimed",
                "error": str(e),
                "file": contrato.filename
            }
    
    try:
        print("Iniciando processamento dos dados...")
        task = asyncio.create_task(gerar_todos.gerar_todos())
        result = await task
        print("Processamento concluído com sucesso!")
        
        # Notify all connected clients via WebSocket
        for connection in websocket_connections:
            await connection.send_text("Processing complete")
        
        return {
            "status": 200,
            "message": "Upload e processamento realizados com sucesso",
            "data": result
        }
    except Exception as e:
        erro = f"Erro durante o processamento dos dados: {str(e)}"
        print(erro)
        return {
            "status": 500,
            "message": erro,
            "error": str(e),
            "file": "processamento geral"
        }
    
@app.get("/download/{filename}")
async def download_file(filename: str):
    print(f"Procurando arquivo: {filename}")
    print(f"Diretório de download: {download_dir}")
    file_path = os.path.join(download_dir, filename)
    print(f"Caminho completo: {file_path}")
    
    if os.path.exists(file_path):
        print(f"Arquivo encontrado em: {file_path}")
        return FileResponse(path=file_path, filename=filename, media_type='application/octet-stream')
    else:
        print(f"Arquivo não encontrado em: {file_path}")
        return {"status": 404, "message": "File not found"}