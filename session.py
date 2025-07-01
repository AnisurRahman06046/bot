# session.py
class Session:
    def __init__(self):
        self.state = "main_menu"
        self.selected_category = None
        self.selected_product = None

    def reset(self):
        self.__init__()
