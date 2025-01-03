from colorama import Fore, Back
from typing import Callable

from utils.notify import notify, clear

EXIT_TEXT: str = "Sair"
BACK_TEXT: str = "Voltar"
MAIN_COLOR: str = Fore.YELLOW
OPTION_TEXT: str = "Escolha uma opcao: "
INVALID_OPTION: str = "Opção inválida. Tente novamente."

class Menu:
    def __init__(self, title: str="Menu", exit: bool=True) -> None:
        """
        Initializes the Menu instance.
        :param title: Title of the menu.
        :param exit: Whether to include an exit option.
        """
        self.title = title
        self.entries = []
        self.exit = exit
        self.exit_func = lambda: None
        self.closed = False

    def add_entry(self, text: str, func: Callable, clear_screen: bool=True) -> None:
        """
        Adds an entry to the menu.
        :param text: Display text for the menu option.
        :param func: Function to execute when the option is selected.
        """
        self.entries.append((text, func, clear_screen))

    def default_exit(self, func: Callable):
        """
        Adds an exit option to the menu.
        :param func: Function to execute when the exit option is selected.
        """
        self.exit_func = func
        return func

    def close(self):
        """
        Closes the menu. (So it doesn't interfere with a newly opened menu)
        """
        self.closed = True
        clear()

    @staticmethod
    def press_key():
        """
        Waits for the user to press [ENTER] to continue.
        """
        input(Back.WHITE + Fore.BLACK + "Prima [ENTER] para continuar" + Fore.RESET + Back.RESET)

    def show(self):
        """
        Displays the menu and handles user interaction.
        """
        while not self.closed:
            print(MAIN_COLOR + self.title + Fore.RESET)
            for i, (text, _, _) in enumerate(self.entries, start=1):
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
                    try:
                        self.entries[choice - 1][1]()  # Execute the corresponding function
                    except Exception as e:
                        # Handle the error gracefully without crashing the menu
                        notify("error", f"Erro: {str(e)}")
                        self.press_key()  # Wait for the user to acknowledge the error
                        clear()
                    else:
                        if self.entries[choice - 1][2]:
                            self.press_key()  # Wait for the user to press any key after the function is done
                            clear()
                else:
                    clear()
                    notify("error", INVALID_OPTION)
            except ValueError:
                clear()
                notify("error", INVALID_OPTION)