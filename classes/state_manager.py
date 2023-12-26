class StateManager:
    def __init__(self):
        self.current_state = None
        self.previous_state = None

    def update_state(self, state):
        self.previous_state = self.current_state
        self.current_state = state
