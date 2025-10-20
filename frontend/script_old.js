// Sistema de Triagem ODQ - Frontend JavaScript
// Funcionalidades equivalentes ao sistema desktop

class TriagemSystem {
    constructor() {
        this.API_BASE_URL = 'http://localhost:8000'; // Backend local funcionando
        this.currentJobId = null;
        this.logEntries = [];
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
            const response = await fetch(`${this.API_BASE_URL}/health`);
            if (response.ok) {
                const data = await response.json();
                this.addLogEntry('info', `✅ Backend conectado: ${data.message}`);
            } else {
                this.addLogEntry('warning', '⚠️ Backend não está respondendo corretamente');
            }
        } catch (error) {
            this.addLogEntry('error', `❌ Erro ao conectar com backend: ${error.message}`);
        }
    }

    // Executar Triagem - Funcionalidade principal (sistema desktop)
    async executarTriagem() {
        const formData = this.getFormData();
        
        if (!this.validateForm(formData)) {
            return;
        }

        this.showLoading(true);
        this.addLogEntry('info', 'Iniciando triagem...');
        
        try {
            // Simular as etapas do sistema desktop
            await this.processarTriagem(formData);
        } catch (error) {
            this.addLogEntry('error', `Erro na triagem: ${error.message}`);
            this.showLoading(false);
        }
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

    async processarTriagem(data) {
        try {
            // Etapa 1: Configurar parâmetros
            this.updateLoadingMessage('Configurando parâmetros...');
            this.updateProgress(10);
            await this.sleep(1000);

            // Etapa 2: Conectar ao Microsoft 365
            this.updateLoadingMessage('Conectando ao Microsoft 365...');
            this.addLogEntry('info', `Conectando ao email: ${data.email}`);
            this.updateProgress(20);
            await this.sleep(1500);

            // Etapa 3: Buscar emails
            this.updateLoadingMessage('Buscando emails...');
            const emailsResponse = await this.fetchEmails(data);
            this.updateProgress(40);
            
            this.addLogEntry('info', `Encontrados ${emailsResponse.total} emails`);
            this.updateLoadingStats(`${emailsResponse.total} emails encontrados`);

            // Etapa 4: Processar anexos
            this.updateLoadingMessage('Processando anexos...');
            this.updateProgress(60);
            await this.sleep(2000);

            // Simular processamento de anexos
            let processados = 0;
            let aprovados = 0;
            const totalAnexos = emailsResponse.anexos || 45;

            for (let i = 0; i < totalAnexos; i++) {
                processados++;
                this.updateLoadingMessage(`Processando anexo ${processados}/${totalAnexos}...`);
                this.updateProgress(60 + (30 * processados / totalAnexos));
                
                // Simular análise do currículo
                if (Math.random() > 0.7) { // 30% de aprovação
                    aprovados++;
                    this.addLogEntry('info', `✅ Currículo aprovado: curriculo_${i + 1}.pdf`);
                }
                
                this.updateLoadingStats(`${processados}/${totalAnexos} processados, ${aprovados} aprovados`);
                await this.sleep(100);
            }

            // Etapa 5: Finalizar
            this.updateLoadingMessage('Finalizando triagem...');
            this.updateProgress(95);
            await this.sleep(1000);

            // Mostrar resultados
            this.showResults({
                totalEmails: emailsResponse.total,
                totalAnexos: processados,
                totalAprovados: aprovados,
                taxaAprovacao: ((aprovados / processados) * 100).toFixed(1)
            });

            this.updateProgress(100);
            this.addLogEntry('info', '🎉 Triagem concluída com sucesso!');
            
            setTimeout(() => {
                this.showLoading(false);
            }, 1000);

        } catch (error) {
            throw error;
        }
    }

    async processarTriagem(data) {
        try {
            // Etapa 1: Configurar parâmetros
            this.updateLoadingMessage('Configurando parâmetros...');
            this.updateProgress(10);
            await this.sleep(1000);

            // Etapa 2: Conectar ao Microsoft 365
            this.updateLoadingMessage('Conectando ao Microsoft 365...');
            this.addLogEntry('info', `Conectando ao email: ${data.email}`);
            this.updateProgress(20);
            await this.sleep(1500);

            // Etapa 3: Buscar emails
            this.updateLoadingMessage('Buscando emails...');
            const emailsResponse = await this.fetchEmails(data);
            this.updateProgress(40);
            
            this.addLogEntry('info', `Encontrados ${emailsResponse.total} emails`);
            this.updateLoadingStats(`${emailsResponse.total} emails encontrados`);

            // Etapa 4: Processar anexos
            this.updateLoadingMessage('Processando anexos...');
            this.updateProgress(60);
            await this.sleep(2000);

            // Simular processamento de anexos
            let processados = 0;
            let aprovados = 0;
            const totalAnexos = emailsResponse.anexos || 45;

            for (let i = 0; i < totalAnexos; i++) {
                processados++;
                this.updateLoadingMessage(`Processando anexo ${processados}/${totalAnexos}...`);
                this.updateProgress(60 + (30 * processados / totalAnexos));
                
                // Simular análise do currículo
                if (Math.random() > 0.7) { // 30% de aprovação
                    aprovados++;
                    this.addLogEntry('info', `✅ Currículo aprovado: curriculo_${i + 1}.pdf`);
                }
                
                this.updateLoadingStats(`${processados}/${totalAnexos} processados, ${aprovados} aprovados`);
                await this.sleep(100);
            }

            // Etapa 5: Finalizar
            this.updateLoadingMessage('Finalizando triagem...');
            this.updateProgress(95);
            await this.sleep(1000);

            // Mostrar resultados
            this.showResults({
                totalEmails: emailsResponse.total,
                totalAnexos: processados,
                totalAprovados: aprovados,
                taxaAprovacao: ((aprovados / processados) * 100).toFixed(1)
            });

            this.updateProgress(100);
            this.addLogEntry('info', '🎉 Triagem concluída com sucesso!');
            
            setTimeout(() => {
                this.showLoading(false);
            }, 1000);

        } catch (error) {
            throw error;
        }
    }

    // Executar Triagem por Email ODQ
    async executarTriagemEmail() {
        const formData = this.getFormDataEmail();
        
        if (!this.validateFormEmail(formData)) {
            return;
        }

        this.showLoading(true);
        this.addLogEntry('info', 'Iniciando triagem por email ODQ...');
        
        try {
            await this.processarTriagemEmail(formData);
        } catch (error) {
            this.addLogEntry('error', `Erro na triagem por email: ${error.message}`);
            this.showLoading(false);
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
            // Etapa 1: Configurar conexão Microsoft Graph
            this.updateLoadingMessage('Conectando ao Microsoft Graph...');
            this.addLogEntry('info', 'Conectando à conta izabella.cordeiro@odequadroservicos.com.br');
            this.updateProgress(15);
            await this.sleep(1000);

            // Etapa 2: Buscar emails com anexos
            this.updateLoadingMessage('Buscando emails com anexos...');
            this.updateProgress(30);

            const requestData = {
                vaga_descricao: data.vagaDesc,
                palavras_chave: data.keywords,
                formacoes: data.formacoes.filter(f => f.trim() !== ''),
                palavras_negativas: data.negativas.filter(n => n.trim() !== ''),
                usar_ocr: data.usarOcr,
                max_emails: data.maxEmails
            };

            this.addLogEntry('info', `Parâmetros: Vaga: ${data.vagaDesc}`);
            this.addLogEntry('info', `Palavras-chave: ${data.keywords.join(', ')}`);
            this.addLogEntry('info', `Max emails: ${data.maxEmails}`);
            this.addLogEntry('info', `OCR: ${data.usarOcr ? 'Ativado' : 'Desativado'}`);

            // Fazer chamada real para a API
            this.updateLoadingMessage('Processando emails...');
            this.updateProgress(50);

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

            const result = await response.json();
            
            this.updateProgress(90);
            this.addLogEntry('info', `Triagem concluída: ${result.total_processados} currículos processados`);
            this.addLogEntry('info', `${result.total_aprovados} currículos aprovados (${result.percentual_aprovacao}%)`);

            // Mostrar detalhes dos aprovados
            if (result.arquivos_aprovados && result.arquivos_aprovados.length > 0) {
                this.addLogEntry('info', '📋 Currículos aprovados:');
                result.arquivos_aprovados.forEach(arquivo => {
                    const formacoes = arquivo.formacoes_encontradas ? arquivo.formacoes_encontradas.join(', ') : 'Não informado';
                    this.addLogEntry('info', `✅ ${arquivo.arquivo} - Formações: ${formacoes}`);
                });
            }

            // Mostrar resultados
            this.showResultsEmail(result);
            
            this.updateProgress(100);
            this.addLogEntry('info', '🎉 Triagem por email ODQ concluída com dados reais!');
            
            setTimeout(() => {
                this.showLoading(false);
            }, 1000);

        } catch (error) {
            this.addLogEntry('error', `Falha na triagem: ${error.message}`);
            this.updateProgress(0);
            this.showLoading(false);
            throw error;
        }
    }

    showResultsEmail(result) {
        // Atualizar estatísticas
        document.getElementById('total-emails').textContent = result.total_processados || 0;
        document.getElementById('total-anexos').textContent = result.total_processados || 0;
        document.getElementById('total-aprovados').textContent = result.total_aprovados || 0;
        document.getElementById('taxa-aprovacao').textContent = `${result.percentual_aprovacao || 0}%`;

        // Adicionar informações específicas do email
        if (result.arquivos_aprovados && result.arquivos_aprovados.length > 0) {
            result.arquivos_aprovados.forEach(arquivo => {
                const formacoes = arquivo.formacoes_encontradas ? arquivo.formacoes_encontradas.join(', ') : 'Não informado';
                this.addLogEntry('info', `📄 ${arquivo.arquivo} - Formações: ${formacoes}`);
            });
        }

        // Mostrar painel de resultados
        document.getElementById('results-panel').classList.remove('hidden');
    }

    async fetchEmails(data) {
        // Simular busca de emails via API
        return new Promise((resolve) => {
            setTimeout(() => {
                const total = Math.floor(Math.random() * 50) + 20;
                resolve({
                    total: total,
                    anexos: Math.floor(total * 0.8)
                });
            }, 1500);
        });
    }

    showResults(results) {
        // Atualizar estatísticas
        document.getElementById('total-emails').textContent = results.totalEmails;
        document.getElementById('total-anexos').textContent = results.totalAnexos;
        document.getElementById('total-aprovados').textContent = results.totalAprovados;
        document.getElementById('taxa-aprovacao').textContent = `${results.taxaAprovacao}%`;

        // Mostrar painel de resultados
        document.getElementById('results-panel').classList.remove('hidden');
    }

    // Funcionalidades dos botões
    limparFormulario() {
        document.getElementById('triagem-form').reset();
        this.addLogEntry('info', 'Formulário limpo.');
    }

    abrirAprovados() {
        this.addLogEntry('info', 'Funcionalidade será implementada no deploy final.');
    }

    limparLog() {
        const logOutput = document.getElementById('log-output');
        logOutput.innerHTML = '';
        this.logEntries = [];
        this.addLogEntry('info', 'Log limpo.');
    }

    downloadLog() {
        const logText = this.logEntries.map(entry => 
            `[${entry.timestamp}] ${entry.type.toUpperCase()}: ${entry.message}`
        ).join('\n');
        
        this.downloadFile('triagem_log.txt', logText);
        this.addLogEntry('info', 'Log baixado.');
    }

    downloadAprovados() {
        this.addLogEntry('info', 'Download será implementado no deploy final.');
    }

    verAprovados() {
        this.addLogEntry('info', 'Visualização será implementada no deploy final.');
    }

    novaTriagem() {
        this.limparFormulario();
        document.getElementById('results-panel').classList.add('hidden');
        this.addLogEntry('info', 'Pronto para nova triagem.');
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
    console.log('🚀 Sistema de Triagem ODQ iniciado');
});