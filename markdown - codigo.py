#%%
import re
import os


#%%
def extract_code_blocks(markdown_content):
    """Extracts code blocks (denoted by ``` ... ```) from the given markdown content."""
    return re.findall(r"```(?:\w+)?\n([\s\S]*?)\n```", markdown_content)

def extract_headers(markdown_content):
    """Extracts markdown headers (lines starting with `) from the given markdown content."""
    return re.findall(r"\*\*\d+\.\s(.+?)\*\*", markdown_content)

def generate_files(markdown_content):
    """Generate files based on headers and code blocks in the markdown content."""
    
    headers = extract_headers(markdown_content)
    code_blocks = extract_code_blocks(markdown_content)

    if len(headers) != len(code_blocks):
        print("Mismatch between headers and code blocks!")
        return

    for header, code_block in zip(headers, code_blocks):
        try:
            with open(header, 'w') as f:
                f.write(code_block.strip())  # strip() is used to remove any extra whitespace around the code
            print(f"File '{header}' created.")
        except Exception as e:
            print(f"Error creating '{header}': {e}")

def main():
    filename = input("Enter the name of the markdown file: ")
    try:
        with open(filename, 'r') as f:
            markdown_content = f.read()
        generate_files(markdown_content)
    except FileNotFoundError:
        print(f"File '{filename}' not found!")
    except Exception as e:
        print(f"An error occurred: {e}")


#%%
if __name__ == "__main__":
    main()

# %%
