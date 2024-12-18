import spacy
import pandas as pd

# Load the English language model
nlp = spacy.load("en_core_web_sm")
df = pd.read_csv("data.csv")

def extract_named_entities(sentence):
    # Process the sentence using spaCy
    doc = nlp(sentence)
    
    # Extract named entities from the sentence
    named_entities = [ent.text for ent in doc.ents if ent.label_ in ("ORG", "PRODUCT")]
    return named_entities

# Example usage

for index, row in df.iterrows():
    sentence = row.iloc[0]
    entities = extract_named_entities(sentence)
    print(sentence)
    print(f"Named entities in the sentence: {entities}")
    input()
