"use client";

import { PostHistory } from "@/components/history/PostHistory";
import { History } from "lucide-react";

export default function HistoryPage() {
  return (
    <div className="flex h-full flex-col items-center p-8">
      <div className="w-full max-w-4xl mx-auto space-y-12">
        
        {/* Header - Centered */}
        <div className="text-center space-y-3">
          <div className="flex items-center justify-center gap-3 mb-4">
            <History className="h-10 w-10 text-primary" />
          </div>
          <h1 className="text-4xl font-bold tracking-tight">Post History</h1>
          <p className="text-lg text-muted-foreground">
            View all your posts across different platforms
          </p>
        </div>

        {/* History Content */}
        <div className="flex-1">
          <PostHistory />
        </div>
      </div>
    </div>
  );
}
