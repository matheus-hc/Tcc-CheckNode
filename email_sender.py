import requests
from email.mime.text import MIMEText
from smtplib import SMTP_SSL
from config import Config

def get_latest_node_version():
    try:
        response = requests.get("https://nodejs.org/dist/index.json", timeout=10)
        response.raise_for_status()
        latest_version = response.json()[0]["version"]
        return latest_version.strip("v")
    except requests.RequestException as e:
        print("Erro ao buscar a versão mais recente do Node.js:", e)
        return None

def get_repo_node_version(repo_url):
    package_json_url = f"{repo_url}/raw/main/package.json"
    try:
        response = requests.get(package_json_url, timeout=10)
        response.raise_for_status()
        package_data = response.json()
        if "engines" in package_data and "node" in package_data["engines"]:
            return package_data["engines"]["node"].strip("v")
        else:
            return "NO_NODE_INFO"
    except requests.RequestException as e:
        print("Erro ao acessar o repositório:", e)
        return "NO_PACKAGE_JSON"

def check_and_send_email(repo_name, repo_url, user_email, current_version):
    latest_version = get_latest_node_version()
    repo_node_version = get_repo_node_version(repo_url)

    if not latest_version:
        print("Erro ao buscar a versão mais recente do Node.js.")
        return

    if repo_node_version == "NO_PACKAGE_JSON":
        subject = "Aviso: package.json ausente no repositório"
        message = f"O repositório {repo_name} não contém um arquivo package.json."
    elif repo_node_version == "NO_NODE_INFO":
        subject = "Aviso: Versão do Node.js não especificada"
        message = f"O repositório {repo_name} não especifica uma versão do Node.js no campo 'engines' do package.json."
    elif repo_node_version == latest_version:
        subject = "Seu repositório está atualizado com o Node.js"
        message = f"O repositório {repo_name} está usando a versão mais recente do Node.js ({latest_version})."
    else:
        subject = "Atualização do Node.js necessária"
        message = (f"O repositório {repo_name} está usando uma versão desatualizada do Node.js ({repo_node_version}). "
                   f"A versão mais recente é {latest_version}. Considere atualizar.")

    send_email(user_email, subject, message)

def send_email(to_email, subject, message):
    try:
        if not Config.MAIL_USERNAME or not Config.MAIL_PASSWORD:
            print("Erro: credenciais de e-mail não configuradas.")
            return

        msg = MIMEText(message, 'plain', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = Config.MAIL_USERNAME
        msg['To'] = to_email

        with SMTP_SSL(Config.MAIL_SERVER, Config.MAIL_PORT) as server:
            server.login(Config.MAIL_USERNAME, Config.MAIL_PASSWORD)
            server.sendmail(Config.MAIL_USERNAME, to_email, msg.as_string())
            print(f"E-mail enviado com sucesso para {to_email}")
    except Exception as e:
        print("Erro ao enviar e-mail:", e)
