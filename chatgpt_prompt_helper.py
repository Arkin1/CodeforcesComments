from selenium import webdriver
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
import time
import socket
import threading
import os
import urllib.parse
from markupsafe import escape


class ChatGPTAutomation:
    def __init__(self, chrome_path, chrome_driver_path):
        """
        This constructor automates the following steps:
        1. Open a Chrome browser with remote debugging enabled at a specified URL.
        2. Prompt the user to complete the log-in/registration/human verification, if required.
        3. Connect a Selenium WebDriver to the browser instance after human verification is completed.

        :param chrome_path: file path to chrome.exe (ex. C:\\Users\\User\\...\\chromedriver.exe)
        :param chrome_driver_path: file path to chrome.exe (ex. C:\\Users\\User\\...\\chromedriver.exe)
        """

        self.chrome_path = chrome_path
        self.chrome_driver_path = chrome_driver_path

        url = r"https://chat.openai.com"
        free_port = self.find_available_port()
        self.launch_chrome_with_remote_debugging(free_port, url)
        self.wait_for_human_verification()
        self.driver = self.setup_webdriver(free_port)

    def find_available_port(self):
        """ This function finds and returns an available port number on the local machine by creating a temporary
            socket, binding it to an ephemeral port, and then closing the socket. """

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            return s.getsockname()[1]



    def launch_chrome_with_remote_debugging(self, port, url):
        """ Launches a new Chrome instance with remote debugging enabled on the specified port and navigates to the
            provided url """

        def open_chrome():
            chrome_cmd = f"{self.chrome_path}  --user-data-dir=D:\Work --remote-debugging-port={port} {url}"
            os.system(chrome_cmd)

        chrome_thread = threading.Thread(target=open_chrome)
        chrome_thread.start()

    def setup_webdriver(self, port):
        """  Initializes a Selenium WebDriver instance, connected to an existing Chrome browser
             with remote debugging enabled on the specified port"""
        options = webdriver.ChromeOptions()
        options.add_experimental_option("debuggerAddress", f"127.0.0.1:{port}")
        driver = webdriver.Chrome(options=options)
        return driver

    def send_prompt_to_chatgpt(self, prompt):
        """ Sends a message to ChatGPT and waits for 20 seconds for the response """
        input_box = self.driver.find_element(by=By.XPATH, value='//textarea[contains(@placeholder, "Send a message")]')

        self.driver.execute_script(f"arguments[0].value = arguments[1];", input_box, prompt)
        input_box.send_keys(Keys.RETURN)
        input_box.send_keys(Keys.ENTER)
        time.sleep(1)

        while(True):
            try:
                self.driver.find_element(by = By.XPATH, value="//div[@class ='text-2xl']")
                a=1
            except:
                break
        time.sleep(1)


    def return_chatgpt_conversation(self):
        """
        :return: returns a list of items, even items are the submitted questions (prompts) and odd items are chatgpt response
        """

        return self.driver.find_elements(by=By.CSS_SELECTOR, value='div.text-base')



    def save_conversation(self, round_type, file_name):
        """
        It saves the full chatgpt conversation of the tab open in chrome into a text file, with the following format:
            prompt: ...
            response: ...
            delimiter
            prompt: ...
            response: ...

        :param file_name: name of the file where you want to save
        """

        directory_name = f"conversations/{round_type}"
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)

        delimiter = "|^_^|"
        chatgpt_conversation = self.return_chatgpt_conversation()
        with open(os.path.join(directory_name, file_name), "a", encoding='utf-8') as file:
            for i in range(0, len(chatgpt_conversation), 4):
                file.write(
                    f"prompt: {chatgpt_conversation[i].text}\nresponse: {chatgpt_conversation[i + 2].text}\n\n{delimiter}\n\n")



    def return_last_response(self):
        """ :return: the text of the last chatgpt response """

        response_elements = self.driver.find_elements(by=By.CSS_SELECTOR, value='div.text-base')
        return response_elements[-1].text



    def wait_for_human_verification(self):
        print("You need to manually complete the log-in or the human verification if required.")

        while True:
            user_input = input(
                "Enter 'y' if you have completed the log-in or the human verification, or 'n' to check again: ").lower()

            if user_input == 'y':
                print("Continuing with the automation process...")
                break
            elif user_input == 'n':
                print("Waiting for you to complete the human verification...")
                time.sleep(5)  # You can adjust the waiting time as needed
            else:
                print("Invalid input. Please enter 'y' or 'n'.")



    def quit(self):
        """ Closes the browser and terminates the WebDriver session."""
        print("Closing the browser...")
        self.driver.close()
        self.driver.quit()

# prompt = "What are the benefits of exercise?"
# chatgpt.send_prompt_to_chatgpt(prompt)
# chatgpt.send_prompt_to_chatgpt(prompt)
# chatgpt.send_prompt_to_chatgpt(prompt)
# chatgpt.send_prompt_to_chatgpt(prompt)

# # Retrieve the last response from ChatGPT
# response = chatgpt.return_last_response()
# print(response)

# # Save the conversation to a text file
# file_name = "conversation.txt"
# chatgpt.save_conversation(file_name)

# # Close the browser and terminate the WebDriver session
# chatgpt.quit()
PROMPT_FOLDER = 'prompt_generation'
ROUND_TYPE = 'educ'
ID = 2
with open(f'{PROMPT_FOLDER}/prompt.txt', 'r') as fp:
    prompt = fp.read()

ROUND_FOLDER = f'{PROMPT_FOLDER}/{ROUND_TYPE}/test/{ID}'

trees_file_names = []

for file_name in os.listdir(ROUND_FOLDER):
    trees_file_names.append(file_name)

from collections import defaultdict
ref_trees = defaultdict(dict)
round_trees = defaultdict(dict)

for fn in [file_name for file_name in trees_file_names if file_name.startswith('ref')]:
    root = fn.split('_')[1]
    type = fn.split('_')[2].split('.')[0]

    with open(f'{ROUND_FOLDER}/{fn}', 'r', encoding = 'utf-8') as fp:
        ref_trees[root][type] = fp.read()

for fn in [file_name for file_name in trees_file_names if not file_name.startswith('ref')]:
    root = fn.split('_')[0]
    type = fn.split('_')[1].split('.')[0]

    with open(f'{ROUND_FOLDER}/{fn}', 'r', encoding = 'utf-8') as fp:
        round_trees[root][type] = fp.read()

total_chars = 0
for tree_data in round_trees.values():
    if(total_chars == 0):
        chatgpt = ChatGPTAutomation('\"C:/Program Files (x86)/Google/Chrome/Application/chrome.exe\"', 'chromedriver.exe')
        chatgpt.send_prompt_to_chatgpt(prompt)
        total_chars+= len(prompt)
    # idx = 0
    # for tree_data in ref_trees.values():
    #     chatgpt.send_prompt_to_chatgpt('%rule%\n' + tree_data['input'])
    #     chatgpt.send_prompt_to_chatgpt('%rule%\n' + tree_data['output'])
    #     idx+=1
    #     if(idx % 10 == 0):
    #         chatgpt.send_prompt_to_chatgpt(f'Here is a recap of the rules \n{prompt}')

    #chatgpt.send_prompt_to_chatgpt('A NEW COMMENT TREE HAS APPEARED')

    chat_prompt = '%rule%\n' + tree_data['input']
    chatgpt.send_prompt_to_chatgpt(chat_prompt)
    #chatgpt.send_prompt_to_chatgpt('%rule%\n' + tree_data['output'])
    total_chars+= len(chat_prompt)

    if(total_chars >= 10000):
        file_name = f"{ID}.txt"
        chatgpt.save_conversation(ROUND_TYPE, file_name)
        print("Chat was saved!")

        total_chars = 0

        chatgpt.quit()

if(total_chars > 0):
    file_name = f"{ID}.txt"
    chatgpt.save_conversation(ROUND_TYPE, file_name)
    print("Chat was saved!")

chatgpt.quit()

