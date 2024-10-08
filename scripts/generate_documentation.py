import os
import json
from datetime import datetime


# Função para carregar o arquivo de configuração
def load_config(config_path="scripts/config/generate_documentation.json"):
    with open(config_path, "r") as config_file:
        return json.load(config_file)


# Função para mapear extensões para linguagens
def detect_language(file_name):
    extension_mapping = {
        ".py": "python",
        ".json": "json",
        ".html": "html",
        ".js": "javascript",
        ".css": "css",
        ".md": "markdown",
        ".sh": "bash",
        ".yml": "yaml",
        ".yaml": "yaml",
    }
    ext = os.path.splitext(file_name)[1]  # Obter a extensão do arquivo
    return extension_mapping.get(
        ext, ""
    )  # Retornar a linguagem correspondente ou vazio se não mapeado


# Função para gerar a estrutura do projeto, considerando as configurações e identificando o último item
def generate_file_structure(
    startpath, folders_to_check, ignore_dirs, extensions_to_ignore, ignore_files_root
):
    content = "## Estrutura do Projeto\n\n```\n"

    # Processar arquivos na raiz
    root_dirs = []
    root_files = []

    for item in os.listdir(startpath):
        if item in ignore_files_root or item in ignore_dirs or item.startswith("."):
            continue
        if os.path.isdir(os.path.join(startpath, item)):
            root_dirs.append(item)
        else:
            root_files.append(item)

    # Escrever a raiz do projeto
    content += f"{os.path.basename(startpath)}/\n"

    # Processar diretórios e arquivos na raiz do projeto
    for i, item in enumerate(root_dirs + root_files):
        is_last = i == len(root_dirs) + len(root_files) - 1
        if is_last:
            content += f"└── {item}"
        else:
            content += f"├── {item}"

        if item in root_dirs:
            content += "/\n"
            content += generate_subtree(
                startpath, item, ignore_dirs, extensions_to_ignore, 1, is_last
            )
        else:
            content += "\n"

    content += "```\n"
    return content


# Função para gerar a árvore de subdiretórios e arquivos
def generate_subtree(
    startpath, directory, ignore_dirs, extensions_to_ignore, level, is_last_parent
):
    path = os.path.join(startpath, directory)
    items = os.listdir(path)
    items = [
        item for item in items if item not in ignore_dirs and not item.startswith(".")
    ]
    dirs = [item for item in items if os.path.isdir(os.path.join(path, item))]
    files = [
        item
        for item in items
        if os.path.isfile(os.path.join(path, item))
        and not any(item.endswith(ext) for ext in extensions_to_ignore)
    ]

    subtree_content = ""

    for i, item in enumerate(dirs + files):
        is_last = i == len(dirs) + len(files) - 1
        if is_last_parent:
            indent = "    " * (level - 1) + "    "
        else:
            indent = "│   " * level

        if is_last:
            subtree_content += f"{indent}└── {item}"
        else:
            subtree_content += f"{indent}├── {item}"

        if item in dirs:
            subtree_content += "/\n"
            subtree_content += generate_subtree(
                path,
                item,
                ignore_dirs,
                extensions_to_ignore,
                level + 1,
                is_last and is_last_parent,
            )
        else:
            subtree_content += "\n"

    return subtree_content


# Função para gerar o arquivo .md com a data e hora atual no nome
def generate_md_file(content, output_dir="docs"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    file_name = f"documentation_{timestamp}.md"
    file_path = os.path.join(output_dir, file_name)

    with open(file_path, "w") as md_file:
        md_file.write(content)

    print(f"Arquivo de documentação gerado: {file_path}")


# Função para obter o conteúdo dos arquivos
def get_file_content(files):
    content = "## Conteúdo dos Arquivos\n\n"
    for file in files:
        language = detect_language(file)  # Detectar a linguagem com base na extensão
        content += f"### {file}\n"
        try:
            with open(file, "r") as f:
                file_content = f.read()
                if language:
                    content += f"```{language}\n{file_content}\n```\n"
                else:
                    content += f"```\n{file_content}\n```\n"
        except Exception as e:
            content += f"Erro ao ler o arquivo: {e}\n"
    return content


# Aqui começa a unificação dos três scripts
def execute_scripts(config):
    folders_to_check = config["folders_to_check"]
    ignore_dirs = config.get("ignore_dirs", [])
    extensions_to_ignore = config.get("extensions_to_ignore", [".md"])
    ignore_files_root = config.get("ignore_files_root", [])

    content = "# Documentação Unificada\n\n"

    # Gerar estrutura dos arquivos e pastas, começando da raiz
    content += generate_file_structure(
        ".", folders_to_check, ignore_dirs, extensions_to_ignore, ignore_files_root
    )

    # Obter os arquivos a serem processados
    files_to_process = get_files_to_process(
        folders_to_check, extensions_to_ignore, ignore_files_root
    )  # Ignorar as extensões configuradas
    content += get_file_content(files_to_process)

    return content


# Função para verificar arquivos ignorando as extensões definidas
def get_files_to_process(folders_to_check, extensions_to_ignore, ignore_files_root):
    files_to_process = []

    # Processar os arquivos na raiz do projeto
    for file in os.listdir("."):
        if (
            os.path.isfile(file)
            and file not in ignore_files_root
            and not any(file.endswith(ext) for ext in extensions_to_ignore)
        ):
            files_to_process.append(os.path.join(".", file))

    # Processar as pastas configuradas
    for folder in folders_to_check:
        for root, dirs, files in os.walk(folder):
            for file in files:
                if not any(file.endswith(ext) for ext in extensions_to_ignore):
                    files_to_process.append(os.path.join(root, file))
    return files_to_process


# Função principal
def main():
    # Carregar as configurações
    config = load_config()

    # Executar os scripts e obter o conteúdo
    md_content = execute_scripts(config)

    # Gerar o arquivo de documentação
    generate_md_file(md_content)


if __name__ == "__main__":
    main()
