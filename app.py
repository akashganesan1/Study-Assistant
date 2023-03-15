from flask import Flask, render_template, request
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from gpt_index import SimpleDirectoryReader, GPTListIndex, GPTSimpleVectorIndex, LLMPredictor, PromptHelper
from langchain import OpenAI
import sys
import os
from flask_cors import CORS

os.environ["OpenAI_API_KEY"] = "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"
def createVectorIndex(path):
    max_input = 4096
    tokens = 256
    chunk_size = 600
    max_chunk_overlap = 20
    Prompt_helper = PromptHelper(max_input, tokens, max_chunk_overlap, chunk_size_limit=chunk_size)

    # define LLM
    llmPredictor = LLMPredictor(llm=OpenAI(temperature=0, model_name="text-davinci-002", max_tokens=tokens))

    # load_data
    docs = SimpleDirectoryReader(path).load_data()

    # create vector index
    Vector_index = GPTSimpleVectorIndex(documents=docs, llm_predictor=llmPredictor, prompt_helper=Prompt_helper)
    Vector_index.save_to_disk('vectorindex.json')
    return Vector_index
vector_index = createVectorIndex(r"P:\knowledge")
def answer_me(vector_index,promptInput):
    vIndex = GPTSimpleVectorIndex.load_from_disk(vector_index)
    while True:
        prompt = promptInput
        response = vIndex.query(prompt,response_mode ="compact")
        print(f"Response : {response} \n")
        return response

app = Flask(__name__)
# Set up the chatbot model
CORS(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get-response', methods=['POST'])
def get_response():
    # Get the user's prompt and generate a response
    print(request.json)

    prompt_input = request.json['prompt']
    global context
    if prompt_input == "reset":
        context = None  # Reset context when user requests to start a new conversation
        response = "Conversation reset. How may I assist you?"
    else:
        response, context = answer_me('vectorindex.json', prompt_input, context=context)

    # Return the response as JSON
    return {'response': response}




def generate_response(prompt):
    # encode the prompt and generate text using the model
    input_ids = tokenizer.encode(prompt, return_tensors='pt')
    output_ids = model.generate(input_ids, do_sample=True, max_length=50, top_k=50)

    # decode the generated text and return
    response = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return response


if __name__ == '__main__':
    app.run(port=5000)
