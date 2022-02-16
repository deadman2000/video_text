def rec(video_id, frame, text):
    return {'video_id': video_id, 'frame': frame, 'text': text}

data = [
    rec('Oevq2aSOs0M', 721, 'I\'m sure he...pardon me, what did you say?'),
    rec('Oevq2aSOs0M', 727, 'Never mind, I\'m just pulling your leg.  Why don\'t you take this desk right here, and we\'ll get you settled in.'),
    rec('Oevq2aSOs0M', 7702, 'The bottle says: PROFESSOR ABDUL MAAMOUD\'S GUARANTEED SNAKE OIL.'),
    rec('Oevq2aSOs0M', 10064, 'It\'s the personal diary of former museum President Sterling Waldorf-Carlton.'),
    rec('-FV_idCr3jQ', 24, "That accusation is false, Miss Bow. However, the High Priest's identity is a carefully guarded secret, so your failure to identify him is nothing to be ashamed about. He was present at the museum party, but was rarely seen afterwards. One witness said he was spotted briefly in the office of Yvette Delacroix."),
    rec('55qojo9cBBc', 4551, "By reading a few lines from the book, you gather that the theme of this book is that man pays for his crimes against men by suffering for those crimes. It's amazing how much meaning you can get from a few well-chosen words.")
]