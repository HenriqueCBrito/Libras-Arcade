import csv

def ler_perguntas_do_csv(nome_arquivo):
    perguntas = []
    try:
        csvfile = open(nome_arquivo, newline='', encoding='utf-8')
        reader = csv.DictReader(csvfile)
        if 'pergunta' not in reader.fieldnames:
            print(f"O arquivo {nome_arquivo} não contém a coluna 'pergunta'.")
            return perguntas
        for row in reader:
            perguntas.append(row['pergunta'])
        csvfile.close()
    except FileNotFoundError:
        print(f"Arquivo {nome_arquivo} não encontrado.")
    except Exception as e:
        print(f"Erro ao ler o arquivo {nome_arquivo}: {e}")
    return perguntas

def mostrar_perguntas(perguntas):
    for pergunta in perguntas:
        print(f"- {pergunta}")

def main():
    temas = {
        'viagens': 'viagens.csv',
        'cotidiano': 'cotidiano.csv',
        'escola': 'escola.csv'
    }

    tema_escolhido = input("Qual tema você deseja receber perguntas (viagens/cotidiano/escola)? ").strip().lower()

    if tema_escolhido in temas:
        nome_arquivo = temas[tema_escolhido]
        perguntas = ler_perguntas_do_csv(nome_arquivo)
        if perguntas:
            print(f"Perguntas sobre {tema_escolhido}:")
            mostrar_perguntas(perguntas)
        else:
            print(f"Não foram encontradas perguntas para o tema {tema_escolhido}.")
    else:
        print("Tema não reconhecido. Por favor, escolha entre 'viagens' ou 'cotidiano'.")

if __name__ == "__main__":
    main()
