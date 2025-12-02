from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch


class LLMResponse:
    def __init__(self, model_name="google/flan-t5-base"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

        # Ensure pad token exists
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token

    def get_response(self, user_query, context=""):
        """Get response from the LLM with context"""
        input_text = f"Context: {context}\nUser: {user_query}\nAssistant:" if context else f"User: {user_query}\nAssistant:"

        inputs = self.tokenizer.encode(input_text, return_tensors="pt", max_length=1024, truncation=True)

        with torch.no_grad():
            outputs = self.model.generate(
                inputs,
                max_length=len(inputs[0]) + 100,
                num_return_sequences=1,
                pad_token_id=self.tokenizer.eos_token_id,
                do_sample=True,
                temperature=0.7,
                top_p=0.9
            )

        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        if "Assistant:" in response:
            response = response.split("Assistant:")[-1].strip()

        return response
