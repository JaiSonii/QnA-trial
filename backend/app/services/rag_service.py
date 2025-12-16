class RAGService:
    def __init__(self):
        self.mock_knowledge = {
            "login": "To login, please click the 'Login' button at the top right. You need an admin account to enter.",
            "admin": "Admins have the ability to mark questions as answered and view the dashboard statistics.",
            "event": "The event starts at 9:00 AM and ends at 5:00 PM EST.",
            "submit": "Guests can submit questions using the form on the main page. No login is required.",
            "fastapi": "This backend is built using FastAPI for high performance and easy async support."
        }

    def generate_answer(self, query: str) -> str:
        """
        Simulates an AI analyzing the question and finding a relevant answer.
        """
        query_lower = query.lower()
        
        for key, answer in self.mock_knowledge.items():
            if key in query_lower:
                return f"AI Suggestion: {answer}"
        
        return "AI Suggestion: I couldn't find a specific answer in the documentation. Please wait for an Admin."

rag_service = RAGService()