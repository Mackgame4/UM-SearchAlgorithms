from colorama import Fore
from utils.notify import notify, clear, press_key

EXIT_TEXT = "Sair"
BACK_TEXT = "Voltar"
MAIN_COLOR = Fore.YELLOW
OPTION_TEXT = "Escolha uma opcao: "
INVALID_OPTION = "Opção inválida. Tente novamente."

class Menu:
    """
    Initializes the Menu instance.
    :param title: Title of the menu.
    :param exit: Whether to include an exit option.
    """
    def __init__(self, title="Menu", exit=True):
        self.title = title
        self.entries = []
        self.exit = exit
        self.exit_func = lambda: None
        self.closed = False

    """
    Adds an entry to the menu.
    :param text: Display text for the menu option.
    :param func: Function to execute when the option is selected.
    """
    def add_entry(self, text, func):
        self.entries.append((text, func))

    """
    Adds an exit option to the menu.
    """
    def default_exit(self, func):
        self.exit_func = func
        return func
    
    """
    Closes the menu. (So it doent interfere with a new opened menu)
    """
    def close(self):
        self.closed = True
        clear()

    """
    Displays the menu and handles user interaction.
    """
    def show(self):
        while not self.closed:
            print(MAIN_COLOR + self.title + Fore.RESET)
            for i, (text, _) in enumerate(self.entries, start=1):
                print(MAIN_COLOR + f"{i} - " + Fore.RESET + text)
            if self.exit:
                print(MAIN_COLOR + "0 - " + Fore.RESET + EXIT_TEXT)
            else:
                print(MAIN_COLOR + "0 - " + Fore.RESET + BACK_TEXT)

            try:
                choice = int(input(MAIN_COLOR + OPTION_TEXT + Fore.RESET))
                if choice == 0:
                    self.exit_func()
                    break
                elif 1 <= choice <= len(self.entries):
                    self.entries[choice - 1][1]() # Execute the corresponding function
                    press_key()
                    clear()
                else:
                    clear()
                    notify("error", INVALID_OPTION)
            except ValueError:
                clear()
                notify("error", INVALID_OPTION)