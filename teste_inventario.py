import os
import time
import platform
import psutil
import json

# Intervalo de tempo para coleta de informações (em segundos)
INTERVALO = 60

def get_system_info():
    return {
        "sistema_operacional": platform.system(),
        "versao_sistema_operacional": platform.release(),
        "processador": platform.processor(),
        "memoria_total": psutil.virtual_memory().total,
        "memoria_livre": psutil.virtual_memory().available,
        "ip_externo": psutil.net_if_addrs().get("lo", [{"address": "N/A"}])[0].address
    }

def get_internal_ip():
    try:
        network_info = psutil.net_if_addrs()

        # Verifica se há pelo menos duas interfaces de rede
        if len(network_info) < 2:
            raise Exception("Menos de duas interfaces de rede encontradas.")

        # Obtém o IP da segunda interface de rede
        internal_ip = network_info[1].address
        return internal_ip
    except Exception as e:
        print(f"Erro ao obter o IP interno: {e}")
        return "N/A"

def get_network_info():
    return {
        "latencia": psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv,
        "ip_interno": get_internal_ip()
    }

def clear_screen():
    os.system("cls" if platform.system() == "Windows" else "clear")

def write_to_file(info, filename="info.txt"):
    with open(filename, "a") as file:
        file.write(json.dumps(info) + "\n")

if __name__ == "__main__":
    while True:
        system_info = get_system_info()
        network_info = get_network_info()

        # Escreve as informações em um arquivo
        write_to_file(system_info)
        write_to_file(network_info)

        time.sleep(INTERVALO)
        clear_screen()  # Limpa a tela antes de coletar novas informações
