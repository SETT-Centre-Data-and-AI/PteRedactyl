# User Guide

## 📚 Contents <a id="contents"></a>
- 🧭 [Introduction](#introduction)
- ⚡ [Quickstart](#quickstart)
- ♻️ [Reusing an Analyser](#reusing_an_analyser)
- 🔍 [Examining Results](#examining_results)
- 🧩 [Selecting Entities to Redact](#selecting_entities_to_redact)
- ⚙️ [Passing Custom Regex Entities](#passing_custom_regex_entities)
- 🧮 [Anonymising DataFrames](#anonymising_dataframes)
- 🐙 [Kraken integration](#kraken_integration)


## 🧭 Introduction <a id="introduction"></a>
PteRedactyl is a redaction package for personally identifiable information (PII) in text, that combines NER models with regex matching to identify and mask sensitive information. Custom transformers-based NER models can be swapped in, 


This guide will cover usage of PteRedactyl's main functions: `create_analyser`, `analyse`, `anonymise`, and `anonymise_df`:
 - `create_analyser()`: Creates a presidio AnalyserEngine that can be reused across high-level functions
 - `analyse()`: Analyses a string for PII, returning a list of recognised NER or regex-based results with scores
 - `anonymise()`: Analyses and anonymises text, replacing PII with placeholders or hide-in-plain-sight (HIPS) replacements
 - `anonymise_df()`: As above, but by looping over a given column (or columns) in a DataFrame

## ⚡ Quickstart <a id="quickstart"></a>
```python
# Simple anonymisation
import pteredactyl as pt
text = "The patient's name is Steven Johnson. His NHS Number is 0123456789 and postcode is SO16 2HQ. He has been diagnosed with Stevens Johnson Syndrome"

anonymised_text = pt.anonymise(text)
```

You can configure the package by passing different parameters:

- `entities`: List of entities to anonymise.
- `replacement_lists`: Custom replacement values for each entity.
- `highlight`: Set to `True` to highlight anonymised parts in the output.

```python
# Anonymisation for specific entities
entities = ["LOCATION", "PERSON"]
anonymised_text = pt.anonymise(text, entities=entities)

# Hide in plain site by supplying a dictionary of entities: potential replacements
replacement_lists = {
    "PERSON": ["Alice Smith", "Bob Johnson", "Carol Davis"],
    "LOCATION": ["Los Angeles", "Chicago", "Houston"]
}
anonymised_text = pt.anonymise(text, replacement_lists=replacement_lists)
```

## ♻️ Reusing an Analyser <a id="reusing_an_analyser"></a>
When analysing or anonymising multiple pieces of text or DataFrames in the same way, it is highly recommended to create and reuse a single analyser (presidio AnalyzerEngine). While each high-level PteRedactyl function will spin up an analyser if one is not provided, an analyser can be created and then passed, to reuse it.

Example Usage:
```python
import pteredactyl as pt

# Create an analyser
analyser = pt.create_analyser()

# Use the analyser to redact some text
text = "The patient's name is Steven Johnson. His NHS Number is 0123456789 and postcode is SO16 2HQ. He has been diagnosed with Stevens Johnson Syndrome"
redacted_text = pt.anonymise(text=text, analyser=analyser, highlight=True)

print(redacted_text)
```

## 🔍 Examining Results <a id="examining_results"></a>
Instead of anonymising, we can instead check the results of analysis by using the `analyse()` function.
```python
import pteredactyl as pt

text = "The patient's name is Steven Johnson. His NHS Number is 0123456789 and postcode is SO16 2HQ. He has been diagnosed with Stevens Johnson Syndrome"
analyser = pt.create_analyser()
analysis = pt.analyse(text=text, analyser=analyser)
for result in analysis:
    print(result)
```

## 🧩 Selecting Entities to Redact <a id="selecting_entities_to_redact"></a>
We can select specific NER or regex entities to analyse/redact by feeding in these arguments. When empty, PteRedactyl will redact according to a predefined list, which can be checked as follows: 

```python
import pteredactyl as pt
pt.show_defaults()
```

Let's try redacting only specific entities:

```python
import pteredactyl as pt

# Create an analyser
analyser = pt.create_analyser()

# Use the analyser to redact some text
text = "The patient's name is Steven Johnson. His NHS Number is 0123456789 and postcode is SO16 2HQ. He was diagnosed with Stevens Johnson Syndrome on the 1st of January 2024."
redacted_text = pt.anonymise(text=text, analyser=analyser, highlight=True)

print(redacted_text)

# Redact specific entities - keeping the date
text = "The patient's name is Steven Johnson. His NHS Number is 0123456789 and postcode is SO16 2HQ. He was diagnosed with Stevens Johnson Syndrome on the 1st of January 2024."
redacted_text = pt.anonymise(text=text, analyser=analyser, highlight=True, entities="PERSON", regex_entities=["NHS_NUMBER", "POSTCODE"])

print(redacted_text)
```

## ⚙️ Passing Custom Regex Entities <a id="passing_custom_regex_entities"></a>
We can include custom regex and check functions in our analysis/redaction, too:

```python
import pteredactyl as pt
from pteredactyl import build_pteredactyl_recogniser

# Create an analyser
analyser = pt.create_analyser()

# Build a custom regex recogniser
def check_soton_landline(input: str):
    cleaned = input.replace('-','').replace(' ','')
    return cleaned.startswith('0238')


soton_landline_recogniser = build_pteredactyl_recogniser(entity_type = 'SOUTHAMPTON_LANDLINE',
                                           regex = r'(?:\d[\s-]?){11}',
                                           check_function = check_soton_landline)

# Use the analyser to redact some text
text = "The patient's name is Steven Johnson. His NHS Number is 0123456789 and postcode is SO16 2HQ. He was diagnosed with Stevens Johnson Syndrome on the 1st of January 2024. He can be contacted at 02380 111111"
redacted_text = pt.anonymise(text=text, analyser=analyser, highlight=True, entities="PERSON", regex_entities=["NHS_NUMBER", "POSTCODE", soton_landline_recogniser])

print(redacted_text)
```
```Output
The patient's name is <PERSON>. His NHS Number is <NHS_NUMBER> and postcode is <POSTCODE>. He was diagnosed with Stevens Johnson Syndrome on the 1st of January 2024. He can be contacted at <SOUTHAMPTON_LANDLINE>
```

## 🧮 Anonymising DataFrames <a id="anonymising_dataframes"></a>

The `anonymise_df()` function is designed to anonymise sensitive information in a pandas DataFrame. This function can handle Named Entity Recognition (NER) and regex-based entity recognition to redact information such as names, addresses, and other personal identifiers. It can act on a single column or multiple, and redact inplace or by returning a new DataFrame/column 

### Parameters

- `df`: The DataFrame containing the text to anonymise.
- `column`: The name or list of names of the column(s) to anonymise.
- `analyser`: An optional AnalyzerEngine instance. If not provided, a new analyser will be created.
- `entities`: A list of entities to anonymise using the NER model.
- `regex_entities`: A list of regex patterns or custom recognisers to identify and anonymise.
- `highlight`: If `True`, anonymised parts are highlighted.
- `replacement_lists`: A dictionary for hide-in-plain-sight redaction containing replacement values per entity type.
- `inplace`: If `True`, the original DataFrame is modified; otherwise, a copy is returned.
- `col_inplace`: If `True`, the original column is replaced with the redacted version.

### Basic Example

Here's a basic example of anonymising a DataFrame column:

```python
import pandas as pd
import pteredactyl as pt

analyser = pt.create_analyser()

# Create a DataFrame with sample data
df = pd.DataFrame({
    'text': [
        "John Doe's number is 07111 293892.",
        "Jane Smith's lives at 123 Shirley Road."
    ]
})

# Anonymise the 'text' column
anonymised_df = pt.anonymise_df(
    df=df,
    column='text',
    analyser=analyser,
    entities=['PERSON', 'PHONE_NUMBER', 'LOCATION'],
    inplace=False
)

# Print the result
print(anonymised_df)
```
```Output
                                      text                       text_redacted
0       John Doe's number is 07111 293892.  <PERSON>'s number is 07111 293892.
1  Jane Smith's lives at 123 Shirley Road.     <PERSON>'s lives at <LOCATION>.
```

## 🐙 Kraken integration <a id="kraken_integration"></a>
If using [Kraken](https://github.com/SETT-Centre-Data-and-AI/Kraken) to power your reproducible analytical pipeline, you can easily integrate the two packages, with a full run as follows:

```python
import kraken
import pteredactyl as pt

analyser = pt.create_analyser()

# Extract data from databases
sql_folder = r'C:/...path_to_sql'
results = kraken.run(sql_folder)

df = results.get('histology').df # as an example

# Anonymise the 'text' column
anonymised_df = pt.anonymise_df(
    df=df,
    column='report',
    analyser=analyser,
    entities=['PERSON', 'PHONE_NUMBER', 'LOCATION'],
    inplace=False
)

# Print the result
print(anonymised_df)
```
```Output
                                    report                     report_redacted
0       John Doe's number is 07111 293892.  <PERSON>'s number is 07111 293892.
1  Jane Smith's lives at 123 Shirley Road.     <PERSON>'s lives at <LOCATION>.
```