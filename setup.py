"""
Script de Configuração Automática - Sistema de Triagem ODQ
Configura automaticamente o ambiente de desenvolvimento
"""

import os
import sys
from pathlib import Path


def create_env_file():
    """Cria o arquivo .env se não existir"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print("✅ Arquivo .env já existe")
        return True
    
    if env_example.exists():
        print("📝 Criando arquivo .env a partir do .env.example...")
        env_content = env_example.read_text(encoding='utf-8')
        
        # Substituir com valores do parameters.json se existir
        params_file = Path("parameters.json")
        if params_file.exists():
            import json
            try:
                params = json.loads(params_file.read_text(encoding='utf-8'))
                
                # Extrair tenant_id da authority
                authority = params.get("authority", "")
                tenant_id = authority.split("/")[-1] if authority else ""
                
                # Substituir valores
                env_content = env_content.replace(
                    "your-client-id-here", params.get("client_id", "")
                )
                env_content = env_content.replace(
                    "your-client-secret-here", params.get("secret", "")
                )
                env_content = env_content.replace(
                    "your-tenant-id-here", tenant_id
                )
                
                print("✅ Configurações do parameters.json aplicadas")
                
            except Exception as e:
                print(f"⚠️ Erro ao processar parameters.json: {e}")
        
        env_file.write_text(env_content, encoding='utf-8')
        print("✅ Arquivo .env criado com sucesso!")
        return True
    
    print("❌ Arquivo .env.example não encontrado")
    return False


def install_dependencies():
    """Instala as dependências do projeto"""
    print("\n📦 Instalando dependências...")
    
    req_file = Path("requirements.txt")
    if not req_file.exists():
        print("❌ Arquivo requirements.txt não encontrado")
        return False
    
    try:
        import subprocess
        result = subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Dependências instaladas com sucesso!")
            return True
        else:
            print(f"❌ Erro na instalação: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False


def test_configuration():
    """Testa se a configuração está funcionando"""
    print("\n🔍 Testando configuração...")
    
    try:
        # Carregar variáveis de ambiente
        from dotenv import load_dotenv
        load_dotenv()
        
        # Verificar credenciais básicas
        client_id = os.getenv("AZURE_CLIENT_ID")
        client_secret = os.getenv("AZURE_CLIENT_SECRET")
        tenant_id = os.getenv("AZURE_TENANT_ID")
        
        if not all([client_id, client_secret, tenant_id]):
            print("❌ Credenciais do Azure não configuradas")
            return False
        
        print("✅ Credenciais do Azure configuradas")
        
        # Testar imports principais
        import msal
        import requests
        print("✅ Bibliotecas principais disponíveis")
        
        return True
        
    except ImportError as e:
        print(f"❌ Biblioteca não encontrada: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro na configuração: {e}")
        return False


def main():
    """Função principal"""
    print("🚀 Sistema de Triagem ODQ - Configuração Automática")
    print("=" * 60)
    
    # Verificar se estamos no diretório correto
    if not Path("triagem-web").exists() and not Path("Triagem").exists():
        print("❌ Execute este script no diretório raiz do projeto")
        return False
    
    success = True
    
    # 1. Criar arquivo .env
    if not create_env_file():
        success = False
    
    # 2. Instalar dependências
    if not install_dependencies():
        success = False
    
    # 3. Testar configuração
    if not test_configuration():
        success = False
    
    print("\n" + "=" * 60)
    
    if success:
        print("🎉 CONFIGURAÇÃO CONCLUÍDA COM SUCESSO!")
        print("\n📋 Próximos passos:")
        print("1. ✅ Execute: python test_connection.py")
        print("2. ✅ Inicie o backend: cd triagem-web/backend && python main.py")
        print("3. ✅ Acesse: http://localhost:8000")
        print("\n🔗 Repository: https://github.com/licitaquiassessoriaoficial-creator/triagem.git")
    else:
        print("❌ CONFIGURAÇÃO FALHOU!")
        print("\n📝 Consulte CONFIGURACAO_SEGURA.md para instruções manuais")
    
    return success


if __name__ == "__main__":
    main()