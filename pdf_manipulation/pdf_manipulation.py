import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfReader, PdfWriter
import subprocess
import os
import tempfile
import sys

def get_exec_path(nome):
    """
    Retorna o caminho correto para o executável embutido,
    tanto em modo script quanto em modo compilado (PyInstaller).
    """
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, 'bin', nome)
    else:
        return os.path.join(os.path.dirname(__file__), 'bin', nome)

def selecionar_pdf():
    caminho = filedialog.askopenfilename(filetypes=[("Arquivos PDF", "*.pdf")])
    if caminho:
        entrada_pdf.set(caminho)

def remover_restricoes_qpdf(caminho_original):
    try:
        temp_file = tempfile.mktemp(suffix=".pdf")
        qpdf_path = get_exec_path("qpdf.exe")
        subprocess.run([qpdf_path, "--decrypt", caminho_original, temp_file], check=True)
        return temp_file
    except Exception as e:
        messagebox.showerror("Erro ao remover restrições", str(e))
        return None

def comprimir_pdf(caminho_entrada, caminho_saida):
    try:
        gs_path = get_exec_path("gswin64c.exe")
        cmd = [
            gs_path,
            "-sDEVICE=pdfwrite",
            "-dCompatibilityLevel=1.4",
            "-dPDFSETTINGS=/screen",
            "-dNOPAUSE",
            "-dQUIET",
            "-dBATCH",
            f"-sOutputFile={caminho_saida}",
            caminho_entrada
        ]
        subprocess.run(cmd, check=True)
        return True
    except Exception as e:
        messagebox.showerror("Erro na compressão", str(e))
        return False

def extrair_paginas():
    try:
        caminho = entrada_pdf.get()
        paginas_str = entrada_paginas.get()

        caminho_desbloqueado = remover_restricoes_qpdf(caminho)
        if not caminho_desbloqueado:
            return

        reader = PdfReader(caminho_desbloqueado)
        writer = PdfWriter()

        total_paginas = len(reader.pages)
        paginas_selecionadas = []

        for parte in paginas_str.split(','):
            if '-' in parte:
                inicio, fim = map(int, parte.split('-'))
                paginas_selecionadas.extend(range(inicio, fim + 1))
            else:
                paginas_selecionadas.append(int(parte))

        for num in paginas_selecionadas:
            if 1 <= num <= total_paginas:
                writer.add_page(reader.pages[num - 1])
            else:
                messagebox.showerror("Erro", f"Página {num} fora do intervalo.")
                return

        arquivo_temp = tempfile.mktemp(suffix=".pdf")
        with open(arquivo_temp, "wb") as f:
            writer.write(f)

        caminho_final = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF", "*.pdf")])
        if caminho_final:
            sucesso = comprimir_pdf(arquivo_temp, caminho_final)
            os.remove(arquivo_temp)
            os.remove(caminho_desbloqueado)
            if sucesso:
                messagebox.showinfo("Sucesso", "PDF gerado, desbloqueado e comprimido com sucesso!")

    except Exception as e:
        messagebox.showerror("Erro", str(e))

# === Interface Gráfica ===
root = tk.Tk()
root.title("PDF Cutter & Compressor")

entrada_pdf = tk.StringVar()
entrada_paginas = tk.StringVar()

tk.Label(root, text="PDF de entrada:").pack(pady=5)
tk.Entry(root, textvariable=entrada_pdf, width=50).pack()
tk.Button(root, text="Selecionar PDF", command=selecionar_pdf).pack(pady=5)

tk.Label(root, text="Páginas (ex: 1,3,5-7):").pack(pady=5)
tk.Entry(root, textvariable=entrada_paginas, width=30).pack()

tk.Button(root, text="Extrair, Desbloquear e Comprimir", command=extrair_paginas).pack(pady=10)

# Rodapé com crédito
rodape = tk.Label(root, text="Desenvolvido por Gustavo de Tarso", font=("Arial", 8), fg="gray")
rodape.pack(side="bottom", pady=5)

root.mainloop()
