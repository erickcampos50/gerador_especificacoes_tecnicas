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
        "Execucao": ("6. EXECUÇÃO", "7. INFORMAÇÕES"),
        "Informacoes": ("7. INFORMAÇÕES", "8. PENDÊNCIAS"),
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
