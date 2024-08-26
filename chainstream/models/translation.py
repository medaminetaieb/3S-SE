def detect_language(text: str) -> str:
    from langdetect import detect
    import pycountry

    try:
        language = pycountry.languages.get(alpha_2=detect(text))
        return language.name
    except Exception as e:
        return "English"


def load_t5(model_name="google/flan-t5-base", prefer_cuda=True):
    from torch import cuda
    from transformers import T5Tokenizer, T5ForConditionalGeneration
    from chainstream.models.utils import localize

    model_path = localize(model_name)
    tokenizer = T5Tokenizer.from_pretrained(
        pretrained_model_name_or_path=model_path,
        local_files_only=True,
        clean_up_tokenization_spaces=True,
        legacy=False,
    )
    try:
        model = T5ForConditionalGeneration.from_pretrained(
            pretrained_model_name_or_path=model_path,
            local_files_only=True,
            device_map="auto" if prefer_cuda and cuda.is_available() else "cpu",
        )
    except cuda.OutOfMemoryError as e:
        model = T5ForConditionalGeneration.from_pretrained(
            pretrained_model_name_or_path=model_path,
            local_files_only=True,
        )
    return model, tokenizer


def translate(text: str, target_language="English", translator=load_t5()) -> str:
    input_text = f"translate {detect_language(text)} to {target_language}: " + text
    input_ids = translator[1](input_text, return_tensors="pt").input_ids.to(
        translator[0].device
    )
    return translator[1].decode(
        translator[0].generate(input_ids, max_new_tokens=100)[0],
        skip_special_tokens=True,
    )
