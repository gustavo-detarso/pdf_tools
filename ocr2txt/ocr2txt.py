import tkinter as tk
from tkinter import filedialog, messagebox
from pdf2image import convert_from_path
import pytesseract
from PIL import Image, ImageFilter, ImageOps
import os
import re
import sys

# Dicionário de correções
correcoes = {
    "AFERDIA": "AFERIDA",
    "EMESE": "ÊMESE",
    "H ATB": "HISTÓRICO ATB",
    "CLINCIO": "CLÍNICO",
    "EXAMMES": "EXAMES",
    "SPRONTUARIO": "PRONTUÁRIO",
}

def corrigir_texto(texto):
    for errado, certo in correcoes.items():
        texto = re.sub(rf"\b{errado}\b", certo, texto, flags=re.IGNORECASE)
    return texto

def get_tesseract_path():
    # Para empacotado (PyInstaller) ou modo dev
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, "tesseract", "tesseract.exe")

# Configura pytesseract para usar o binário local
pytesseract.pytesseract.tesseract_cmd = get_tesseract_path()

def selecionar_pdf():
    caminho = filedialog.askopenfilename(filetypes=[("Arquivos PDF", "*.pdf")])
    if caminho:
        entrada_pdf.set(caminho)

def pre_processar_img(img):
    img = img.convert("L")
    img = ImageOps.autocontrast(img)
    img = img.filter(ImageFilter.MedianFilter(size=3))
    img = ImageOps.invert(img)
    img = ImageOps.autocontrast(img)
    img = ImageOps.invert(img)
    img = img.point(lambda x: 0 if x < 160 else 255, '1')
    return img

def extrair_ocr():
    try:
        pdf_path = entrada_pdf.get()
        if not pdf_path:
            messagebox.showwarning("Atenção", "Selecione um arquivo PDF.")
            return

        saida_txt = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Arquivo texto", "*.txt")])
        if not saida_txt:
            return

        messagebox.showinfo("Processando", "Extraindo texto, pode demorar...")

        paginas = convert_from_path(pdf_path, 400)  # dpi maior
        custom_config = r'--oem 3 --psm 6'

        with open(saida_txt, "w", encoding="utf-8") as out_file:
            for i, pagina in enumerate(paginas):
                pagina_tratada = pre_processar_img(pagina)
                texto = pytesseract.image_to_string(pagina_tratada, lang="por", config=custom_config)
                texto_corrigido = corrigir_texto(texto)
                out_file.write(f"\n--- Página {i+1} ---\n")
                out_file.write(texto_corrigido)

        messagebox.showinfo("Concluído", f"O texto foi salvo em:\n{saida_txt}")

    except Exception as e:
        messagebox.showerror("Erro", str(e))

# Interface Gráfica
root = tk.Tk()
root.title("OCR2TXT - PDF para texto via OCR (por Gustavo de Tarso)")

entrada_pdf = tk.StringVar()

tk.Label(root, text="PDF de entrada:").pack(pady=5)
tk.Entry(root, textvariable=entrada_pdf, width=50).pack()
tk.Button(root, text="Selecionar PDF", command=selecionar_pdf).pack(pady=5)

tk.Button(root, text="Extrair Texto (OCR Aprimorado)", command=extrair_ocr).pack(pady=15)

rodape = tk.Label(root, text="Desenvolvido por Gustavo de Tarso", font=("Arial", 8), fg="gray")
rodape.pack(side="bottom", pady=5)

root.mainloop()
