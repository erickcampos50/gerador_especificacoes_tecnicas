#%%
import os
import pandas as pd
# from pdf_processor import extract_sections_from_pdf
from logger import log_error





import re
from pdfminer.high_level import extract_text

def extract_sections_from_pdf(pdf_path):
    text = extract_text(pdf_path)

    if "CADERNO TÉCNICO" not in text:
        return None

    sections = {
        "Composicao": ("1. COMPOSIÇÃO ANALÍTICA DE SERVIÇO", "2. ITENS E SUAS CARACTERÍSTICAS"),
        "Itens": ("2. ITENS E SUAS CARACTERÍSTICAS", "3. EQUIPAMENTO"),
        "Equipamentos": ("3. EQUIPAMENTO", "4. CRITÉRIOS PARA QUANTIFICAÇÃO DOS SERVIÇOS"),
        "Criterios": ("4. CRITÉRIOS PARA QUANTIFICAÇÃO DOS SERVIÇOS", "5. CRITÉRIOS DE AFERIÇÃO"),
        "Afericao": ("5. CRITÉRIOS DE AFERIÇÃO", "6. EXECUÇÃO"),
        "Informacoes": ("6. EXECUÇÃO", "7. INFORMAÇÕES"),
        "Pendencias": ("7. INFORMAÇÕES", "8. PENDÊNCIAS"),
    }

    extracted_data_list = []

    start_position = 0
    while True:
        extracted_data = {}
        all_found = True  # assume que todas as seções foram encontradas

        for key, (start_marker, end_marker) in sections.items():
            start = text.find(start_marker, start_position)
            end = text.find(end_marker, start + len(start_marker))

            if start != -1 and end != -1:
                extracted_data[key] = text[start + len(start_marker):end].strip()
            else:
                all_found = False
                break

        if not all_found:
            break

        extracted_data_list.append(extracted_data)
        start_position = end  # ajusta a posição de início para a próxima busca

    return extracted_data_list








def scan_directory_for_pdfs(directory_path):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith(".pdf"):
                yield os.path.join(root, file)

def main():
    directory_path = input("Digite o caminho do diretório: ")

    data = []

    for pdf_path in scan_directory_for_pdfs(directory_path):
        try:
            extracted_data_list = extract_sections_from_pdf(pdf_path)
            
            if not extracted_data_list:
                log_error(f"Term 'CADERNO TÉCNICO' not found in {pdf_path}.")
                continue

            for extracted_data in extracted_data_list:
                data.append(extracted_data)

        except Exception as e:
            log_error(f"Error processing {pdf_path}: {str(e)}")

    dataframe = pd.DataFrame(extracted_data_list)

    if not dataframe.empty:
        dataframe.to_csv('output.csv', index=False)
    return dataframe
#%%
if __name__ == "__main__":
    dataframe = main()

# %%
