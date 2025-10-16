"""Interface gráfica para triagem de currículos - Microsoft 365."""

import json
import os
import re
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import messagebox


class TriagemApp(tk.Tk):
    """Aplicação principal de triagem de currículos."""

    def __init__(self):
        """Inicializa a interface gráfica."""
        super().__init__()
        self.title("Triagem de Currículos - Microsoft 365")
        self.geometry("700x400")

        # Variáveis de controle
        self.email = tk.StringVar()
        config_file = "parameters.json"
        config_path = os.path.join(os.path.dirname(__file__), config_file)
        self.config_path = tk.StringVar(value=config_path)
        self.vaga_desc = tk.StringVar()
        self.keywords = tk.StringVar()
        self.data_inicio = tk.StringVar()
        self.data_fim = tk.StringVar()
        self.formacoes_var = tk.StringVar()

        self._setup_ui()

    def _setup_ui(self):
        """Configura a interface do usuário."""
        # Email
        tk.Label(self, text="Email Microsoft 365:").pack(pady=5)
        tk.Entry(self, textvariable=self.email, width=50).pack(pady=2)

        # Arquivo de configuração
        config_label = "Arquivo de configuração: parameters.json (fixo)"
        tk.Label(self, text=config_label).pack(pady=5)
        config_entry = tk.Entry(
            self, textvariable=self.config_path, width=50, state="disabled"
        )
        config_entry.pack(pady=2)

        # Descrição da vaga
        tk.Label(self, text="Descrição da vaga:").pack(pady=5)
        tk.Entry(self, textvariable=self.vaga_desc, width=50).pack(pady=2)

        # Palavras-chave
        keywords_label = "Palavras-chave (separadas por vírgula):"
        tk.Label(self, text=keywords_label).pack(pady=5)
        tk.Entry(self, textvariable=self.keywords, width=50).pack(pady=2)

        # Data inicial
        data_inicial_label = "Data inicial (YYYY-MM-DD, opcional):"
        tk.Label(self, text=data_inicial_label).pack(pady=2)
        data_inicio_entry = tk.Entry(
            self, textvariable=self.data_inicio, width=20
        )
        data_inicio_entry.pack(pady=2)

        # Data final
        data_final_label = "Data final (YYYY-MM-DD, opcional):"
        tk.Label(self, text=data_final_label).pack(pady=2)
        tk.Entry(self, textvariable=self.data_fim, width=20).pack(pady=2)

        # Formação
        formacao_label = "Formação (separadas por vírgula):"
        tk.Label(self, text=formacao_label).pack(pady=5)
        formacoes_entry = tk.Entry(
            self, textvariable=self.formacoes_var, width=50
        )
        formacoes_entry.pack(pady=2)

        # Botões
        triagem_btn = tk.Button(
            self, text="Executar Triagem", command=self.run_triagem
        )
        triagem_btn.pack(pady=10)

        aprovados_btn = tk.Button(
            self, text="Abrir pasta de aprovados", command=self.open_aprovados
        )
        aprovados_btn.pack(pady=2)

        # Log
        frame = tk.Frame(self)
        frame.pack(pady=10, fill="both", expand=True)
        log_params = {
            "height": 10,
            "width": 60,
            "state": "disabled",
            "wrap": "word",
        }
        self.log_text = tk.Text(frame, **log_params)
        self.log_text.pack(side="left", fill="both", expand=True)
        scrollbar = tk.Scrollbar(frame, command=self.log_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.log_text["yscrollcommand"] = scrollbar.set

    def run_triagem(self):
        """Executa o processo de triagem."""
        # Validação
        config = self.config_path.get()
        email = self.email.get().strip()
        vaga_desc = self.vaga_desc.get().strip()
        keywords = self.keywords.get().strip()
        data_inicio = self.data_inicio.get().strip()
        data_fim = self.data_fim.get().strip()
        formacoes_str = (self.formacoes_var.get() or "").strip()
        negativas_str = ""

        if not all([config, email, vaga_desc, keywords]):
            error_msg = (
                "Preencha o email, arquivo de configuração, "
                "descrição da vaga e as palavras-chave."
            )
            messagebox.showerror("Erro", error_msg)
            return

        # Preparação dos parâmetros
        try:
            with open(config, "r", encoding="utf-8") as f:
                params = json.load(f)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao ler configuração: {e}")
            return

        params["formacoes"] = formacoes_str
        script_dir = os.path.dirname(config)
        temp_config = os.path.join(script_dir, "parameters_temp.json")

        # Configuração do endpoint
        endpoint_base = params["endpoint"].split("/users/")[0]
        endpoint = f"{endpoint_base}/users/{email}/messages"
        filtros = ["isRead eq false"]  # Apenas emails não lidos

        # Filtros de data
        if data_inicio:
            di_fmt = self._format_date(data_inicio)
            if not di_fmt:
                error_msg = (
                    "Data inicial inválida. Use DD/MM/AAAA ou AAAA-MM-DD."
                )
                messagebox.showerror("Erro", error_msg)
                return
            filtros.append(f"receivedDateTime ge {di_fmt}T00:00:00Z")

        if data_fim:
            df_fmt = self._format_date(data_fim)
            if not df_fmt:
                error_msg = (
                    "Data final inválida. Use DD/MM/AAAA ou AAAA-MM-DD."
                )
                messagebox.showerror("Erro", error_msg)
                return
            filtros.append(f"receivedDateTime le {df_fmt}T23:59:59Z")

        # Montagem da URL final
        filtro_str = " and ".join(filtros)
        url = f"{endpoint}?$filter={filtro_str}&$top=500"
        params["endpoint"] = url

        # Salvar configuração temporária
        with open(temp_config, "w", encoding="utf-8") as f:
            json.dump(params, f, indent=2, ensure_ascii=False)

        # Executar triagem
        self._execute_triagem(
            temp_config,
            vaga_desc,
            keywords,
            negativas_str,
            formacoes_str,
            script_dir,
        )

    def _format_date(self, date_str):
        """Formata string de data para ISO format."""
        date_str = date_str.strip()
        if re.match(r"^\d{2}/\d{2}/\d{4}$", date_str):
            d, m, y = date_str.split("/")
            return f"{y}-{m}-{d}"
        elif re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
            return date_str
        return None

    def _execute_triagem(
        self,
        temp_config,
        vaga_desc,
        keywords,
        negativas_str,
        formacoes_str,
        script_dir,
    ):
        """Executa o processo de triagem em thread separada."""

        def log(msg):
            self.log_text.config(state="normal")
            self.log_text.insert("end", msg + "\\n")
            self.log_text.see("end")
            self.log_text.config(state="disabled")
            self.log_text.update_idletasks()

        def rodar_triagem():
            log("Iniciando triagem...")
            log("*** PROCESSANDO APENAS EMAILS NÃO LIDOS ***")

            script_path = "confidential_client_secret_sample.py"
            args = [
                sys.executable,
                "-u",
                script_path,
                temp_config,
                vaga_desc,
                keywords,
                negativas_str,
                "--formacoes",
                formacoes_str,
            ]

            log(f'Comando: {" ".join(args)}')
            log(f"Diretório: {script_dir}")

            if not os.path.isfile(temp_config):
                log(f"ERRO: {temp_config} não encontrado")
                return

            env = os.environ.copy()
            env["PYTHONUNBUFFERED"] = "1"

            try:
                proc = subprocess.Popen(
                    args,
                    cwd=script_dir,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    encoding="utf-8",
                    bufsize=1,
                    env=env,
                )

                for line in iter(proc.stdout.readline, ""):
                    if not line:
                        break
                    log(line.rstrip("\\n"))

                proc.stdout.close()
                ret = proc.wait()
                log(f"Processo finalizado (exit code {ret})")

                if ret != 0:
                    log("Triagem terminou com erro.")

            except FileNotFoundError:
                log("ERRO: Python não encontrado ou script ausente.")
            except Exception as e:
                log(f"ERRO ao iniciar processo: {e}")
            finally:
                # Limpar arquivo temporário
                if os.path.exists(temp_config):
                    try:
                        os.remove(temp_config)
                    except Exception:
                        pass

        threading.Thread(target=rodar_triagem, daemon=True).start()

    def open_aprovados(self):
        """Abre a pasta de aprovados."""
        config = self.config_path.get()
        if not config:
            error_msg = "Selecione o arquivo de configuração primeiro."
            messagebox.showerror("Erro", error_msg)
            return

        aprovados_dir = os.path.join(os.path.dirname(config), "aprovados")
        if os.path.exists(aprovados_dir):
            os.startfile(aprovados_dir)
        else:
            info_msg = "Nenhuma pasta de aprovados encontrada."
            messagebox.showinfo("Info", info_msg)


if __name__ == "__main__":
    app = TriagemApp()
    app.mainloop()
