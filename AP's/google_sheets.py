import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
# Nome do arquivo token
Nome_do_token = "token.json"
# Nome do arquivo credenciais
Nome_das_credenciais = "credenciais.json"
# Escopos para autenticação
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
# ID da planilha
ID_DA_PLANILHA = "1GLzoK827r47xqDQmC6aRcGqJSEty8yj9UM5iwC1CNT0"
# Intervalo de células para leitura
INTERVALO_DE_CELULAS = "Página1!A1:B1000"
school_name = input("Digite o nome da escola, sem caracteres especiais e com letras maiúsuclas (ç, ~, ^) ex: ECIT_GRACILIANO_E_LORDAO: ")
cabeçalho_row_A, cabeçalho_row_B = "Nome da escola", "MAC DO AP".strip()
def read_cisco_macs_from_file(file_path):
    macs = []
    # Lê os MACs do arquivo e os armazena em uma lista
    with open(file_path, 'r') as file:
        for line in file:
            macs.append(line.strip())
    return macs
def get_credentials():
    creds = None
    if os.path.exists(Nome_do_token):
        creds = Credentials.from_authorized_user_file(Nome_do_token, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(Nome_das_credenciais, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(Nome_do_token, "w") as token:
            token.write(creds.to_json())
    return creds
def write_to_sheet(service, spreadsheet_id, range_to_write, values):
    body = {
        "values": values
    }
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=range_to_write,
        valueInputOption="RAW",
        body=body
    ).execute()
def main():
    """Função principal do script."""
    try:
        creds = get_credentials()    
        # Construir o serviço do Google Sheets
        service = build("sheets", "v4", credentials=creds)
        sheet = service.spreadsheets()
        # Verificar se o nome da escola já existe na coluna A
        result_row_B = sheet.values().get(spreadsheetId=ID_DA_PLANILHA, range="Página1!B:B").execute()
        existing_values_row_B = result_row_B.get("values", []) # Encontrar a próxima célula vazia na coluna B
        last_row_index_row_B = len(existing_values_row_B)
        print(last_row_index_row_B)
             # Ler os MACs do arquivo
        macs = read_cisco_macs_from_file("Macs.txt")
        for i, mac in enumerate(macs, start=1):
            if [mac] not in existing_values_row_B:
                range_to_write_row_B = f"Página1!B{last_row_index_row_B + i + 1}"
                write_to_sheet(service, ID_DA_PLANILHA, range_to_write_row_B, [[mac]])
                print(f"O MAC '{mac}' foi adicionado na célula {range_to_write_row_B} da coluna B.")
                cabeçalho_range_row_B = f"Página1!B{last_row_index_row_B + 1}"
                write_to_sheet(service, ID_DA_PLANILHA, cabeçalho_range_row_B, [[cabeçalho_row_B]])     
        result_row_A = sheet.values().get(spreadsheetId=ID_DA_PLANILHA, range="Página1!A:A").execute()
        existing_values_row_A = result_row_A.get("values", [])
        #Verifica se o nome da escola já está presente na planilha.
        if [school_name] not in existing_values_row_A:
            last_row_index_row_A = last_row_index_row_B
            range_to_write = f"Página1!A{last_row_index_row_A + 2 }"
            write_to_sheet(service, ID_DA_PLANILHA, range_to_write, [[school_name]])
            print(f"O nome da escola '{school_name}' foi adicionado à última linha da coluna A.")
            # Escrever o cabeçalho "Nome da escola" na célula anterior à linha dos mac's
            cabeçalho_range_row_A = f"Página1!A{last_row_index_row_A  + 1}"
            write_to_sheet(service, ID_DA_PLANILHA, cabeçalho_range_row_A, [[cabeçalho_row_A]])
        if not existing_values_row_A:
            print("No data found.")
            return  
    except HttpError as err:
        print(err)
if __name__ == "__main__":
    main()