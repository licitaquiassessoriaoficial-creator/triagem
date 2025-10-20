#!/usr/bin/env python3
"""
Teste do Sistema de Triagem ODQ - Email
Testa a funcionalidade de puxar emails da odequadroservicos.com.br
"""

import sys
from pathlib import Path

from confidential_client_secret_sample import (
    load_config, get_token, fetch_messages,
    list_attachments, download_attachment
)

# Adicionar o diretório principal ao PATH
sys.path.append('.')


def testar_conexao_email():
    """Testa a conexão com o Microsoft Graph para puxar emails"""
    
    print("🔧 Teste do Sistema de Triagem ODQ - Email")
    print("=" * 50)
    
    try:
        # Carregar configuração
        config_path = Path("parameters.json")
        if not config_path.exists():
            print("❌ Arquivo parameters.json não encontrado!")
            return False
            
        print("✅ Carregando configuração...")
        config = load_config(str(config_path))
        
        # Verificar dados da configuração
        default_email = "izabella.cordeiro@odequadroservicos.com.br"
        user_email = config.get("user_email", default_email)
        print(f"📧 Email alvo: {user_email}")
        
        # Obter token
        print("🔑 Obtendo token de acesso...")
        token = get_token(config)
        print("✅ Token obtido com sucesso!")
        
        # Buscar mensagens
        print("📬 Buscando emails com anexos...")
        # Limitar para teste
        endpoint_test = config["endpoint"].replace("$top=999", "$top=5")
        messages = fetch_messages(
            endpoint_test, token, timeout=30, max_retries=2
        )
        
        print(f"✅ Encontrados {len(messages)} emails")
        
        if messages:
            # Testar primeiro email com anexos
            for i, msg in enumerate(messages[:3]):
                msg_id = msg.get('id')
                subject = msg.get('subject', 'Sem assunto')
                
                print(f"\n📨 Email {i+1}: {subject[:50]}...")
                
                if msg.get('hasAttachments'):
                    # Listar anexos
                    attachments = list_attachments(user_email, msg_id, token)
                    print(f"   📎 Anexos encontrados: {len(attachments)}")
                    
                    # Limitar a 2 anexos por teste
                    for j, att in enumerate(attachments[:2]):
                        attachment_type = '#microsoft.graph.fileAttachment'
                        if att.get('@odata.type') == attachment_type:
                            fname = att.get('name', f'anexo_{j}')
                            print(f"     - {fname}")
                            
                            # Testar download (só os primeiros bytes)
                            try:
                                fname_dl, data_dl, ctype = download_attachment(
                                    user_email, msg_id, att['id'], token
                                )
                                if data_dl:
                                    bytes_len = len(data_dl)
                                    print(f"     ✅ Download OK: "
                                          f"{bytes_len} bytes")
                                    break  # Apenas um download para teste
                            except Exception as e:
                                print(f"     ⚠️  Erro no download: {e}")
                else:
                    print("   📎 Nenhum anexo")
                    
        print("\n🎉 Teste concluído com sucesso!")
        print(f"✅ Conectado à conta: {user_email}")
        print(f"✅ Emails acessíveis: {len(messages)}")
        return True
        
    except Exception as e:
        print(f"\n❌ Erro no teste: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    sucesso = testar_conexao_email()
    sys.exit(0 if sucesso else 1)