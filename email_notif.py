import smtplib
from email.mime.text import MIMEText
from typing import Callable, Any, List, Tuple, Dict

def send_email_notification(subject: str, message: str) -> None:
    gmail_user = "change this"
    gmail_app_password = " -> temporary app pwd"
    recipient = "change this"

    msg = MIMEText(message)
    msg['From'] = gmail_user
    msg['To'] = recipient
    msg['Subject'] = subject

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(gmail_user, gmail_app_password)
            server.send_message(msg)
        print("✓ Email sent!")
    except Exception as e:
        print(f"✗ Error: {e}")

class Agent:
    def __init__(self, name: str):
        self.name = name
        self._tasks: List[Tuple[Callable[..., Any], Tuple[Any, ...], Dict[str, Any]]] = []

    def add_task(self, func: Callable[..., Any], *args: Any, **kwargs: Any) -> None:
        self._tasks.append((func, args, kwargs))

    def run(self) -> None:
        print(f"[Agent:{self.name}] Starting {len(self._tasks)} task(s).")
        for i, (func, args, kwargs) in enumerate(self._tasks, start=1):
            try:
                print(f"[Agent:{self.name}] Running task {i}: {getattr(func, '__name__', repr(func))}")
                func(*args, **kwargs)
                print(f"[Agent:{self.name}] Task {i} completed.")
            except Exception as e:
                print(f"[Agent:{self.name}] Task {i} failed: {e}")

class NVIDIAAgent(Agent):
    def __init__(self):
        super().__init__(name="NVIDIA_EmailAgent")

    def preflight_check(self) -> bool:
        return True

if __name__ == "__main__":
    subject = "🚙 Driver Alert! 🚙"
    message = "A driver linked to your account has started a trip! Monitor their drive here: http://localhost:5173" #CHANGE THIS

    # create the agent, add the email task, run it
    agent = NVIDIAAgent()
    if agent.preflight_check():
        agent.add_task(send_email_notification, subject, message)
        agent.run()
    else:
        print("Preflight checks failed;")