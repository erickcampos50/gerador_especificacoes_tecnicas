Vamos iniciar!

Primeiro, uma pequena visão geral da estrutura dos arquivos que vamos criar:

1. `main.py`: Arquivo principal que gerencia a execução.
2. `pdf_processor.py`: Contém as funções relacionadas ao processamento do PDF.
3. `logger.py`: Funções para registrar os erros.
4. `requirements.txt`: Lista das bibliotecas necessárias.

---

**1. requirements.txt**

```
PyPDF2
pandas
pdfminer.six
```

---

**2. logger.py**

```python
import datetime

def log_error(error_message):
    with open("error_log.txt", "a") as log_file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] ERROR: {error_message}\n")
```

---

**3. pdf_processor.py**

```python
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

    extracted_data = {}

    for key, (start_marker, end_marker) in sections.items():
        start = text.find(start_marker)
        end = text.find(end_marker)

        if start != -1 and end != -1:
            extracted_data[key] = text[start + len(start_marker):end].strip()

    return extracted_data
```

---

**4. main.py**

```python
import os
import pandas as pd
from pdf_processor import extract_sections_from_pdf
from logger import log_error

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
            extracted_data = extract_sections_from_pdf(pdf_path)
            
            if not extracted_data:
                log_error(f"Term 'CADERNO TÉCNICO' not found in {pdf_path}.")
                continue

            data.append(extracted_data)

        except Exception as e:
            log_error(f"Error processing {pdf_path}: {str(e)}")

    dataframe = pd.DataFrame(data)

    if not dataframe.empty:
        dataframe.to_csv('output.csv', index=False)

if __name__ == "__main__":
    main()
```

---

Isso conclui uma implementação totalmente funcional.