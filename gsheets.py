import pandas as pd
import requests
import os
import re

def baixar_e_ler_planilha(diretorio):
    """
    Pede o ID/Link da planilha ao usuário, faz o download via Google Sheets API (Export)
    e retorna o DataFrame do pandas junto com o caminho local onde o arquivo foi salvo.
    """
    print("\n--- Configuração da Base de Leads ---")
    entrada_usuario = input(
        "Digite o Link ou o ID da planilha do Google Sheets (precisa estar como 'Qualquer pessoa com o link'): "
    ).strip()

    # Expressão regular para extrair apenas o ID único do link fornecido
    match = re.search(r"/d/([a-zA-Z0-9-_]+)", entrada_usuario)
    if match:
        sheet_id = match.group(1)
    else:
        sheet_id = entrada_usuario

    # Monta a URL de exportação direta do arquivo no formato XLSX
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx"

    arquivo_planilha_local = os.path.join(diretorio, "leads_local.xlsx")

    try:
        print("\nBaixando a planilha do Google Sheets para uso local...")
        resposta = requests.get(url)
        if resposta.status_code == 200:
            with open(arquivo_planilha_local, "wb") as f:
                f.write(resposta.content)
            print("✅ Download concluído e salvo como 'leads_local.xlsx'!")
        else:
            print(f"❌ Falha ao baixar a planilha. HTTP Status: {resposta.status_code}")
            exit(1)

        print("\nLendo os dados transferidos para o arquivo local...")
        df = pd.read_excel(arquivo_planilha_local)

        df.columns = [str(col).strip().lower() for col in df.columns]

        print("✅ Conexão bem-sucedida!")
        print(f"📊 Colunas localizadas: {', '.join(df.columns)}")
        print(f"👥 Total de contatos identificados: {len(df)}")

        if "phone" not in df.columns:
            print("\n❌ ERRO: Coluna 'phone' não encontrada. Verifique o cabeçalho na sua planilha.")
            exit(1)

        # Cria a coluna 'status' caso ela não exista na planilha
        if "status" not in df.columns:
            df["status"] = ""
            
        # Força a coluna a ser do tipo object para aceitar strings e evitar TypeError com floats
        df["status"] = df["status"].astype("object")

        return df, arquivo_planilha_local

    except Exception as e:
        print(f"\n❌ Erro ao carregar planilha do Google Sheets: {e}")
        exit(1)
