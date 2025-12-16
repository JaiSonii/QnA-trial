"use client";

import { useEffect, useState } from "react";
import { Question } from "@/lib/types";
import { getQuestions, postQuestion, WS_URL } from "@/lib/api"; // removed markAnswered
import QuestionCard from "@/components/QuestionCard";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import Link from "next/link";
import { LogIn, LogOut, Send } from "lucide-react";
import { postQuestionXHR } from "@/lib/legacyApi";

export default function Dashboard() {
  const [questions, setQuestions] = useState<Question[]>([]);
  const [newQuestion, setNewQuestion] = useState("");
  const [isAdmin, setIsAdmin] = useState(false);

  // 1. Initial Load & Auth Check
  useEffect(() => {
    fetchQuestions();
    const token = localStorage.getItem("token");
    if (token) setIsAdmin(true);
  }, []);

  // 2. WebSocket Connection
  useEffect(() => {
    const ws = new WebSocket(WS_URL);

    ws.onmessage = (event: MessageEvent) => {
      try {
        const message = JSON.parse(event.data as string);

        if (message.type === "NEW_QUESTION") {
          const newQ = message.data;
          setQuestions((prev) => {
            if (prev.some(q => q.id === newQ.id)) return prev;
            return [newQ, ...prev];
          });
          toast.success("New question received!");
        }
        else if (message.type === "NEW_REPLY") {
          toast.info("New reply posted");
          fetchQuestions();
        }
        else {
          fetchQuestions();
        }

      } catch (error) {
        console.error("WS Parse Error", error);
      }
    };

    return () => ws.close();
  }, []);

  const fetchQuestions = async () => {
    try {
      const data = await getQuestions();
      setQuestions(data);
    } catch (error) {
      console.error("Failed to fetch questions", error);
      toast.error("Could not load questions.");
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const token = localStorage.getItem("token");

      await postQuestionXHR(newQuestion, token);

      setNewQuestion("");
      toast.success("Question submitted successfully!");
    } catch (error: any) {
      // Handle the validation error thrown by XHR wrapper
      toast.error(error.message || "Failed to submit question.");
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    setIsAdmin(false);
    window.location.reload();
  };

  return (
    <div className="min-h-screen bg-gray-50 p-4 md:p-8">
      <div className="max-w-3xl mx-auto space-y-8">

        {/* Header */}
        <header className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Hemut Q&A</h1>
            <p className="text-muted-foreground">Real-time community forum</p>
          </div>
          {isAdmin ? (
            <Button variant="ghost" onClick={handleLogout}>
              <LogOut className="mr-2 h-4 w-4" /> Logout
            </Button>
          ) : (
            <Link href="/login">
              <Button variant="outline">
                <LogIn className="mr-2 h-4 w-4" /> Admin Login
              </Button>
            </Link>
          )}
        </header>

        <div className="bg-white p-6 rounded-lg shadow-sm border">
          <h2 className="text-lg font-semibold mb-4">Ask a Question</h2>
          <form onSubmit={handleSubmit} className="flex gap-4">
            <Input
              value={newQuestion}
              onChange={(e) => setNewQuestion(e.target.value)}
              placeholder="What would you like to know?"
              className="flex-1"
            />
            <Button type="submit">
              <Send className="mr-2 h-4 w-4" /> Ask
            </Button>
          </form>
        </div>

        <div className="space-y-4">
          <h2 className="text-xl font-semibold">Community Discussion</h2>
          {questions.length === 0 ? (
            <p className="text-center text-muted-foreground py-8">No questions yet. Be the first!</p>
          ) : (
            questions.map((q) => (
              <QuestionCard
                key={q.id}
                question={q}
                isAdmin={isAdmin}
                onRefresh={fetchQuestions} // Pass the refresh trigger down
              />
            ))
          )}
        </div>
      </div>
    </div>
  );
}