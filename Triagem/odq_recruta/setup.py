#!/usr/bin/env python3
"""
Script de setup para ODQ Recruta
"""
import os
import sys
import subprocess
from pathlib import Path

def run_command(command, description):
    """Executa um comando e trata erros"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} concluído")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro em {description}: {e}")
        print(f"   Saída: {e.stdout}")
        print(f"   Erro: {e.stderr}")
        return False

def check_python_version():
    """Verifica se a versão do Python é compatível"""
    if sys.version_info < (3, 10):
        print("❌ Python 3.10+ é necessário")
        print(f"   Versão atual: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} - OK")
    return True

def install_dependencies():
    """Instala as dependências do projeto"""
    if not run_command("pip install -r requirements.txt", "Instalando dependências"):
        return False
    return True

def create_env_file():
    """Cria arquivo .env se não existir"""
    env_path = Path(".env")
    example_path = Path("env_example.txt")
    
    if env_path.exists():
        print("✅ Arquivo .env já existe")
        return True
    
    if example_path.exists():
        print("📝 Copiando env_example.txt para .env...")
        with open(example_path, "r", encoding="utf-8") as f:
            content = f.read()
        with open(env_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("✅ Arquivo .env criado")
        print("⚠️  IMPORTANTE: Configure suas credenciais no arquivo .env")
        return True
    else:
        print("❌ Arquivo env_example.txt não encontrado")
        return False

def create_directories():
    """Cria diretórios necessários"""
    directories = ["logs", ".odq_cache", ".odq_temp"]
    for dir_name in directories:
        Path(dir_name).mkdir(exist_ok=True)
    print("✅ Diretórios criados")

def run_tests():
    """Executa testes básicos"""
    print("🧪 Executando testes...")
    if run_command("python -m pytest tests/ -v", "Testes"):
        print("✅ Todos os testes passaram")
        return True
    else:
        print("⚠️  Alguns testes falharam, mas o sistema pode funcionar")
        return True

def main():
    """Função principal do setup"""
    print("🚀 Setup do ODQ Recruta")
    print("=" * 50)
    
    # Verificar Python
    if not check_python_version():
        sys.exit(1)
    
    # Instalar dependências
    if not install_dependencies():
        print("❌ Falha na instalação das dependências")
        sys.exit(1)
    
    # Criar arquivo .env
    if not create_env_file():
        print("❌ Falha na criação do arquivo .env")
        sys.exit(1)
    
    # Criar diretórios
    create_directories()
    
    # Executar testes
    run_tests()
    
    print("\n" + "=" * 50)
    print("✅ Setup concluído com sucesso!")
    print("\n📋 Próximos passos:")
    print("1. Configure suas credenciais no arquivo .env")
    print("2. Execute: python app.py")
    print("\n📖 Para mais informações, consulte o README.md")

if __name__ == "__main__":
    main()

