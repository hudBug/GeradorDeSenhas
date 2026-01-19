import customtkinter as ctk
import string
import secrets
import random

# Configurações de aparência
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

class GeradorSenhas(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gerador de senhas em Python")
        self.geometry("800x600")
        self.resizable(False, False)

        # Título e subtitulo
        self.label_titulo = ctk.CTkLabel(
            self, text="Gerador de Senhas", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.label_subtitulo = ctk.CTkLabel(
            self, text="Gerador de Senhas", 
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.label_titulo.pack(pady=(25, 15))
        self.label_subtitulo.pack(pady=(25, 15))

        # Entrada Palavra Base
        self.label_base = ctk.CTkLabel(self, text="Palavra base para senha (ex: consegui):")
        self.label_base.pack()
        self.entry_base = ctk.CTkEntry(self, width=320, placeholder_text="Digite aqui")
        self.entry_base.pack(pady=5)

        # Slider de Comprimento
        self.label_tamanho = ctk.CTkLabel(self, text="Comprimento Total: 12")
        self.label_tamanho.pack(pady=(15, 0))
        
        self.slider = ctk.CTkSlider(self, from_=8, to=32, number_of_steps=24, command=self.atualizar_label)
        self.slider.set(12)
        self.slider.pack(pady=10)

        # Senha gerada
        self.entry_senha = ctk.CTkEntry(
            self, width=340, height=50, 
            justify="center", font=ctk.CTkFont(size=20, weight="bold"),
            fg_color="#333333"
        )
        self.entry_senha.pack(pady=20)

        # Botão Gerar
        self.btn_gerar = ctk.CTkButton(
            self, text="Gerar Senha", 
            command=self.gerar_senha,
            font=ctk.CTkFont(weight="bold")
        )
        self.btn_gerar.pack(pady=5)

        # Botão Copiar
        self.btn_copiar = ctk.CTkButton(
            self, text="Copiar Senha", 
            command=self.copiar_senha,
            fg_color="transparent", border_width=2
        )
        self.btn_copiar.pack(pady=10)

        # Label de Feedback
        self.label_feedback = ctk.CTkLabel(self, text="", text_color="#2ecc71")
        self.label_feedback.pack()

    def atualizar_label(self, valor):
        self.label_tamanho.configure(text=f"Comprimento Total: {int(valor)}")

    def transformar_palavra(self, palavra):
        # Regras de substituição
        mapa = {
            'a': ['@', '4'],
            'e': ['3', '#'],
            'i': ['1', '!'],
            'o': ['0'],
            'u': ['('],
            's' : ['5', '$'],
            'p': ['9'],
            'g': ['6'],
            'z':['7', '2'],
            'x': ['+']
        }
        nova_palavra = ""
        for letra in palavra.lower():
            if letra in mapa and random.random() < 0.7:
                nova_palavra += random.choice(mapa[letra])
            else:
                # Alterna maiúsculas e minúsculas aleatoriamente
                nova_palavra += letra.upper() if random.random() < 0.5 else letra.lower()
        return nova_palavra

    def gerar_senha(self):
        try:
            palavra_raw = self.entry_base.get().strip().replace(" ", "")
            
            if not palavra_raw:
                self.label_feedback.configure(text="Erro: Insira uma palavra base!", text_color="#e74c3c")
                return

            # Ajusta tamanho alvo se a palavra for maior que o slider
            tamanho_slider = int(self.slider.get())
            tamanho_alvo = max(tamanho_slider, len(palavra_raw))
            
            palavra_estilizada = self.transformar_palavra(palavra_raw)
            pool = string.ascii_letters + string.digits + string.punctuation
            
            tentativas = 0
            while tentativas < 100:
                faltam = tamanho_alvo - len(palavra_estilizada)
                extras = ''.join(secrets.choice(pool) for _ in range(faltam))
                
                senha_final = palavra_estilizada + extras
                
                # Valida se tem Maiúscula, Minúscula, Número e Especial
                if (any(c.isupper() for c in senha_final) and 
                    any(c.islower() for c in senha_final) and 
                    any(c.isdigit() for c in senha_final) and 
                    any(c in string.punctuation for c in senha_final)):
                    break
                
                # Se a palavra for grande demais e faltar requisito, força um extra no fim
                if len(palavra_estilizada) >= tamanho_alvo:
                    palavra_estilizada += secrets.choice(string.digits + string.punctuation)
                
                tentativas += 1

            self.entry_senha.delete(0, 'end')
            self.entry_senha.insert(0, senha_final)
            self.label_feedback.configure(text="Senha gerada com sucesso!", text_color="#2ecc71")

        except Exception as e:
            print(f"DEBUG: {e}")
            self.label_feedback.configure(text="Erro inesperado ao gerar a senha.", text_color="#e74c3c")

    def copiar_senha(self):
        try:
            senha = self.entry_senha.get()
            if senha:
                self.clipboard_clear()
                self.clipboard_append(senha)
                self.label_feedback.configure(text="Copiado para a área de transferência!", text_color="#2ecc71")
                self.after(2000, lambda: self.label_feedback.configure(text=""))
        except:
            self.label_feedback.configure(text="Erro ao copiar.", text_color="#e74c3c")

if __name__ == "__main__":
    app = GeradorSenhas()
    app.mainloop()