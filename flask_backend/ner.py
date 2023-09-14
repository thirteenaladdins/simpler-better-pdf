import spacy
from spacy.util import minibatch
import random

# Create a new blank English model
nlp = spacy.blank('en')

# Add the NER component
ner = nlp.add_pipe('ner')

# Add your entity labels
labels = ["HS_CODE", "QUANTITY", "NET_WEIGHT", "GROSS_WEIGHT", "PRODUCT_DESCRIPTION", "COO", "UNIT_PRICE", "TOTAL_PRICE"]
for label in labels:
    ner.add_label(label)

# Here's an example of how you might process and print entities. For this example, I'll use the "en_core_web_md" model.
# It's a separate pipeline, and we're using it just for demonstration.
demo_nlp = spacy.load("en_core_web_md")
demo_doc = demo_nlp("Apple is looking to buy a U.K. startup for $1 billion")

# Print named entities from the demo text
for ent in demo_doc.ents:
    print(ent.text, ent.label_)

# Note: In the training phase, you'll need to use the 'nlp' pipeline you created to process your texts and update the model weights.


# TRAINING MODEL

# TRAIN_DATA = [...] # Your annotated data

# # Train the model
# optimizer = nlp.begin_training()
# for i in range(10):
#     random.shuffle(TRAIN_DATA)
#     batches = minibatch(TRAIN_DATA, size=8)
#     for batch in batches:
#         texts, annotations = zip(*batch)
#         nlp.update(texts, annotations, sgd=optimizer)
