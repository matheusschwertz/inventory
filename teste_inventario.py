import time
import platform
import psutil
import requests
import json

# Intervalo de tempo para envio de informações (em segundos)
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

def send_info(info):
    # Converte o dicionário em JSON
    json_data = json.dumps(info)

    # Envia a requisição HTTP POST
    requests.post("http://192.168.104.5:5000", data=json_data)

if __name__ == "__main__":
    while True:
        system_info = get_system_info()
        network_info = get_network_info()

        # Envia as informações para o servidor
        send_info(system_info)
        send_info(network_info)

        time.sleep(INTERVALO)
