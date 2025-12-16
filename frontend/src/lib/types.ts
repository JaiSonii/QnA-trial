// lib/types.ts

export interface Reply {
  id: number;
  content: string;
  created_at: string;
  is_admin: boolean; // Helps us style admin replies differently
}

export interface Question {
  id: number;
  content: string;
  status: "Pending" | "Escalated" | "Answered";
  created_at: string;
  
  // The AI suggestion still lives here (optional)
  answer?: string; 
  
  // NEW: The thread of user/admin responses
  replies: Reply[]; 
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}