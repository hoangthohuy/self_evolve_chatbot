from transformers import AutoTokenizer

from transformers import AutoModelForSequenceClassification
import torch

list_style = [
	{"label":"formal"},
	{"label":"informal"},
]

id2label_style = {i:label['label'] for i, label in enumerate(list_style)}
label2id_style = {label['label']:i for i, label in enumerate(list_style)}
id2label_style
label2id_style

formal_informal_classifier = AutoModelForSequenceClassification.from_pretrained(
    "./models/formal_informal_classification/checkpoint-18",
    num_labels=len(list_style),
    id2label=id2label_style,
    label2id=label2id_style,
)


def informal_or_not(text,tokenizer):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding="max_length", max_length=256)
    with torch.no_grad():
        outputs = formal_informal_classifier(**inputs)

    logits = outputs.logits          # [1, num_labels]
    predicted_informal_or_not = logits.argmax(dim=-1).item()

    return (predicted_informal_or_not)



