import time

class SessionManager:
    def __init__(self, expiry_seconds: int):
        """Initialize the session manager with expiry duration.
        :param expiry_seconds: Session lifetime in seconds.
        """
        self.expiry_seconds = expiry_seconds
        self.sessions = {}  # { session_id: creation_time }

    def create_session(self, session_id: str):
        """
        Create a new session with the current timestamp.
        """
        self.sessions[session_id] = time.time()
        return f"Session {session_id} created."
    
    def is_session_active(self, session_id: str) -> bool:
        """
        Check if a session is active based on expiry time.
        Expired sessions are deleted automatically.
        """
        if session_id not in self.sessions:
            return False
        
        creation_time = self.sessions[session_id]
        current_time = time.time()

        # Check expiry
        if current_time - creation_time <= self.expiry_seconds:
            return True
        else:
            # Auto-delete expired session
            del self.sessions[session_id]
            return False
        
    def delete_session(self, session_id: str) -> str:
        """
        Delete a session manually.
        """
        if session_id in self.sessions:
            del self.sessions[session_id]
            return "Deleted"
        return "Session not found."