import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import random

# Dados Mega Sena: números e preços
PRECOS = {
    6: 5,
    7: 35,
    8: 140,
    9: 420,
    10: 1050,
    11: 2310,
    12: 4620,
    13: 8580,
    14: 15015,
    15: 25025,
    16: 40040,
    17: 61880,
    18: 92820,
    19: 135660,
    20: 193800,
}

def gerar_numeros_aleatorios(qtd):
    """Gera uma lista com 'qtd' dezenas únicas entre 1 e 60."""
    return sorted(random.sample(range(1, 61), qtd))

class MegaSenaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mega Sena - Apostas Automáticas")
        self.geometry("600x600")
        self.configure(bg="#f5f5f5")

        # Variáveis
        self.valor_apostado = tk.DoubleVar()
        self.jogos = []

        self._criar_widgets()

    def _criar_widgets(self):
        # Título
        label_titulo = tk.Label(self, text="Mega Sena - Apostas Automáticas", font=("Helvetica", 18, "bold"), bg="#f5f5f5")
        label_titulo.pack(pady=15)

        # Frame entrada valor apostado
        frame_entrada = tk.Frame(self, bg="#f5f5f5")
        frame_entrada.pack(pady=10)

        label_valor = tk.Label(frame_entrada, text="Informe o valor apostado (R$):", font=("Helvetica", 12), bg="#f5f5f5")
        label_valor.pack(side=tk.LEFT, padx=5)

        self.entry_valor = tk.Entry(frame_entrada, textvariable=self.valor_apostado, font=("Helvetica", 12), width=15)
        self.entry_valor.pack(side=tk.LEFT, padx=5)
        self.entry_valor.focus()

        btn_iniciar = tk.Button(self, text="Iniciar Apostas", font=("Helvetica", 12, "bold"), bg="#4CAF50", fg="white", command=self.iniciar_apostas)
        btn_iniciar.pack(pady=15)

        # Área texto resultados
        self.text_resultado = tk.Text(self, width=70, height=20, font=("Consolas", 11))
        self.text_resultado.pack(padx=10, pady=10)
        self.text_resultado.configure(state='disabled')

    def iniciar_apostas(self):
        # Limpa texto
        self.text_resultado.configure(state='normal')
        self.text_resultado.delete("1.0", tk.END)

        try:
            valor = float(self.entry_valor.get())
            if valor < 5:
                messagebox.showerror("Erro", "Valor mínimo para apostar é R$ 5,00")
                return
        except ValueError:
            messagebox.showerror("Erro", "Informe um valor numérico válido.")
            return

        self.valor_apostado.set(valor)
        self.jogos.clear()

        self.text_resultado.insert(tk.END, f"Você tem R$ {valor:.2f} para apostar.\n\n")

        saldo = valor
        # Executa o fluxo de apostas com opções para o usuário
        saldo = self.opcoes_apostas(saldo)

        # Caso ainda tenha saldo menor que 35 e maior ou igual a 5, faz apostas 6 dezenas direto
        if saldo >= 5 and saldo < 35:
            max_jogos = int(saldo // PRECOS[6])
            resposta = messagebox.askyesno("Apostas Restantes",
                                          f"Com o restante de R$ {saldo:.2f}, você pode fazer até {max_jogos} jogo(s) de 6 dezenas (R$ 5,00 cada).\nDeseja completar com essas apostas?")
            if resposta:
                self.gerar_jogos(6, max_jogos)
                saldo -= max_jogos * PRECOS[6]

        # Mostrar resumo final
        self.mostrar_resumo(saldo)

    def opcoes_apostas(self, saldo):
        # Lista das faixas, do maior para o menor, só as que cabem no saldo
        faixas = [k for k in sorted(PRECOS.keys(), reverse=True) if PRECOS[k] <= saldo]

        for dezenas in faixas:
            preco = PRECOS[dezenas]
            max_jogos = int(saldo // preco)
            if max_jogos < 1:
                continue

            resposta = messagebox.askyesno("Opção de aposta",
                                          f"Deseja fazer {max_jogos} jogo(s) com {dezenas} dezenas por R$ {preco:.2f} cada?")

            if resposta:
                # Pergunta se quer fazer o máximo ou quantos jogos deseja
                if max_jogos > 1:
                    qtd = simpledialog.askinteger("Quantidade de jogos",
                                                  f"Quantos jogos de {dezenas} dezenas deseja fazer? (1 a {max_jogos})",
                                                  minvalue=1, maxvalue=max_jogos)
                else:
                    qtd = 1
                self.gerar_jogos(dezenas, qtd)
                saldo -= preco * qtd

                # Chama recursivamente para saldo restante (menos a faixa 6 que será feita depois)
                if dezenas != 6:
                    saldo = self.opcoes_apostas(saldo)
                break  # Para o loop para perguntar faixa maior primeiro e processar saldo
        return saldo

    def gerar_jogos(self, dezenas, quantidade):
        for _ in range(quantidade):
            jogo = gerar_numeros_aleatorios(dezenas)
            self.jogos.append((dezenas, jogo))
            self.text_resultado.insert(tk.END, f"Jogo com {dezenas} dezenas: {jogo}\n")

    def mostrar_resumo(self, saldo_final):
        total_jogos = sum(qtd for qtd, _ in [(1, jogo) for jogo in self.jogos])
        valor_usado = self.valor_apostado.get() - saldo_final

        resumo = (
            f"\nResumo da aposta:\n"
            f"Valor apostado: R$ {self.valor_apostado.get():.2f}\n"
            f"Quantidade total de jogos: {total_jogos}\n"
            f"Valor usado: R$ {valor_usado:.2f}\n"
            f"Troco: R$ {saldo_final:.2f}\n\n"
            f"Boa sorte! 🍀"
        )
        self.text_resultado.insert(tk.END, resumo)
        self.text_resultado.configure(state='disabled')


if __name__ == "__main__":
    app = MegaSenaApp()
    app.mainloop()
