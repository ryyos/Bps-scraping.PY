from datetime import datetime as time

class Logs:
    def __init__(self) -> None:
        pass

    def ex(self, type, url) -> None:
        log = f"""
Type: {type}
Base_url: {url}
Status: success
Time: {time.now()}

            """
        
        print(log)