import torch
from transformers import BertForSequenceClassification, AutoTokenizer

LABELS = ['neutral', 'happiness', 'sadness', 'enthusiasm', 'fear', 'anger', 'disgust']
tokenizer = AutoTokenizer.from_pretrained('Aniemore/rubert-tiny2-russian-emotion-detection')
model = BertForSequenceClassification.from_pretrained('Aniemore/rubert-tiny2-russian-emotion-detection')

@torch.no_grad()
def predict_emotion(text: str) -> str:
    """
        We take the input text, tokenize it, pass it through the model, and then return the predicted label
        :param text: The text to be classified
        :type text: str
        :return: The predicted emotion
    """
    inputs = tokenizer(text, max_length=512, padding=True, truncation=True, return_tensors='pt')
    outputs = model(**inputs)
    predicted = torch.nn.functional.softmax(outputs.logits, dim=1)
    predicted = torch.argmax(predicted, dim=1).numpy()

    return LABELS[predicted[0]]

@torch.no_grad()
def predict_emotions(text: str) -> list:
    """
        It takes a string of text, tokenizes it, feeds it to the model, and returns a dictionary of emotions and their
        probabilities
        :param text: The text you want to classify
        :type text: str
        :return: A dictionary of emotions and their probabilities.
    """
    inputs = tokenizer(text, max_length=512, padding=True, truncation=True, return_tensors='pt')
    outputs = model(**inputs)
    predicted = torch.nn.functional.softmax(outputs.logits, dim=1)
    emotions_list = {}
    for i in range(len(predicted.numpy()[0].tolist())):
        emotions_list[LABELS[i]] = predicted.numpy()[0].tolist()[i]
    return emotions_list



EMOTIONS_STRINGS : dict[str, str] = {
    'neutral' : '🗿 Нейтральный',
    'happiness': '😁 Радостный',
    'sadness': '😭 Грустный',
    'enthusiasm': '🤩 Взбудораженный',
    'anger': '🤬 Злой',
    'disgust': '🤮 Отвращение',
    'fear': '😱 Напуганный'
}

def to_longest(text : str, longest : int) -> str:
    if longest < len(text):
        return text
    return text + ' ' * (longest - len(text))

longest_value = len(max(EMOTIONS_STRINGS.values(), key=len))

# Function for output
def generate_answer(text:str) -> str:
    res_str : str = ''
    emodict : dict = predict_emotions(text)
    for emotion, value in sorted(filter(lambda x: x[1] > 0.05,emodict.items()), key=lambda v: v[1], reverse=True):
        res_str += f'{to_longest(EMOTIONS_STRINGS[emotion], longest_value)} {("%.2f" % value)}\n'
    return res_str

