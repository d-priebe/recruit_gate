from pathlib import Path
import openai
import time


class GPTScraper:
    def __init__(self):
        self.openai_key = self.open_file(Path.cwd() / 'data/OpenAikey.txt')
        openai.api_key = self.openai_key
       
        
        self.memory_system = {"Title":[
                                {"role": "system", "content": ""},
                            ],
                            "Summary":[
                                {"role": "system", "content": ""},
                            ],
                            
                            "Commit_Prompt":[                
                                {"role": "system", "content":  self.open_file(Path.cwd()/'prompts/commit_prompt.txt')},
                            ],
                            
                            "Hyper_Prompt":[                
                                {"role": "system", "content":  self.open_file(Path.cwd()/'prompts/commit_hyper_prompt.txt')},
                            ]
                        }

    def open_file(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as infile:
            return infile.read()

    def Memory_Selection(self, Current_prompt):
        return self.memory_system.get(Current_prompt, [])

    def chat_update(self, messages, role, content):
        messages.append({"role": role, "content": content})
        return messages

    def chatGPT_response(self,messages):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Ensure correct model name
                messages=messages,
                temperature=0.9
            )
            return response['choices'][0]['message']['content']
        except openai.APIError as e:
            if e.__class__.__name__ == 'RateLimitError':
                print("Rate limit exceeded, waiting to retry...")
                time.sleep(10)  
                return self.chatGPT_response(messages) 
            else:
                raise e

    def scrape(self, Current_prompt, raw_html):
        
        initial_prompt = self.Memory_Selection(Current_prompt)
        initial_prompt = initial_prompt[0]['content'].replace('<<raw_html>>', raw_html)
        messages = self.chat_update([], "user", initial_prompt) 

        model_response = self.chatGPT_response(messages)
        return model_response

