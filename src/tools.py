from datetime import datetime

def log(text):
    """is used to log things with the time at the begining"""    
    GREEN = "\033[38;5;40m"
    RESET = "\033[0m"
    current_time = datetime.now().strftime("[%H:%M]")
    print(f"{GREEN}{current_time} {text}{RESET}")

def log_error(text):
    """is used to log errors with the time at the begining and a red color"""    
    RED = "\033[38;5;196m"
    RESET = "\033[0m"
    current_time = datetime.now().strftime("[%H:%M]")
    print(f"{RED}{current_time} {text}{RESET}")