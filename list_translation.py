# Data source: https://bestlifeonline.com/world-facts/
from translation import textTranslate

def write_list(to_lang_list, from_lang_list, filename=None):
    """Write out text translations"""
    if filename:
        with open(filename, 'w') as f:
            for i,v in enumerate(from_lang_list):
                f.write(f"Fact {i} (in English): {v}.\n")
                f.write(f"Translated Fact (in German): {to_lang_list[i]}.\n")
                f.write('\n')
    else:
        print('No filename provided.')
        return None

if __name__ == "__main__":
    filename='./data-files/text_translation/interesting-facts.txt'
    output_filename = './interesting-facts-in-german.txt'

    # Instantiate the translator object
    translator = textTranslate(sample_filename=filename)

    # Create a list of strings in text
    statements = translator.load_single_line_text(filename)
    
    # Iterate through statements and produce translated equivalent
    translated_list = []
    for statement in statements:
        result = translator.translate_text(
                text = statement,
                to_lang='de',
                from_lang='en'
                )
        translated_list.append(result)

    # Write out translated file
    write_list(filename = output_filename, 
            to_lang_list=translated_list, 
            from_lang_list=statements)
