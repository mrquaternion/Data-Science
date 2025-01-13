# 1. Entraînement initial
print("=== Phase 1: Entraînement Initial ===")
model, tokenizer = setup_model_and_tokenizer()
dataset = load_dataset('gberseth/IFT6758-comments', split="train")
dataset = dataset.map(lambda example: {'text': example['input'] + example['output']})

training_args = get_training_args()
peft_config = get_peft_config()
trained_model, train_result = train_model(model, tokenizer, dataset, peft_config, training_args)

# 2. Test initial
print("\n=== Phase 2: Test Initial ===")
test_input = "Hello, how are you?"
initial_output = generate_response(trained_model, tokenizer, test_input)
print(f"Input: {test_input}")
print(f"Output initial: {initial_output}")

# 3. Ajout d'un nouvel exemple et ré-entraînement
print("\n=== Phase 3: Ré-entraînement avec données augmentées ===")
new_example = {
    'input': 'Hi, how are you doing?',
    'output': 'I am doing well, thank you for asking! I am here to help you.',
    'text': 'Hi, how are you doing? I am doing well, thank you for asking! I am here to help you.'
}
augmented_dataset = dataset.add_item(new_example)
retrained_model, retrain_result = train_model(model, tokenizer, augmented_dataset, peft_config, training_args)

# 4. Test avec le même input sur le modèle ré-entraîné
print("\n=== Phase 4: Test Final ===")
final_output = generate_response(retrained_model, tokenizer, test_input)
print(f"Input: {test_input}")
print(f"Output final: {final_output}")

# Comparaison des résultats
print("\n=== Comparaison des Résultats ===")
print("\nRéponse initiale:", initial_output)
print("\nRéponse finale:", final_output)
