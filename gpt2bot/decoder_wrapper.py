import random

from gpt2bot.decoder import generate_response
from database.database_wrapper import read_injected_turns


def generateTurn(turns, prompt, max_turns_history, num_samples, model, tokenizer, config, mmi_model, mmi_tokenizer):
    # A single turn is a group of user messages and bot responses right after
    turn = {
        'user_messages': [],
        'bot_messages': []
    }
    injected_turns = read_injected_turns()
    turns += injected_turns
    # todo something with injection of bot replies might go wrong
    turns.append(turn)
    turn['user_messages'].append(prompt)
    # Merge turns into a single history (don't forget EOS token)
    history = ""
    from_index = max(len(turns) - max_turns_history - 1, 0) if max_turns_history >= 0 else 0
    for turn in turns[from_index:]:
        # Each turn begings with user messages
        for message in turn['user_messages']:
            history += message + tokenizer.eos_token
        for message in turn['bot_messages']:
            history += message + tokenizer.eos_token
    # Generate bot messages
    bot_messages = generate_response(
        model,
        tokenizer,
        history,
        config,
        mmi_model=mmi_model,
        mmi_tokenizer=mmi_tokenizer
    )
    if num_samples == 1:
        bot_message = bot_messages[0]
    else:
        # TODO: Select a message that is the most appropriate given the context
        # This way you can avoid loops
        bot_message = random.choice(bot_messages)
    turn['bot_messages'].append(bot_message)

    return bot_message, turns
