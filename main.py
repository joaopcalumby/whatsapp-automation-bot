import os
from gsheets import baixar_e_ler_planilha
from whatsapp_bot import iniciar_disparos

def main():
    print("====================================")
    print("   🚀 WHATSAPP LEAD AUTOMATOR 🚀    ")
    print("====================================\n")

    diretorio = os.path.dirname(os.path.abspath(__file__))
    
    # 1. Obter e ler a planilha do Google Sheets
    df, arquivo_planilha_local = baixar_e_ler_planilha(diretorio)

    # 2. Configurar o limite de envios
    print("\n" + "-" * 50)
    print("--- Configuração de Limite ---")
    limite_input = input("Quantos leads você quer contatar nesta sessão? (Aperte ENTER para enviar a todos): ").strip()
    limite_envios = int(limite_input) if limite_input.isdigit() else None

    if limite_envios:
        print(f"📌 O bot enviará mensagens para no máximo {limite_envios} lead(s) não contatado(s).")
    else:
        print("📌 O bot enviará mensagens para todos os leads pendentes da planilha, sem limite.")

    print("\n" + "-" * 50)
    confirmacao = input("Tudo certo! Podemos iniciar os disparos de mensagens? (s/n): ").strip().lower()
    
    if confirmacao != "s":
        print("Processamento cancelado.")
        exit(0)

    print("\n⚠️ AVISO: O progresso será salvo localmente no arquivo 'leads_local.xlsx'. Assim, você poderá copiar os dados atualizados para a nuvem.\n")

    # 3. Iniciar o disparo pelo WhatsApp Web
    iniciar_disparos(df, arquivo_planilha_local, diretorio, limite_envios)

if __name__ == "__main__":
    main()
