import time
import serial

def send_command(ser, comando):
    ser.write((comando + "\n").encode())
    try:
        resposta = ser.readline().decode('utf-8').strip()
        print(f"Resposta recebida: {resposta}")
    except UnicodeDecodeError:
        print("Erro de decodificação UTF-8. Dados recebidos ignorados.")

def read_serial_response(ser):
    try:
        resposta = ser.readline().decode('utf-8').strip()
        print(f"Resposta recebida: {resposta}")
        return resposta
    except UnicodeDecodeError:
        print("Erro de decodificação UTF-8. Dados recebidos ignorados.")
def create_archive(mac_address):
    try:
            with open("Macs.txt", "a+") as arquivo:
                arquivo.seek(0)
                linhas = arquivo.readline()
                if mac_address not in linhas:
                    arquivo.write(mac_address + "\n")
                    print(f"O mac address: {mac_address} foi escrito com sucesso.")
                else:
                    print("Não foi possível escrever.")
    except:
        print("Não foi possível escrever no arquivo")
mac_address = None
# Pede ao usuário para inserir a porta serial (ex: COM1)
serial_port = input("Digite a porta serial (ex: COM1): ")
# Configuração da porta serial
ser = serial.Serial(serial_port, 9600, timeout=0.5)
time.sleep(2)  # Aguarde para garantir que a porta esteja pronta
# Variável para controlar se a tecla ENTER já foi enviada
tecla_enter_enviada = False
while True:
    resposta = read_serial_response(ser)
    if resposta is not None:  # Verifica se a resposta não é None
        if "Press RETURN to get started!" in resposta:
            send_command(ser, "\r\n")
            print("Tecla ENTER enviada.")
            time.sleep(1)
            # Código para pegar apenas o Mac address e adicioná-lo a uma lista
        elif "Base ethernet MAC Address:" in resposta:
            mac_address = resposta.split(': ')[1]
            print(mac_address)
            create_archive(mac_address=mac_address)
            time.sleep(1.5)
        elif "Username:" in resposta or "Password:" in resposta:
            send_command(ser, "Cisco")
            time.sleep(1)
        elif "%Error opening tftp://255.255.255.255/ap1g2-k9w7-tar.default (connection timed out)ap:" in resposta:
            send_command(ser, "dir flash:")
            time.sleep(1)
        elif "ap:" in resposta:
            send_command(ser, "delete flash:private-multiple-fs")
            time.sleep(1)
        elif 'Are you sure you want to delete "flash:private-multiple-fs" (y/n)?' in resposta:
            send_command(ser, "y")
            time.sleep(1)
        elif 'Are you sure you want to reset the system (y/n)?' in resposta:
            send_command(ser, "y")
            time.sleep(1)
        elif 'File "flash:private-multiple-fs" deleted' in resposta:
            send_command(ser, "reset")
            time.sleep(1)
        elif "AP" in resposta and ">" in resposta:
            send_command(ser, "enable")
            time.sleep(1)
        elif "AP" in resposta and "#" in resposta:
            send_command(ser, "capwap ap controller ip address 'Insira aqui o ip da sua controladora.'")
            if "AP" in resposta and "#" in resposta and "!" in resposta:
                break
        elif "Press RETURN to get started!" in resposta and not tecla_enter_enviada:
            send_command(ser, "\r\n")
            print("Tecla ENTER enviada.")
            tecla_enter_enviada = True  # Marcar que a tecla ENTER foi enviada
            time.sleep(1.5)
    else:
        # Se a resposta for None, continue para a próxima iteração
        continue
