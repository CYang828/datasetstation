import emoji


def demojize(emoji_str: str):
    return emoji.demojize(emoji_str)


def emojize(emo: str):
    return emoji.emojize(emo)