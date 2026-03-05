import pywhatkit as kit
import pyautogui
import time
import random
import pandas as pd
import os

# 1. Configuração do Caminho (Ajustado para seu PC)
diretorio = os.path.dirname(os.path.abspath(__file__))
caminho_planilha = os.path.join(diretorio, 'leads.xlsx')

def limpar_numero(num):
    """Remove espaços, hifens e garante o +55"""
    num = str(num).strip()
    for char in [" ", "-", "(", ")", ".", ".0"]: # .0 caso o Excel trate como número
        num = num.replace(char, "")
    if not num.startswith('+'):
        num = '+' + num
    return num

try:
    # Lê a planilha
    df = pd.read_excel(caminho_planilha)
    
    # Ajuste: Deixa todos os nomes de colunas em minúsculo para evitar erro de 'Telefone' vs 'telefone'
    df.columns = [str(col).strip().lower() for col in df.columns]
    
    if 'telefone' not in df.columns:
        print(f"❌ ERRO: Não achei a coluna 'telefone'. Colunas encontradas: {list(df.columns)}")
        print("Certifique-se de que a primeira linha da planilha é a palavra: telefone")
        exit()

    lista_telefones = df['telefone'].dropna().tolist()
    print(f"✅ {len(lista_telefones)} contatos carregados com sucesso!")

except Exception as e:
    print(f"❌ Erro crítico ao abrir arquivo: {e}")
    exit()

# 2. Loop de Envio
mensagens = ["Bom dia! tudo bem?", "Olá! Como vai?", "Oi! Tudo certo?"]

for i, num_bruto in enumerate(lista_telefones):
    numero_final = limpar_numero(num_bruto)
    texto = random.choice(mensagens)
    
    try:
        print(f"[{i+1}/{len(lista_telefones)}] Enviando para: {numero_final}")
        
        # Abre e envia
        kit.sendwhatmsg_instantly(numero_final, texto, wait_time=15, tab_close=True)
        
        # Espera carregar e enviar
        time.sleep(5) 
        
        # Força o fechamento da aba
        pyautogui.hotkey('ctrl', 'w')
        
        # Intervalo entre leads
        atraso = random.randint(15, 25)
        print(f"✅ Sucesso! Aguardando {atraso}s...")
        time.sleep(atraso)

    except Exception as e:
        print(f"❌ Erro no envio para {num_bruto}: {e}")

print("\n🎯 Automação concluída!")