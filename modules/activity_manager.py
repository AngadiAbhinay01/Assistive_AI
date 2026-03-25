class ActivityManager:
    def __init__(self, steps):
        self.steps = steps
        self.current_step = 0
        self.started = False

    def start(self):
        """
        Start the activity
        """
        self.started = True
        self.current_step = 0
        return self.steps[self.current_step]

    def next_step(self):
        """
        Move to next step
        """
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
        return self.steps[self.current_step]

    def previous_step(self):
        """
        Move to previous step
        """
        if self.current_step > 0:
            self.current_step -= 1
        return self.steps[self.current_step]

    def repeat_step(self):
        """
        Repeat current step
        """
        return self.steps[self.current_step]