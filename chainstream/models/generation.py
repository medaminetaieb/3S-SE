def phi3(prefer_cuda=True):
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
    from chainstream.models.utils import localize

    torch.random.manual_seed(0)

    model_path = localize("microsoft/Phi-3-mini-4k-instruct")
    tokenizer = AutoTokenizer.from_pretrained(model_path, legacy=False)
    try:
        model = AutoModelForCausalLM.from_pretrained(
            model_path,
            device_map="auto" if prefer_cuda and torch.cuda.is_available() else "cpu", 
            torch_dtype="auto", 
            trust_remote_code=True, 
        )
    except torch.cuda.OutOfMemoryError as e:
        model = AutoModelForCausalLM.from_pretrained(
            model_path, 
            torch_dtype="auto", 
            trust_remote_code=True, 
        )

    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
    )
    return pipe

    messages = [
        {"role": "user", "content": "Can you provide ways to eat combinations of bananas and dragonfruits?"},
        {"role": "assistant", "content": "Sure! Here are some ways to eat bananas and dragonfruits together: 1. Banana and dragonfruit smoothie: Blend bananas and dragonfruits together with some milk and honey. 2. Banana and dragonfruit salad: Mix sliced bananas and dragonfruits together with some lemon juice and honey."},
        {"role": "user", "content": "What about solving an 2x + 3 = 7 equation?"},
    ]

    generation_args = {
        "max_new_tokens": 500,
        "return_full_text": False,
        "temperature": 0.0,
        "do_sample": False,
    }

    output = pipe(messages, **generation_args)
    print(output[0]['generated_text'])
