class speech_terms:
    def __init__(self):
        self._hesitation_words = ("like", "uh", "so", "um", "actually", "basically", "just", "right", "seem", "seriously", "well", "literally", "totally")
        self._hesitation_terms = ("you know", "i guess", "i suppose", "you see", "i mean", "or something", "you know what i mean", "believe me")
        self._filler_words = () # not sure the difference b/w filler and hesitation, temporarily view them as the same 
        self._filler_terms = ()
        self._memory_words = ("remember", "recall", "recollect", "forget", "forgot")
        self._memory_terms = ("")
        self.negation = ("no", "not")