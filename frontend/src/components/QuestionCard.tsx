import { useState } from "react";
import { Question } from "@/lib/types";
import { postReply, updateStatus } from "@/lib/api";
import { Card, CardHeader, CardContent, CardFooter } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Separator } from "@/components/ui/separator";
import { formatDistanceToNow } from "date-fns";
import { CheckCircle, Sparkles } from "lucide-react";

interface Props {
  question: Question;
  isAdmin: boolean;
  onRefresh: () => void;
}

export default function QuestionCard({ question, isAdmin, onRefresh }: Props) {
  const [replyText, setReplyText] = useState("");

  const handleReply = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!replyText.trim()) return;
    await postReply(question.id, replyText);
    setReplyText("");
    onRefresh();
  };

  const markAnswered = async () => {
    await updateStatus(question.id, "Answered");
    onRefresh();
  };

  const handleEscalate = async () => {
    await updateStatus(question.id, "Escalated");
    onRefresh();
  };

  return (
    <Card className="w-full mb-4 shadow-sm">
      <CardHeader className="flex flex-row items-center justify-between pb-2 bg-slate-50 rounded-t-lg">
        <div className="flex items-center gap-2">
          <Badge variant={question.status === "Answered" ? "default" : "secondary"}>
            {question.status}
          </Badge>
          <span className="text-xs text-muted-foreground">
            {formatDistanceToNow(
              new Date(question.created_at.endsWith("Z") ? question.created_at : question.created_at + "Z")
            )} ago
          </span>
        </div>
        {isAdmin && question.status !== "Answered" && (
          <div className="flex gap-2">
            <Button size="sm" variant="destructive" onClick={handleEscalate} className="h-7 text-xs">
              Escalate
            </Button>
            <Button size="sm" variant="outline" onClick={markAnswered} className="h-7 text-xs">
              <CheckCircle className="mr-1 h-3 w-3" /> Mark Resolved
            </Button>
          </div>
        )}
      </CardHeader>

      <CardContent className="pt-4">
        {/* The Question */}
        <p className="text-lg font-medium mb-4">{question.content}</p>

        {question.answer && (
          <div className="mb-4 p-3 bg-blue-50 border border-blue-100 rounded-md">
            <div className="flex items-center gap-2 text-blue-600 text-xs font-semibold mb-1">
              <Sparkles className="h-3 w-3" />
              AI Suggestion
            </div>
            <p className="text-sm text-slate-700">
              {question.answer.replace("(AI Suggestion): ", "")}
            </p>
          </div>
        )}

        <Separator className="my-4" />

        {/* The Replies */}
        <div className="space-y-3">
          {(question.replies || []).map((reply) => (
            <div key={reply.id} className="bg-muted/50 p-3 rounded-md text-sm">
              <p>{reply.content}</p>
              <span className="text-[10px] text-muted-foreground block mt-1">
                {formatDistanceToNow(
                  new Date(reply.created_at.endsWith("Z") ? reply.created_at : reply.created_at + "Z")
                )} ago
              </span>
            </div>
          ))}
        </div>
      </CardContent>

      <CardFooter>
        <form onSubmit={handleReply} className="flex w-full gap-2 items-center">
          <Input
            placeholder="Add a response..."
            value={replyText}
            onChange={(e) => setReplyText(e.target.value)}
            className="text-sm h-9"
          />
          <Button type="submit" size="sm" variant="ghost">Reply</Button>
        </form>
      </CardFooter>
    </Card>
  );
}