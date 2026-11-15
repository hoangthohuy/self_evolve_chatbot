from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
import torch
list_label = [
	{"label":"fail"},
	{"label":"success"},
]
id2label_label = {i:label['label'] for i, label in enumerate(list_label)}
label2id_label = {label['label']:i for i, label in enumerate(list_label)}

outcome_classifier = AutoModelForSequenceClassification.from_pretrained(
    "./models/outcome_classification/checkpoint-44",
    num_labels=2,
    id2label=id2label_label,
    label2id=label2id_label,
)

def outcome(text,tokenizer):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding="max_length", max_length=256)
    with torch.no_grad():
        outputs = outcome_classifier(**inputs)

    logits = outputs.logits          # [1, num_labels]
    predicted_informal_or_not = logits.argmax(dim=-1).item()

    return (id2label_label[predicted_informal_or_not])