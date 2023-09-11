#%%
import os
import pandas as pd
from pdf_processor import extract_sections_from_pdf
from logger import log_error
#%%
def scan_directory_for_pdfs(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".pdf"):
                yield os.path.join(root, file)

def main():
    directory_path = input("Digite o caminho do diretório: ")

    print("Iniciando a varredura de PDFs no diretório...")

    pdf_files = list(scan_directory_for_pdfs(directory_path))
    total_files = len(pdf_files)

    if total_files == 0:
        print("Nenhum arquivo PDF encontrado.")
        return

    print(f"{total_files} arquivos PDF encontrados. Processando...")

    data = []

    for index, pdf_path in enumerate(pdf_files, 1):
        print(f"Processando arquivo {index} de {total_files} - {pdf_path}...")

        try:
            extracted_sections_list = extract_sections_from_pdf(pdf_path)
            
            if not extracted_sections_list:
                log_error(f"Term 'CADERNO TÉCNICO' not found in {pdf_path}.")
                print(f"Aviso: 'CADERNO TÉCNICO' não encontrado em {pdf_path}. Veja o log para mais detalhes.")
                continue

            # Adicione todos os dicionários de seções extraídas à lista de dados
            data.extend(extracted_sections_list)

        except Exception as e:
            log_error(f"Error processing {pdf_path}: {str(e)}")
            print(f"Erro ao processar {pdf_path}. Veja o log para mais detalhes.")

    print("Finalizando processamento...")

    dataframe = pd.DataFrame(data)

    if not dataframe.empty:
        dataframe.to_csv('output.csv', index=False)
        print("Dados processados salvos em 'output.csv'.")
    else:
        print("Nenhum dado processado foi encontrado.")

    print("Execução completa!")
#%%
main()

# %%
