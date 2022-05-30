"""
Data source: https://bestlifeonline.com/world-facts/
"""
from translation import textTranslate

def write_list(filename=None, to_lang_list=None,from_lang_list=None):
    """Write out text translations"""
    with open(filename, 'w') as f:
        for i,v in enumerate(from_lang_list):
            f.write(f"Fact {i} (in English): {v}.\n")
            f.write(f"Translated Fact (in German): {to_lang_list[i]}.\n")
            f.write('\n')

if __name__ == "__main__":
    filename='./data-files/text_translation/interesting-facts.txt'
    output_filename = './interesting-facts-in-german.txt'
    translateObj = textTranslate(sample_filename=filename)
    statements = translateObj.load_single_line_text(filename)
    
    # Iterate through statements and produce translated equivalent
    translated_list = []
    for statement in statements:
        result = translateObj.translate_text(
                text = statement,
                to_lang='de',
                from_lang='en'
                )
        translated_list.append(result)

    # Write out translated file
    write_list(filename = output_filename, 
            to_lang_list=translated_list, 
            from_lang_list=statements)
