
try:
    from .browser_controller import BrowserController
    from .gemini_client import analyze_screen
    from .action_executor import execute_action
except ImportError:
    from browser_controller import BrowserController
    from gemini_client import analyze_screen
    from action_executor import execute_action

class VisionPilotAgent:

    def __init__(self, browser=None):
        self.browser = browser or BrowserController()

    def run(self, goal):

        self.browser.open_site("https://www.amazon.in")

        for step in range(6):

            screenshot = self.browser.screenshot()

            action = analyze_screen(goal, screenshot)

            print("Agent Decision:", action)

            finished = execute_action(self.browser, action)

            if finished:
                return "Task Completed"

        return "Stopped after max steps"
