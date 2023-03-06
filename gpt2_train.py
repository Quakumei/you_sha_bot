from transformers import GPT2LMHeadModel, GPT2Tokenizer
from transformers import AutoTokenizer, AutoModelWithLMHead, TextDataset, DataCollatorForLanguageModeling, Trainer, TrainingArguments

# Load the pre-trained RuGPT2 model and tokenizer
model_name = "sberbank-ai/rugpt2large"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelWithLMHead.from_pretrained(model_name)

# Load the text file containing your data
train_data = TextDataset(
    tokenizer=tokenizer,
    file_path='path/to/your/text/file.txt',
    block_size=128
)

# Create a data collator to batch and pad the data
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer, mlm=False
)

# Set up the training arguments and trainer
training_args = TrainingArguments(
    output_dir='./results',
    overwrite_output_dir=True,
    num_train_epochs=3,
    per_device_train_batch_size=16,
    save_steps=1000,
    save_total_limit=2,
    prediction_loss_only=True,
    logging_steps=500
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_data,
    data_collator=data_collator
)

# Fine-tune the model on your data
trainer.train()

# Generate responses to user input
def generate_response(input_text):
    input_ids = tokenizer.encode(input_text, return_tensors='pt')
    output_ids = model.generate(input_ids)
    output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return output_text
