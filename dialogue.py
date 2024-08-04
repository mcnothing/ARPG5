import json

class Dialogue:
    def load_json() -> json:
        with open('assets/json/dialogues.json') as f:
            return json.load(f)
    master_topics = load_json()    

    def __init__(self, dialogue_choices: list) -> None:
        self.topics = {}
        # Go through JSON file and add dialogue responses to dictionary, on per-character basis.
        for topic in dialogue_choices:
            self.add_topic(topic)
        
    def add_topic(self, topic: str) -> None:
        self.topics[topic] = Dialogue.master_topics[topic]

    def get_topic(self, topic: str) -> str:
        return self.topics[topic]

    def get_line(self, topic: str, index: int) -> str:
        return self.topics[topic][index]
