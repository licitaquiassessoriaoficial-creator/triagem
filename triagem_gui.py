import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import json
import re
import threading
import traceback

class TriagemApp(tk.Tk):
        def __init__(self):
            super().__init__()
            self.title("Triagem de Currículos - Microsoft 365")
            self.geometry("700x400")

            self.email = tk.StringVar()
            self.config_path = tk.StringVar(value=os.path.join(os.path.dirname(__file__), "parameters.json"))
            self.vaga_desc = tk.StringVar()
            self.keywords = tk.StringVar()
            self.data_inicio = tk.StringVar()
            self.data_fim = tk.StringVar()
            self.formacoes_var = tk.StringVar()

            tk.Label(self, text="Email Microsoft 365:").pack(pady=5)
            tk.Entry(self, textvariable=self.email, width=50).pack(pady=2)
            tk.Label(self, text="Arquivo de configuração: parameters.json (fixo)").pack(pady=5)
            tk.Entry(self, textvariable=self.config_path, width=50, state='disabled').pack(pady=2)
            tk.Label(self, text="Descrição da vaga:").pack(pady=5)
            tk.Entry(self, textvariable=self.vaga_desc, width=50).pack(pady=2)
            tk.Label(self, text="Palavras-chave (separadas por vírgula):").pack(pady=5)
            tk.Entry(self, textvariable=self.keywords, width=50).pack(pady=2)
            tk.Label(self, text="Data inicial (YYYY-MM-DD, opcional):").pack(pady=2)
            tk.Entry(self, textvariable=self.data_inicio, width=20).pack(pady=2)
            tk.Label(self, text="Data final (YYYY-MM-DD, opcional):").pack(pady=2)
            tk.Entry(self, textvariable=self.data_fim, width=20).pack(pady=2)
            tk.Label(self, text="Formação (separadas por vírgula):").pack(pady=5)
            tk.Entry(self, textvariable=self.formacoes_var, width=50).pack(pady=2)
            tk.Button(self, text="Executar Triagem", command=self.run_triagem).pack(pady=10)
            tk.Button(self, text="Abrir pasta de aprovados", command=self.open_aprovados).pack(pady=2)

            frame = tk.Frame(self)
            frame.pack(pady=10, fill='both', expand=True)
            self.log_text = tk.Text(frame, height=10, width=60, state='disabled', wrap='word')
            self.log_text.pack(side='left', fill='both', expand=True)
            scrollbar = tk.Scrollbar(frame, command=self.log_text.yview)
            scrollbar.pack(side='right', fill='y')
            self.log_text['yscrollcommand'] = scrollbar.set

        def run_triagem(self):
            import sys
            config = self.config_path.get()
            email = self.email.get().strip()
            vaga_desc = self.vaga_desc.get().strip()
            keywords = self.keywords.get().strip()
            data_inicio = self.data_inicio.get().strip()
            data_fim = self.data_fim.get().strip()
            formacoes_str = (self.formacoes_var.get() or "").strip()
            negativas_str = ""  # Adapte se quiser campo de negativas na interface
            if not config or not email or not vaga_desc or not keywords:
                messagebox.showerror("Erro", "Preencha o email, arquivo de configuração, descrição da vaga e as palavras-chave.")
                return

            with open(config, "r", encoding="utf-8") as f:
                params = json.load(f)
            params["formacoes"] = formacoes_str
            temp_config = os.path.join(os.path.dirname(config), "parameters_temp.json")
            with open(temp_config, "w", encoding="utf-8") as f:
                json.dump(params, f, indent=2, ensure_ascii=False)
            endpoint_base = params["endpoint"].split("/users/")[0]
            endpoint = f"{endpoint_base}/users/{email}/messages"
            filtros = []
            def format_date(date_str):
                date_str = date_str.strip()
                if re.match(r"^\d{2}/\d{2}/\d{4}$", date_str):
                    d, m, y = date_str.split("/")
                    return f"{y}-{m}-{d}"
                elif re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
                    return date_str
                else:
                    return None
            if data_inicio:
                di_fmt = format_date(data_inicio)
                if not di_fmt:
                    messagebox.showerror("Erro", "Data inicial inválida. Use DD/MM/AAAA ou AAAA-MM-DD.")
                    return
                filtros.append(f"receivedDateTime ge {di_fmt}T00:00:00Z")
            if data_fim:
                df_fmt = format_date(data_fim)
                if not df_fmt:
                    messagebox.showerror("Erro", "Data final inválida. Use DD/MM/AAAA ou AAAA-MM-DD.")
                    return
                filtros.append(f"receivedDateTime le {df_fmt}T23:59:59Z")
            filtro_str = " and ".join(filtros)
            url = endpoint
            if filtro_str:
                url += f"?$filter={filtro_str}&$top=500"
            else:
                url += "?$top=500"
            params["endpoint"] = url
            temp_config = os.path.join(os.path.dirname(config), "parameters_temp.json")
            with open(temp_config, "w", encoding="utf-8") as f:
                json.dump(params, f, indent=2, ensure_ascii=False)
            script_dir = os.path.dirname(config)
            parameters_temp_path = temp_config
            vaga_desc_str = vaga_desc
            keywords_str = keywords
            formacoes = [s.strip() for s in formacoes_str.split(',') if s.strip()] if formacoes_str else []  # Processa as formações

            def log(msg):
                self.log_text.config(state="normal")
                self.log_text.insert("end", msg + "\n")
                self.log_text.see("end")
                self.log_text.config(state="disabled")
                self.log_text.update_idletasks()

            def rodar_triagem():
                log("Iniciando triagem...")
                args = [sys.executable, "-u", "confidential_client_secret_sample.py", temp_config, vaga_desc_str, keywords_str, negativas_str, "--formacoes", formacoes_str]
                log(f'Comando: {' '.join(args)}')
                log(f"Diretório: {script_dir}")

                if not os.path.isfile(parameters_temp_path):
                    log(f"ERRO: parameters_temp.json não encontrado: {parameters_temp_path}")
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
                        env=env
                    )
                except FileNotFoundError:
                    log("ERRO: Python não encontrado ou script ausente.")
                    return
                except Exception as e:
                    log(f"ERRO ao iniciar processo: {e}")
                    return

                for line in iter(proc.stdout.readline, ""):
                    if not line:
                        break
                    log(line.rstrip("\n"))
                proc.stdout.close()
                ret = proc.wait()
                log(f"Processo finalizado (exit code {ret})")
                if ret != 0:
                    log("Triagem terminou com erro.")
                if os.path.exists(parameters_temp_path):
                    try:
                        os.remove(parameters_temp_path)
                    except Exception:
                        pass

            threading.Thread(target=rodar_triagem, daemon=True).start()

        def set_log(self, text):
            self.log_text.config(state='normal')
            self.log_text.delete(1.0, tk.END)
            self.log_text.insert(tk.END, text)
            self.log_text.config(state='disabled')

        def append_log(self, text):
            self.log_text.config(state='normal')
            self.log_text.insert(tk.END, text)
            self.log_text.see(tk.END)
            self.log_text.config(state='disabled')

        def open_aprovados(self):
            config = self.config_path.get()
            if not config:
                messagebox.showerror("Erro", "Selecione o arquivo de configuração primeiro.")
                return
            aprovados_dir = os.path.join(os.path.dirname(config), "aprovados")
            if os.path.exists(aprovados_dir):
                os.startfile(aprovados_dir)
            else:
                messagebox.showinfo("Info", "Nenhuma pasta de aprovados encontrada.")

if __name__ == "__main__":
    app = TriagemApp()
    app.mainloop()
