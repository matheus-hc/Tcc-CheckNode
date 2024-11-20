import requests
import os
from datetime import datetime
from email_sender import check_and_send_email


def get_latest_node_version():
    try:
        response = requests.get("https://nodejs.org/dist/index.json")
        if response.status_code == 200:
            latest_version = response.json()[0]["version"]
            return latest_version.strip("v")
    except Exception as e:
        print("Erro ao obter a versão mais recente do Node.js:", e)
    return None


def get_repo_node_version(repo_url):
    package_json_url = f"{repo_url}/raw/main/package.json"
    try:
        response = requests.get(package_json_url)
        if response.status_code == 200:
            package_data = response.json()
            if "engines" in package_data and "node" in package_data["engines"]:
                return package_data["engines"]["node"].strip("v")
            else:
                return "NO_NODE_INFO"  
        else:
            return "NO_PACKAGE_JSON"  
    except Exception as e:
        print("Erro ao acessar o repositório:", e)
        return "NO_PACKAGE_JSON"


def check_repo_version(repo_url, repo_name, user_email):
    latest_version = get_latest_node_version()
    repo_node_version = get_repo_node_version(repo_url)

    if not latest_version:
        print("Erro ao buscar a versão mais recente do Node.js.")
        return

    
    if repo_node_version == "NO_PACKAGE_JSON":
        subject = f"[{repo_name}] Aviso: package.json ausente"
        message = f"O repositório {repo_name} não contém um arquivo package.json."
        check_and_send_email(user_email, subject, message)

    elif repo_node_version == "NO_NODE_INFO":
        subject = f"[{repo_name}] Aviso: Versão do Node.js não especificada"
        message = f"O repositório {repo_name} não especifica uma versão do Node.js no campo 'engines' do package.json."
        check_and_send_email(user_email, subject, message)

    elif repo_node_version != latest_version:
        subject = f"[{repo_name}] Atualização do Node.js necessária"
        message = (f"O repositório {repo_name} está usando uma versão desatualizada do Node.js ({repo_node_version}). "
                   f"A versão mais recente é {latest_version}. Considere atualizar.")
        check_and_send_email(user_email, subject, message)

    else:
        subject = f"[{repo_name}] Repositório atualizado"
        message = f"O repositório {repo_name} está usando a versão mais recente do Node.js ({latest_version})."
        check_and_send_email(user_email, subject, message)


