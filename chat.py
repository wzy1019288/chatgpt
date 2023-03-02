import os
import openai
from utils import save_json, load_json

path = os.path.expanduser('~')
record_path = '{}{}{}'.format(path, os.sep, '.chatgpt/records')


# record_path = 'chat_record'
record_name = 'cache'
if not os.path.exists(record_path):
    os.makedirs(record_path)



def get_path_and_log(data_name=None):
    ''''''

    if data_name is not None:
        new_path = os.path.join(record_path, data_name) + '.json'
        message_log = load_json(new_path)
        return new_path, message_log

    existed_train_data = [js.split('.')[0] for js in os.listdir(record_path) if js != 'cache.json']
    if len(existed_train_data) > 0:
        print('Now we have trained data:')
        for i in range(len(existed_train_data)):
            print(f'[{i+1}] {existed_train_data[i]}')
        
        # 选择旧的数据继续训练
        print("\nIf you want to choose a trained data, please input the Number.\nOr you can input any word or press 'Enter' to continue.")
        while True:
            number = input()
            try:
                number = int(number)
                if number in range(1, len(existed_train_data)+1):
                    new_path = os.path.join(record_path, existed_train_data[number-1]) + '.json'
                    message_log = load_json(new_path)
                    return new_path, message_log
                else:
                    print(f'You have input a number but not correct. (Int should between [1, {len(existed_train_data)}])')
                    print("If you input a wrong number, you can continue to input the correct number. Or press 'Enter' to continue.")
                    continue
            except Exception as e:
                # print(e)
                break

    # 使用新的数据重新训练
    print("\nIf you want to create a new data, please input the date name, like 'TEST1'.\nOr you can press 'Enter' to continue.")
    data_name = input()

    if data_name != '':
        new_path = os.path.join(record_path, data_name) + '.json'
        message_log = []
        save_json(new_path, message_log)
    else:
        new_path = os.path.join(record_path, record_name) + '.json'
        message_log = []
        save_json(new_path, message_log)
    
    return new_path, message_log
        

    


# Set up OpenAI API key
api_key = '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'
openai.api_key = api_key

# Function to send a message to the OpenAI chatbot model and return its response
def send_message(message_log):
    # Use OpenAI's ChatCompletion API to get the chatbot's response
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # The name of the OpenAI chatbot model to use
        messages=message_log,   # The conversation history up to this point, as a list of dictionaries
        # max_tokens=4096,        # The maximum number of tokens (words or subwords) in the generated response
        # stop=None,              # The stopping sequence for the generated response, if any (not used here)
        # temperature=0.7,        # The "creativity" of the generated response (higher temperature = more creative)
    )

    # Find the first response from the chatbot that has text in it (some responses may not have text)
    for choice in response.choices:
        if "text" in choice:
            return choice.text

    # If no response with text is found, return the first response's content (which may be empty)
    return response.choices[0].message.content


# Main function that runs the chatbot
def main(data_name=None):

    # Set a flag to keep track of whether this is the first request in the conversation
    first_request = True

    print('='*30 + ' ChatGPT ' + '='*30)
    new_path, message_log = get_path_and_log(data_name)

    # Start a loop that runs until the user types "quit"
    while True:

        save_json(new_path, message_log)

        if first_request:
            # If this is the first request, get the user's input and add it to the conversation history
            user_input = input("\n[You]: ")
            message_log.append({"role": "user", "content": user_input})

            # Send the conversation history to the chatbot and get its response
            response = send_message(message_log)

            # Add the chatbot's response to the conversation history and print it to the console
            message_log.append({"role": "assistant", "content": response})
            print(f"\n[ChatGPT]: {response}")

            # Set the flag to False so that this branch is not executed again
            first_request = False
        else:
            # If this is not the first request, get the user's input and add it to the conversation history
            user_input = input("\n[You]: ")

            # If the user types "quit", end the loop and print a goodbye message
            if user_input.lower() == "quit":
                print("Goodbye!")
                break

            message_log.append({"role": "user", "content": user_input})

            # Send the conversation history to the chatbot and get its response
            response = send_message(message_log)

            # Add the chatbot's response to the conversation history and print it to the console
            message_log.append({"role": "assistant", "content": response})
            print(f"\n[ChatGPT]: {response}")


# Call the main function if this file is executed directly (not imported as a module)
if __name__ == "__main__":
    main()