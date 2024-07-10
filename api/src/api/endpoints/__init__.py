from time import time

from src.services.agents_service import initialize_agents
from src.services.pool_service import MessagingPoolManager


class SessionManager:
    def __init__(self):
        self.sessions = {}
        self.last_time_used = {}

    def get_session(self, session_id: str):
        current_time = time()
        if session_id not in self.sessions or (
            session_id in self.last_time_used
            and current_time - self.last_time_used[session_id] > 3600
        ):
            agents = initialize_agents()
            self.sessions[session_id] = MessagingPoolManager(agents)
            self.last_time_used[session_id] = current_time
        return self.sessions[session_id]
