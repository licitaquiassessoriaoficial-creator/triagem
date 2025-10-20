// Sistema de Triagem ODQ - Frontend JavaScript
// Funcionalidades equivalentes ao sistema desktop

class TriagemSystem {
    constructor() {
        // URL dinâmica: local para desenvolvimento, Railway para produção
        this.API_BASE_URL = window.location.hostname === 'localhost' 
            ? 'http://localhost:8000' 
            : 'https://triagem-production.up.railway.app';
        this.currentJobId = null;
        this.logEntries = [];
        this.modoOffline = false; // Modo offline/simulação
        this.initializeEventListeners();
        this.initializeTimestamp();
        this.testBackendConnection();
    }

    initializeEventListeners() {
        // Form submission
        document.getElementById('triagem-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.executarTriagem();
        });

        // Clear form
        document.getElementById('limpar-form').addEventListener('click', () => {
            this.limparFormulario();
        });

        // Open approved folder
        document.getElementById('abrir-aprovados').addEventListener('click', () => {
            this.abrirAprovados();
        });

        // Email triagem
        document.getElementById('triagem-email').addEventListener('click', () => {
            this.executarTriagemEmail();
        });

        // Log controls
        document.getElementById('limpar-log').addEventListener('click', () => {
            this.limparLog();
        });

        document.getElementById('download-log').addEventListener('click', () => {
            this.downloadLog();
        });

        // Results actions
        document.getElementById('download-aprovados')?.addEventListener('click', () => {
            this.downloadAprovados();
        });

        document.getElementById('ver-aprovados')?.addEventListener('click', () => {
            this.verAprovados();
        });

        document.getElementById('nova-triagem')?.addEventListener('click', () => {
            this.novaTriagem();
        });
    }

    initializeTimestamp() {
        const timestampElement = document.querySelector('.log-entry .timestamp');
        if (timestampElement) {
            timestampElement.textContent = new Date().toLocaleTimeString();
        }
        
        // Definir data atual como padrão
        const dataInput = document.getElementById('data-filtro');
        if (dataInput) {
            const hoje = new Date();
            const ano = hoje.getFullYear();
            const mes = String(hoje.getMonth() + 1).padStart(2, '0');
            const dia = String(hoje.getDate()).padStart(2, '0');
            dataInput.value = `${ano}-${mes}-${dia}`;
        }
    }

    // Testar conexão com backend
    async testBackendConnection() {
        try {
            const response = await fetch(`${this.API_BASE_URL}/health`, {
                method: 'GET',
                timeout: 5000
            });
            if (response.ok) {
                const data = await response.json();
                this.addLogEntry('info', `✅ Backend conectado: ${data.message}`);
                this.modoOffline = false;
            } else {
                throw new Error('Backend não respondeu corretamente');
            }
        } catch (error) {
            this.addLogEntry('warning', `⚠️ Backend indisponível - Modo simulação ativado`);
            this.addLogEntry('info', `📴 Simulando triagem offline para demonstração`);
            this.modoOffline = true;
        }
    }

    // Executar Triagem - Igual ao sistema desktop
    async executarTriagem() {
        this.addLogEntry('info', '🚀 Iniciando Triagem (igual sistema desktop)...');
        // Verificar se está no modo offline
        if (this.modoOffline) {
            this.addLogEntry('info', '📴 Executando simulação offline');
            await this.executarTriagemSimulada();
        } else {
            // Redirecionar para triagem email que processa dados reais
            await this.sleep(500);
            this.executarTriagemEmail();
        }
    }

    // Simulação de triagem offline
    async executarTriagemSimulada() {
        this.addLogEntry('info', '🎭 MODO SIMULAÇÃO - Demonstração das funcionalidades');
        
        const data = this.getFormDataEmail();
        if (!this.validateFormEmail(data)) return;

        this.showLoading(true);
        this.updateLoadingMessage('Simulando triagem de currículos...');

        // Simular etapas
        this.updateProgress(10);
        this.addLogEntry('info', '🔗 [SIMULAÇÃO] Conectando ao Microsoft Graph...');
        await this.sleep(1000);

        this.updateProgress(30);
        this.addLogEntry('info', '📧 [SIMULAÇÃO] Processando emails do domínio @odequadroservicos.com.br');
        await this.sleep(1500);

        this.updateProgress(50);
        this.addLogEntry('info', '📎 [SIMULAÇÃO] Encontrados 15 emails com anexos');
        await this.sleep(1000);

        this.updateProgress(70);
        this.addLogEntry('info', '🔍 [SIMULAÇÃO] Analisando currículos com OCR...');
        await this.sleep(1500);

        this.updateProgress(90);
        this.addLogEntry('info', '✅ [SIMULAÇÃO] Aplicando critérios de triagem...');
        await this.sleep(1000);

        // Resultado simulado
        const resultadoSimulado = {
            success: true,
            message: "Triagem simulada concluída",
            total_processados: 15,
            total_aprovados: 4,
            percentual_aprovacao: 26.7,
            arquivos_aprovados: [
                {
                    arquivo: "curriculum_joao_silva.pdf",
                    email_assunto: "Candidatura para vaga de Desenvolvedor",
                    email_origem: "joao.silva@email.com",
                    formacoes_encontradas: ["Engenharia de Software", "Ciência da Computação"],
                    tamanho_texto: 1250,
                    ocr_usado: true
                },
                {
                    arquivo: "cv_maria_santos.docx",
                    email_assunto: "Interesse na vaga Python",
                    email_origem: "maria.santos@email.com",
                    formacoes_encontradas: ["Sistemas de Informação"],
                    tamanho_texto: 980,
                    ocr_usado: false
                },
                {
                    arquivo: "curriculo_pedro_costa.pdf",
                    email_assunto: "Aplicação para desenvolvedor backend",
                    email_origem: "pedro.costa@email.com",
                    formacoes_encontradas: ["Engenharia da Computação"],
                    tamanho_texto: 1350,
                    ocr_usado: true
                },
                {
                    arquivo: "cv_ana_oliveira.pdf",
                    email_assunto: "Vaga de programador",
                    email_origem: "ana.oliveira@email.com",
                    formacoes_encontradas: ["Tecnologia em Sistemas"],
                    tamanho_texto: 1100,
                    ocr_usado: true
                }
            ],
            detalhes_usuarios: [
                { email: "rh@odequadroservicos.com.br", name: "RH Geral", emails_count: 8 },
                { email: "recrutamento@odequadroservicos.com.br", name: "Recrutamento", emails_count: 7 }
            ]
        };

        this.updateProgress(100);
        this.addLogEntry('info', '🎉 [SIMULAÇÃO] Triagem concluída!');
        this.addLogEntry('info', `📧 Total de currículos processados: ${resultadoSimulado.total_processados}`);
        this.addLogEntry('info', `✅ Currículos aprovados: ${resultadoSimulado.total_aprovados}`);
        this.addLogEntry('info', `📊 Taxa de aprovação: ${resultadoSimulado.percentual_aprovacao}%`);

        // Mostrar currículos aprovados
        this.addLogEntry('info', '📋 Lista de currículos aprovados (simulação):');
        resultadoSimulado.arquivos_aprovados.forEach((arquivo, index) => {
            const formacoes = arquivo.formacoes_encontradas.join(', ');
            this.addLogEntry('info', `✅ ${index + 1}. ${arquivo.arquivo}`);
            this.addLogEntry('info', `   📚 Formações: ${formacoes}`);
            this.addLogEntry('info', `   📧 Origem: ${arquivo.email_origem}`);
        });

        this.addLogEntry('info', '💡 Esta é uma demonstração. O sistema real processaria emails do Microsoft Graph.');
        
        setTimeout(() => {
            this.showLoading(false);
            this.showResultsEmail(resultadoSimulado);
        }, 1000);
    }

    getFormData() {
        return {
            email: document.getElementById('email').value.trim(),
            vagaDesc: document.getElementById('vaga-desc').value.trim(),
            keywords: document.getElementById('keywords').value.trim(),
            formacoes: document.getElementById('formacoes').value.trim(),
            negativas: document.getElementById('negativas').value.trim(),
            dataFiltro: document.getElementById('data-filtro').value,
            maxEmails: parseInt(document.getElementById('max-emails').value) || 500,
            usarOcr: document.getElementById('usar-ocr').checked
        };
    }

    validateForm(data) {
        if (!data.email || !data.vagaDesc || !data.keywords) {
            this.addLogEntry('error', 'Preencha o email, descrição da vaga e palavras-chave.');
            return false;
        }

        // Validar formato do email
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(data.email)) {
            this.addLogEntry('error', 'Formato de email inválido.');
            return false;
        }

        return true;
    }

    // Executar Triagem por Email ODQ (comportamento desktop)
    async executarTriagemEmail() {
        const formData = this.getFormDataEmail();
        
        if (!this.validateFormEmail(formData)) {
            return;
        }

        this.showLoading(true);
        
        if (this.modoOffline) {
            this.addLogEntry('info', '📴 Executando triagem em modo simulação...');
            await this.executarTriagemSimulada();
        } else {
            this.addLogEntry('info', '🌐 Iniciando triagem de emails (sistema online)...');
            try {
                await this.processarTriagemEmail(formData);
            } catch (error) {
                this.addLogEntry('error', `❌ Erro na triagem: ${error.message}`);
                this.addLogEntry('info', '🔄 Alternando para modo simulação...');
                this.modoOffline = true;
                await this.executarTriagemSimulada();
            }
        }
    }

    getFormDataEmail() {
        // Usar valores do formulário como no sistema desktop
        return {
            vagaDesc: document.getElementById('vaga-desc').value.trim(),
            keywords: document.getElementById('keywords').value.trim().split(',').map(k => k.trim()),
            formacoes: document.getElementById('formacoes').value.trim().split(',').map(f => f.trim()),
            negativas: document.getElementById('negativas').value.trim().split(',').map(n => n.trim()),
            maxEmails: parseInt(document.getElementById('max-emails').value) || 500,
            usarOcr: document.getElementById('usar-ocr').checked
        };
    }

    validateFormEmail(data) {
        if (!data.vagaDesc || !data.keywords || data.keywords.length === 0) {
            this.addLogEntry('error', 'Preencha a descrição da vaga e palavras-chave.');
            return false;
        }
        
        if (data.maxEmails < 1 || data.maxEmails > 1000) {
            this.addLogEntry('error', 'Max. Emails deve estar entre 1 e 1000.');
            return false;
        }
        return true;
    }

    async processarTriagemEmail(data) {
        try {
            // Etapa 1: Conectar ao Microsoft Graph
            this.updateLoadingMessage('Conectando ao Microsoft Graph...');
            this.addLogEntry('info', '🔗 Conectando à conta: izabella.cordeiro@odequadroservicos.com.br');
            this.updateProgress(10);
            await this.sleep(1000);

            // Etapa 2: Preparar parâmetros
            this.updateLoadingMessage('Preparando parâmetros de triagem...');
            this.updateProgress(20);

            const requestData = {
                vaga_descricao: data.vagaDesc,
                palavras_chave: data.keywords,
                formacoes: data.formacoes.filter(f => f.trim() !== ''),
                palavras_negativas: data.negativas.filter(n => n.trim() !== ''),
                usar_ocr: data.usarOcr,
                max_emails: data.maxEmails
            };

            this.addLogEntry('info', `📋 Vaga: ${data.vagaDesc}`);
            this.addLogEntry('info', `🏷️ Palavras-chave: ${data.keywords.join(', ')}`);
            this.addLogEntry('info', `🎓 Formações: ${data.formacoes.join(', ')}`);
            this.addLogEntry('info', `📊 Máximo de emails: ${data.maxEmails}`);
            this.addLogEntry('info', `🔍 OCR para PDFs: ${data.usarOcr ? 'Ativado' : 'Desativado'}`);

            // Etapa 3: Executar triagem
            this.updateLoadingMessage('Executando triagem de currículos...');
            this.updateProgress(30);

            const response = await fetch(`${this.API_BASE_URL}/triagem-email`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer odq-triagem-2024'
                },
                body: JSON.stringify(requestData)
            });

            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`Erro na API: ${response.status} - ${errorText}`);
            }

            this.updateProgress(90);
            const result = await response.json();
            
            // Exibir resultados como no sistema desktop
            this.addLogEntry('info', `✅ Triagem concluída!`);
            this.addLogEntry('info', `📧 Total de currículos processados: ${result.total_processados}`);
            this.addLogEntry('info', `✅ Currículos aprovados: ${result.total_aprovados}`);
            this.addLogEntry('info', `📊 Taxa de aprovação: ${result.percentual_aprovacao}%`);

            // Mostrar detalhes dos aprovados
            if (result.arquivos_aprovados && result.arquivos_aprovados.length > 0) {
                this.addLogEntry('info', '📋 Lista de currículos aprovados:');
                result.arquivos_aprovados.forEach((arquivo, index) => {
                    const formacoes = arquivo.formacoes_encontradas ? arquivo.formacoes_encontradas.join(', ') : 'Não informado';
                    this.addLogEntry('info', `✅ ${index + 1}. ${arquivo.arquivo}`);
                    if (formacoes !== 'Não informado') {
                        this.addLogEntry('info', `   📚 Formações: ${formacoes}`);
                    }
                });
            } else {
                this.addLogEntry('warning', '⚠️ Nenhum currículo foi aprovado com os critérios especificados');
            }

            // Finalizar
            this.updateProgress(100);
            this.addLogEntry('info', '🎉 Triagem concluída com sucesso!');
            this.addLogEntry('info', '📁 Currículos aprovados salvos na pasta "aprovados"');
            
            setTimeout(() => {
                this.showLoading(false);
                this.showResultsEmail(result);
            }, 1000);

        } catch (error) {
            this.addLogEntry('error', `❌ Erro durante a triagem: ${error.message}`);
            this.updateProgress(0);
            this.showLoading(false);
        }
    }

    showResultsEmail(result) {
        // Atualizar estatísticas
        document.getElementById('total-emails').textContent = result.total_processados || 0;
        document.getElementById('total-anexos').textContent = result.total_processados || 0;
        document.getElementById('total-aprovados').textContent = result.total_aprovados || 0;
        document.getElementById('taxa-aprovacao').textContent = `${result.percentual_aprovacao || 0}%`;

        // Mostrar painel de resultados
        document.getElementById('results-panel').classList.remove('hidden');
    }

    // Funcionalidades dos botões
    limparFormulario() {
        document.getElementById('triagem-form').reset();
        // Redefiner valores padrão
        document.getElementById('email').value = 'izabella.cordeiro@odequadroservicos.com.br';
        document.getElementById('vaga-desc').value = 'Analista de Sistemas';
        document.getElementById('keywords').value = 'Python, Desenvolvimento, Software, Programação, Backend, API, SQL';
        document.getElementById('formacoes').value = 'Engenharia, Ciência da Computação, Sistemas, Análise, Tecnologia';
        document.getElementById('negativas').value = 'estagiário, estágio, trainee, júnior';
        document.getElementById('max-emails').value = '500';
        document.getElementById('usar-ocr').checked = true;
        
        // Redefinir data atual
        const hoje = new Date();
        const ano = hoje.getFullYear();
        const mes = String(hoje.getMonth() + 1).padStart(2, '0');
        const dia = String(hoje.getDate()).padStart(2, '0');
        document.getElementById('data-filtro').value = `${ano}-${mes}-${dia}`;
        
        this.addLogEntry('info', '🔄 Formulário limpo e valores padrão restaurados.');
    }

    abrirAprovados() {
        this.addLogEntry('info', '📁 Verificando pasta de aprovados...');
        
        if (this.modoOffline) {
            // Modo simulação - mostrar arquivos fictícios
            this.addLogEntry('info', '📴 Modo simulação - Mostrando arquivos de exemplo');
            this.addLogEntry('info', '✅ Encontrados 4 arquivo(s) aprovado(s):');
            this.addLogEntry('info', '📄 1. curriculum_joao_silva.pdf (125.3 KB)');
            this.addLogEntry('info', '📄 2. cv_maria_santos.docx (98.7 KB)');
            this.addLogEntry('info', '📄 3. curriculo_pedro_costa.pdf (156.8 KB)');
            this.addLogEntry('info', '📄 4. cv_ana_oliveira.pdf (134.2 KB)');
            this.addLogEntry('info', '💾 Para baixar, use a funcionalidade de download.');
            this.addLogEntry('info', '💡 Para ver arquivos reais, configure o backend em modo produção');
            return;
        }
        
        // Fazer chamada para listar aprovados
        fetch(`${this.API_BASE_URL}/aprovados`, {
            headers: {
                'Authorization': 'Bearer odq-triagem-2024'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success && data.arquivos.length > 0) {
                this.addLogEntry('info', `✅ Encontrados ${data.total} arquivo(s) aprovado(s):`);
                data.arquivos.forEach((arquivo, index) => {
                    const tamanhoKB = (arquivo.tamanho / 1024).toFixed(1);
                    this.addLogEntry('info', `📄 ${index + 1}. ${arquivo.nome} (${tamanhoKB} KB)`);
                });
                this.addLogEntry('info', '💾 Para baixar, use a funcionalidade de download.');
            } else {
                this.addLogEntry('warning', '⚠️ Nenhum arquivo aprovado encontrado.');
                this.addLogEntry('info', 'Execute uma triagem para gerar arquivos aprovados.');
            }
        })
        .catch(error => {
            this.addLogEntry('error', `❌ Erro ao acessar aprovados: ${error.message}`);
            this.addLogEntry('info', '🔄 Alternando para modo simulação...');
            this.modoOffline = true;
            this.abrirAprovados(); // Chamar novamente no modo offline
        });
    }

    limparLog() {
        const logOutput = document.getElementById('log-output');
        logOutput.innerHTML = '';
        this.logEntries = [];
        this.addLogEntry('info', '🧹 Log limpo.');
    }

    downloadLog() {
        const logText = this.logEntries.map(entry => 
            `[${entry.timestamp}] ${entry.type.toUpperCase()}: ${entry.message}`
        ).join('\n');
        
        this.downloadFile('triagem_log.txt', logText);
        this.addLogEntry('info', '💾 Log baixado.');
    }

    downloadAprovados() {
        this.addLogEntry('info', '💾 Download de aprovados será implementado no deploy final.');
    }

    verAprovados() {
        this.addLogEntry('info', '👁️ Visualização de aprovados será implementada no deploy final.');
    }

    novaTriagem() {
        this.limparFormulario();
        document.getElementById('results-panel').classList.add('hidden');
        this.addLogEntry('info', '🔄 Pronto para nova triagem.');
    }

    // Utilitários
    addLogEntry(type, message) {
        const timestamp = new Date().toLocaleTimeString();
        const entry = { timestamp, type, message };
        this.logEntries.push(entry);

        const logOutput = document.getElementById('log-output');
        const logEntry = document.createElement('div');
        logEntry.className = `log-entry ${type}`;
        logEntry.innerHTML = `
            <span class="timestamp">${timestamp}</span>
            <span class="message">${message}</span>
        `;
        
        logOutput.appendChild(logEntry);
        logOutput.scrollTop = logOutput.scrollHeight;
    }

    showLoading(show) {
        const overlay = document.getElementById('loading-overlay');
        if (show) {
            overlay.classList.remove('hidden');
            this.updateProgress(0);
        } else {
            overlay.classList.add('hidden');
        }
    }

    updateLoadingMessage(message) {
        document.getElementById('loading-message').textContent = message;
    }

    updateProgress(percent) {
        document.getElementById('progress-fill').style.width = `${percent}%`;
    }

    updateLoadingStats(stats) {
        document.getElementById('loading-stats').textContent = stats;
    }

    downloadFile(filename, content) {
        const blob = new Blob([content], { type: 'text/plain' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    }

    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}

// Inicializar sistema quando a página carregar
document.addEventListener('DOMContentLoaded', () => {
    window.triagemSystem = new TriagemSystem();
    console.log('🚀 Sistema de Triagem ODQ iniciado com dados reais do Microsoft 365');
});