import random


class UserAgentRotator(object):
    """Create a random header from the proxy list

    Parameters
    ----------
    path: str
        path of the file, the user_agent delimiting the list by new line
    """

    def __init__(self, path='utils/configs/user_agent.txt'):
        self.user_agents = self.__load_user_agents(path=path)

    @staticmethod
    def __load_user_agents(path):
        with open(path) as file:
            user_agents = [str(line.strip()) for line in file]
        return user_agents

    def get_user_agent(self):
        return random.choice(self.user_agents)

    def generate_header(self):
        """
        Returns
        -------
        header: Dict[str]
            returns a dict with keys Connection and User-Agent
        """
        header = {
            "Connection": "close",
            "User-Agent": self.get_user_agent()
        }
        return header
