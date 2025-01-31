# Azure Translator
- A repo to house code and artifacts to demo Azure Translator services. This wraps a few Python methods around
  the REST APIs. The `main.py` file offers an independent example of translating a number of sentences into any other supported language.
- For translator documentation, see [here](https://docs.microsoft.com/en-us/azure/cognitive-services/translator/translator-overview) and for the custom translator portal, see [here](https://portal.customtranslator.azure.ai/)

# Sample Code
## Text Translate
> *Real-time transcription, up to 10k characters in a single request. Leverages sample text containing
Microsoft's mission statement and values to showcase translations.*

```python
# Import the class, and initialize the sample text
from translation import textTranslate
tt = textTranslate(sample_filename='./data-files/text_translation/msft-values.txt')
tt.sample_text
```

```python
# To translate into a sample language, with source: English.
# `es` for Spanish, `fr` for French.
tt.one_language(to_lang='ja')
```

```python
# To translate into five randomly picked languages
tt.five_random()
```

```python
# To translate into Latin characters
# Japanese string hardcoded into method (string = '猿も木から落ちる'):
tt.transliterate()
```

## Document Translate
> Ideal for large text processing where throughput is key, and maintaining the original format is important.
Leverages a `DemoDocument.docx` that is already uploaded into a source container, to be translated and dropped into
a target container.

```python
# Import the class, and initialize the object
from translation import documentTranslate
dt = documentTranslate()
```

```python
# To trigger the document translation request for all docs in container
# All documents in `sourcedocs` will move to `targetdocs`.
# Default conversion: `en` (`English`) to `es` (`Spanish`).
# Requires source documents to be in English.
dt.translate_docs()
```

```python
# Uses the `DemoDocument.docx` which is sourced in `German` to convert to `English`.
dt.translate_docs(source_lang='de',target_lang='en')
```


## Custom Translate Models
> Ideal scenario when the model needs to learn specific industry/domain specifics. In this case, we are
looking at Azure localized documentation and comparing the standard translation vs. the custom translation.

```python
## Translation with custom model
from translation import customTranslate
t = customTranslate('./data-files/custom_translation/custom_text.txt')
t.sample_text
t.one_language(category_id=<give custom model ID>, to_lang='es')
```

```python
## Similar translation using standard model
from translation import textTranslate
tt = textTranslate('./data-files/custom_translation/custom_text.txt')
tt.sample_text
tt.one_language(to_lang='es')
```

## Potential Future Samples
- Multiple language outputs in a single API call.
- Expose dynamic dictionaries in text translate, or glossaries with document translation.
