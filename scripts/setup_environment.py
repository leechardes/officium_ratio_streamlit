import os
import subprocess
import sys
import venv

# Obtém o caminho do diretório raiz do projeto
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def create_venv():
    venv_path = os.path.join(ROOT_DIR, "venv")
    if not os.path.exists(venv_path):
        print("Criando o ambiente virtual...")
        venv.create(venv_path, with_pip=True)
        print("Ambiente virtual criado com sucesso.")
    return venv_path


def get_venv_python(venv_path):
    if os.name == "nt":  # Windows
        return os.path.join(venv_path, "Scripts", "python.exe")
    else:  # macOS/Linux
        return os.path.join(venv_path, "bin", "python")


def install_requirements(venv_python):
    requirements_path = os.path.join(ROOT_DIR, "requirements.txt")
    if os.path.exists(requirements_path):
        print("Instalando pacotes do requirements.txt...")
        subprocess.run([venv_python, "-m", "pip", "install", "-r", requirements_path])
        print("Instalação dos pacotes concluída.")
    else:
        print("Arquivo requirements.txt não encontrado.")


def install_odbc_driver():
    if os.name == "nt":
        print(
            "Você está no Windows. Certifique-se de ter o driver ODBC instalado manualmente."
        )
        return

    if sys.platform == "darwin":
        print("Instalando o driver ODBC no macOS...")
        subprocess.run(["brew", "install", "unixodbc"])
    elif sys.platform == "linux":
        print("Instalando o driver ODBC no Linux...")
        subprocess.run(["sudo", "apt-get", "install", "unixodbc", "unixodbc-dev"])


def check_and_install_odbc_driver():
    try:
        output = subprocess.run(["odbcinst", "-j"], capture_output=True, text=True)
        print(output.stdout)
    except FileNotFoundError:
        print("odbcinst não encontrado, instalando driver ODBC...")
        install_odbc_driver()


def start_streamlit(venv_python):
    print("Iniciando o dashboard I9 Smart PDV com Streamlit...")
    streamlit_path = os.path.join(ROOT_DIR, "main.py")
    subprocess.run([venv_python, "-m", "streamlit", "run", streamlit_path])


if __name__ == "__main__":
    os.chdir(ROOT_DIR)  # Muda o diretório de trabalho para a raiz do projeto

    venv_path = create_venv()
    venv_python = get_venv_python(venv_path)

    install_requirements(venv_python)
    # check_and_install_odbc_driver()

    print("Configuração do ambiente concluída.")
    print(f"Para ativar o ambiente virtual, use:")
    if os.name == "nt":
        print(f"    {os.path.join(venv_path, 'Scripts', 'activate')}")
    else:
        print(f"    source {os.path.join(venv_path, 'bin', 'activate')}")
    print(
        "Para iniciar o dashboard, execute 'streamlit run main.py' na raiz do projeto."
    )

    # Descomente a linha abaixo se quiser iniciar o Streamlit automaticamente
    # start_streamlit(venv_python)
