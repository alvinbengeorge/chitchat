import time
from ollama import chat
from ollama import ChatResponse

bot1_log = [{
    'role': 'system',
    'content': 'You are talking to another bot about a conversation. Continue talking with them, this conversation should go infinite. ALL I NEED IS A ONE LINE QUESTION. Use simple english language. Stick to the topic.'
}, {
    "role": "user",
    "content": "TOPIC:" + input("Enter your question for Bot 1: ")
}]
bot2_log = [{
    'role': 'system',
    'content': 'You are talking to another bot about a conversation. Continue talking with them, this conversation should go infinite. This is a chat and not a generate, so PLEASE DO REDUCE THE NUMBER OF LINES TO LESS THAN 2. Use simple english language. Stick to the topic.'
}, {
    "role": "user",
    "content": "TOPIC:" + input("Enter your question for Bot 2: ")
}]

start_time = time.time()

while time.time() - start_time < 1000:
    print(time.time() - start_time)
    text = ""
    response: ChatResponse = chat(
        model="gemma3:latest",
        messages=bot1_log,
        options={
            "num_ctx": 300
        },
        stream=True
    )
    print("\nBOT 1 RESPONSE:\n", end="")
    for chunk in response:
        text += chunk.message.content
        print(chunk.message.content, end="", flush=True)
    print()
    bot2_log.append({
        "role": "user",
        "content": text
    })
    bot1_log.append({
        'role': 'bot',
        'content': text
    })
    text=""
    response: ChatResponse = chat(
        model="gemma3:latest",
        messages=bot2_log,
        options={
            "num_ctx": 300
        },
        stream=True
    )
    print("\nBOT 2 RESPONSE:\n", end="")
    for chunk in response:
        text += chunk.message.content
        print(chunk.message.content, end="", flush=True)
    print()
    bot1_log.append({
        "role": "user",
        "content": text
    })
    bot2_log.append({
        "role": "user",
        "content": text
    })


