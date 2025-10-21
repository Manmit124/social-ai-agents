"use client";

import { useState } from "react";
import { useAuth } from "@/hooks/auth/useAuth";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Sparkles, Send } from "lucide-react";

export default function DashboardPage() {
  const { user } = useAuth();
  const [prompt, setPrompt] = useState("");
  const [isGenerating, setIsGenerating] = useState(false);

  const handleGenerate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!prompt.trim()) return;
    
    setIsGenerating(true);
    // TODO: Implement tweet generation
    setTimeout(() => {
      setIsGenerating(false);
    }, 2000);
  };

  return (
    <div className="flex h-full flex-col items-center justify-center px-4">
      <div className="w-full max-w-4xl space-y-8">
        {/* Header */}
        <div className="text-center">
          <h1 className="mb-2 text-5xl font-bold text-foreground">
            Create Amazing Tweets with AI
          </h1>
          <p className="text-muted-foreground">
            Generate engaging content powered by artificial intelligence
          </p>
        </div>

        {/* Input Area */}
        <div className="relative">
          <div className="rounded-2xl border bg-card p-6 shadow-2xl">
            <form onSubmit={handleGenerate} className="space-y-4">
              <div className="relative">
                <Textarea
                  value={prompt}
                  onChange={(e) => setPrompt(e.target.value)}
                  placeholder="What's on your mind? Describe your tweet idea..."
                  className="min-h-[120px] resize-none border-0 bg-transparent text-base focus-visible:ring-0 focus-visible:ring-offset-0"
                  disabled={isGenerating}
                />
              </div>

              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  <button
                    type="button"
                    className="flex items-center space-x-2 rounded-full bg-secondary px-4 py-2 text-sm text-secondary-foreground transition-colors hover:bg-secondary/80"
                  >
                    <Sparkles className="h-4 w-4" />
                    <span>Creative</span>
                  </button>
                </div>

                <Button
                  type="submit"
                  disabled={!prompt.trim() || isGenerating}
                  className="rounded-full px-6"
                >
                  {isGenerating ? (
                    <>
                      <Sparkles className="mr-2 h-4 w-4 animate-spin" />
                      Generating...
                    </>
                  ) : (
                    <>
                      <Send className="mr-2 h-4 w-4" />
                      Generate Tweet
                    </>
                  )}
                </Button>
              </div>
            </form>
          </div>

          {/* Upgrade Badge */}
          <div className="mt-4 flex justify-center">
            <button className="flex items-center space-x-2 rounded-full border bg-secondary px-4 py-2 text-sm text-secondary-foreground transition-all hover:bg-secondary/80">
              <Sparkles className="h-4 w-4" />
              <span>Upgrade to PRO for unlimited tweets</span>
            </button>
          </div>
        </div>

        {/* Footer Info */}
        <div className="text-center">
          <p className="text-xs text-muted-foreground">
            Logged in as {user?.email}
          </p>
        </div>
      </div>
    </div>
  );
}
