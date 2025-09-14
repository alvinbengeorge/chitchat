import time
from ollama import chat, ChatResponse
from ollama import generate

# Shared system instructions for both bots
SYSTEM_PROMPT = """
You are one of two bots engaged in a debate. 
Rules for the debate:
- Stay strictly on the given topic.
- Keep replies short, clear, and conversational.
- Use simple layman’s English.
- Make sure your points are logical, factual, and valid.
"""

# Get topics for both bots
bot1_topic = input("Enter debate topic for Bot 1: ")
bot2_topic = input("Enter debate topic for Bot 2: ")

# Logs for each bot
bot1_log = [
    {"role": "system", "content": f"{SYSTEM_PROMPT}\nTOPIC: {bot1_topic}"}
]
bot2_log = [
    {"role": "system", "content": f"{SYSTEM_PROMPT}\nTOPIC: {bot2_topic}"}
]

def get_response(bot_log, model="gemma3:1b"):
    """Helper to fetch a streaming response from a bot."""
    response: ChatResponse = chat(
        model=model,
        messages=bot_log,
        options={"num_ctx": 300},
        stream=True
    )
    text = ""
    for chunk in response:
        text += chunk.message.content
        print(chunk.message.content, end="", flush=True)
    print()
    return text

# Start debate loop
start_time = time.time()
rounds = 0

while time.time() - start_time < 200:  # Or replace with: while rounds < 10
    rounds += 1
    elapsed = int(time.time() - start_time)
    print(f"\n--- Round {rounds} (at {elapsed}s) ---")

    # Bot 1 speaks (always assistant)
    print("\nBOT 1 RESPONSE:")
    bot1_reply = get_response(bot1_log)
    bot1_log.append({"role": "assistant", "content": bot1_reply})
    bot2_log.append({"role": "user", "content": bot1_reply})

    # Bot 2 replies (always assistant)
    print("\nBOT 2 RESPONSE:")
    bot2_reply = get_response(bot2_log)
    bot2_log.append({"role": "assistant", "content": bot2_reply})
    bot1_log.append({"role": "user", "content": bot2_reply})

