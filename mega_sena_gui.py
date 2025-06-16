import random
import tkinter as tk
from tkinter import ttk, scrolledtext

# Tabela oficial de preços por quantidade de dezenas
tabela_precos = {
    6: 5.00,
    7: 35.00,
    8: 140.00,
    9: 420.00,
    10: 1050.00,
    11: 2310.00,
    12: 4620.00,
    13: 8580.00,
    14: 15015.00,
    15: 25025.00,
    16: 40040.00,
    17: 61880.00,
    18: 92820.00,
    19: 135660.00,
    20: 193800.00
}

# Função para gerar os jogos aleatórios
def gerar_jogos(lista_jogos):
    jogos_gerados = []
    for dezenas, quantidade in lista_jogos:
        for _ in range(quantidade):
            jogo = sorted(random.sample(range(1, 61), dezenas))
            jogos_gerados.append(jogo)
    return jogos_gerados

# Função para calcular todas as combinações possíveis com o valor disponível
def calcular_opcoes(valor_disponivel):
    opcoes = []
    # Lista com as quantidades de dezenas possíveis (do maior pro menor)
    faixas = sorted(tabela_precos.keys(), reverse=True)

    # Vamos limitar no máximo 3 opções para o usuário (para não poluir a tela)
    max_opcoes = 3

    for dezenas_max in faixas:
        temp_valor = valor_disponivel
        jogos = []
        while temp_valor >= tabela_precos[dezenas_max]:
            qtd = int(temp_valor // tabela_precos[dezenas_max])
            if qtd > 0:
                jogos.append((dezenas_max, qtd))
                temp_valor -= tabela_precos[dezenas_max] * qtd

        # Depois que preenche com essa faixa, tenta preencher com faixas menores
        for dezenas_min in sorted(tabela_precos.keys(), reverse=True):
            while temp_valor >= tabela_precos[dezenas_min] and dezenas_min < dezenas_max:
                jogos.append((dezenas_min, 1))
                temp_valor -= tabela_precos[dezenas_min]

        if jogos:
            opcoes.append(jogos)

        # Para não criar muitas opções, limite a 3
        if len(opcoes) >= max_opcoes:
            break

    return opcoes

# Função para exibir os jogos finais em uma interface Tkinter com barra de rolagem
def exibir_jogos(jogos):
    janela = tk.Tk()
    janela.title("Jogos Gerados - Mega Sena")
    janela.geometry("500x600")

    # Adiciona uma barra de rolagem
    txt_area = scrolledtext.ScrolledText(janela, wrap=tk.WORD, width=60, height=30)
    txt_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    # Exibe todos os jogos com numeração
    for idx, jogo in enumerate(jogos, 1):
        txt_area.insert(tk.END, f"Jogo {idx}: {jogo}\n")

    txt_area.insert(tk.END, "\nBoa sorte!!!")
    janela.mainloop()

# Função principal
def main():
    try:
        valor_apostado = float(input("Informe o valor apostado: R$ "))
    except ValueError:
        print("Valor inválido! Digite um número válido.")
        return

    print(f"\nVocê tem R$ {valor_apostado:.2f} disponível para apostar.\n")

    # Caso o valor seja menor que R$ 5, não permite jogar
    if valor_apostado < tabela_precos[6]:
        print("Valor insuficiente para qualquer aposta.")
        return

    # Gera as combinações possíveis de apostas
    opcoes = calcular_opcoes(valor_apostado)

    # Exibe as opções encontradas
    print("Opções disponíveis:\n")
    for idx, opcao in enumerate(opcoes, 1):
        descricao = []
        total_gasto = 0
        for dezenas, qtd in opcao:
            total_gasto += tabela_precos[dezenas] * qtd
            descricao.append(f"{qtd} jogo(s) de {dezenas} dezenas (R$ {tabela_precos[dezenas]:.2f} cada)")
        print(f"{idx} - {' | '.join(descricao)} (Total: R$ {total_gasto:.2f})")

    # Pede para o usuário escolher a opção
    while True:
        try:
            escolha = int(input(f"\nDigite o número da opção desejada (1 a {len(opcoes)}): "))
            if 1 <= escolha <= len(opcoes):
                break
            else:
                print("Escolha inválida.")
        except ValueError:
            print("Digite um número válido.")

    # Calcula e gera os jogos conforme a escolha
    jogos_escolhidos = gerar_jogos(opcoes[escolha - 1])

    # Exibe os jogos finais
    exibir_jogos(jogos_escolhidos)

# Executa o programa
if __name__ == "__main__":
    main()
