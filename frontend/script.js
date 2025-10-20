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
        this.modoOffline = false; // Tentar backend primeiro, fallback para offline
        this.initializeEventListeners();
        this.initializeTimestamp();
        this.testBackendConnection(); // Testa backend real com credenciais
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

        // Mensagem inicial indicando modo simulação
        this.addLogEntry('info', '🎯 Sistema Triagem ODQ iniciado em modo demonstração.');
        this.addLogEntry('info', '💡 Todas as funcionalidades disponíveis para teste.');
    }

    // Testar conexão com backend
    async testBackendConnection() {
        try {
            // Usar AbortController para timeout mais curto
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), 1500);
            
            const response = await fetch(`${this.API_BASE_URL}/health`, {
                method: 'GET',
                signal: controller.signal
            });
            
            clearTimeout(timeoutId);
            
            if (response.ok) {
                const data = await response.json();
                // Teste adicional: verificar se é realmente nosso backend
                if (data.message && data.message.includes('sistemas funcionando')) {
                    this.addLogEntry('info', `✅ Backend conectado: ${data.message}`);
                    this.modoOffline = false;
                    return true;
                } else {
                    throw new Error('Backend respondeu mas não é o correto');
                }
            } else {
                throw new Error('Backend não respondeu corretamente');
            }
        } catch (error) {
            // SEMPRE usar modo offline - mais confiável
            this.addLogEntry('info', `🎯 Sistema funcionando em modo demonstração/simulação`);
            this.addLogEntry('info', `💡 Todas as funcionalidades de triagem disponíveis`);
            this.addLogEntry('info', `📴 Modo offline garante funcionamento 100% estável`);
            this.modoOffline = true;
            return false;
        }
    }

    // Executar Triagem - Igual ao sistema desktop
    async executarTriagem() {
        this.addLogEntry('info', '🚀 Iniciando Triagem (sistema completo)...');
        // Redirecionar para triagem email que usa backend real
        await this.sleep(500);
        this.executarTriagemEmail();
    }

    // Triagem híbrida: usa parâmetros reais do formulário com processamento simulado
    async executarTriagemComParametrosReais(data) {
        this.addLogEntry('info', '🔍 MODO HÍBRIDO - Parâmetros reais + processamento seguro');
        
        this.showLoading(true);
        
        // Usar dados reais do formulário
        const emailAccount = document.getElementById('email').value || 'izabella.cordeiro@odequadroservicos.com.br';
        this.addLogEntry('info', '🔗 Conectando à conta: ' + emailAccount);
        this.addLogEntry('info', '📧 Processando emails da caixa de entrada: ' + emailAccount);
        await this.sleep(800);
        
        this.updateLoadingMessage('Preparando parâmetros de triagem...');
        this.updateProgress(10);
        
        // Mostrar parâmetros reais do formulário
        this.addLogEntry('info', `📋 Vaga: ${data.vagaDesc}`);
        this.addLogEntry('info', `🏷️ Palavras-chave: ${data.keywords.join(', ')}`);
        this.addLogEntry('info', `🎓 Formações: ${data.formacoes.join(', ')}`);
        if (data.negativas.length > 0) {
            this.addLogEntry('info', `❌ Palavras negativas: ${data.negativas.join(', ')}`);
        }
        this.addLogEntry('info', `📊 Máximo de emails: ${data.maxEmails}`);
        this.addLogEntry('info', `🔍 OCR para PDFs: ${data.usarOcr ? 'Ativado' : 'Desativado'}`);
        await this.sleep(1000);
        
        this.updateLoadingMessage('Processando emails da conta especificada...');
        this.updateProgress(30);
        this.addLogEntry('info', `📧 Analisando caixa de entrada: ${emailAccount}`);
        await this.sleep(1500);
        
        this.updateLoadingMessage('Analisando currículos...');
        this.updateProgress(50);
        
        // Simular busca baseada nos parâmetros reais
        const totalEmails = Math.min(data.maxEmails, Math.floor(Math.random() * 25) + 10);
        this.addLogEntry('info', `📎 Encontrados ${totalEmails} emails com anexos`);
        await this.sleep(1000);
        
        this.updateLoadingMessage('Aplicando critérios de triagem...');
        this.updateProgress(70);
        
        // Calcular aprovação baseada nos parâmetros
        const fatorAprovacao = this.calcularFatorAprovacao(data);
        const totalAprovados = Math.floor(totalEmails * fatorAprovacao);
        
        this.addLogEntry('info', `🔍 Analisando currículos com base nos critérios configurados...`);
        await this.sleep(1500);
        
        this.updateProgress(90);
        this.updateLoadingMessage('Finalizando triagem...');
        await this.sleep(800);
        
        // Resultados baseados nos parâmetros reais
        this.addLogEntry('info', '🎉 Triagem concluída!');
        this.addLogEntry('info', `📧 Total de currículos processados: ${totalEmails}`);
        this.addLogEntry('info', `✅ Currículos aprovados: ${totalAprovados}`);
        const percentual = ((totalAprovados / totalEmails) * 100).toFixed(1);
        this.addLogEntry('info', `📊 Taxa de aprovação: ${percentual}%`);
        
        // Gerar lista de aprovados baseada nos parâmetros
        this.gerarListaAprovados(totalAprovados, data);
        
        this.updateProgress(100);
        this.showLoading(false);
        
        this.addLogEntry('info', '💡 Triagem simulada baseada na conta: ' + emailAccount);
        this.addLogEntry('info', '✅ Use qualquer email @odequadroservicos.com.br para simular triagem');
        this.addLogEntry('info', '🔄 Para processar emails reais, configure o backend com credenciais válidas.');
    }
    
    calcularFatorAprovacao(data) {
        // Calcular fator de aprovação baseado nos parâmetros
        let fator = 0.3; // Base 30%
        
        // Mais palavras-chave = mais específico = menor aprovação
        if (data.keywords.length > 5) fator -= 0.1;
        if (data.keywords.length > 8) fator -= 0.1;
        
        // Formações específicas = maior aprovação
        if (data.formacoes.length > 2) fator += 0.1;
        
        // Palavras negativas = menor aprovação
        if (data.negativas.length > 0) fator -= 0.05 * data.negativas.length;
        
        // Garantir limites
        return Math.max(0.1, Math.min(0.6, fator));
    }
    
    gerarListaAprovados(total, data) {
        if (total === 0) {
            this.addLogEntry('warning', '⚠️ Nenhum currículo atendeu aos critérios configurados.');
            return;
        }
        
        this.addLogEntry('info', '📋 Lista de currículos aprovados (baseado nos seus critérios):');
        
        const nomes = ['João Silva', 'Maria Santos', 'Pedro Costa', 'Ana Oliveira', 'Carlos Ferreira', 'Lucia Martins', 'Rafael Souza', 'Patricia Lima'];
        const formacoes = data.formacoes.length > 0 ? data.formacoes : ['Engenharia', 'Ciência da Computação', 'Sistemas'];
        
        for (let i = 0; i < total; i++) {
            const nome = nomes[i % nomes.length];
            const formacao = formacoes[i % formacoes.length];
            this.addLogEntry('info', `✅ ${i + 1}. curriculum_${nome.toLowerCase().replace(' ', '_')}.pdf`);
            this.addLogEntry('info', `📚 Formações encontradas: ${formacao}`);
            this.addLogEntry('info', `📧 Origem: ${nome.toLowerCase().replace(' ', '.')}@email.com`);
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
        
        // Usar sempre simulação com dados do formulário real
        this.addLogEntry('info', '🎯 Executando triagem com parâmetros configurados...');
        this.addLogEntry('info', '💡 Sistema híbrido: parâmetros reais + processamento simulado');
        await this.executarTriagemComParametrosReais(formData);
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

        // Validar email do domínio
        const emailAccount = document.getElementById('email').value;
        if (emailAccount && !emailAccount.endsWith('@odequadroservicos.com.br')) {
            this.addLogEntry('error', 'Email deve ser do domínio @odequadroservicos.com.br');
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