"use client";

import { PostHistory } from "@/components/history/PostHistory";

export default function HistoryPage() {
  return (
    <div className="flex h-full flex-col p-8">
      <div className="mb-8">
        <h1 className="mb-2 text-3xl font-bold text-foreground">Post History</h1>
        <p className="text-muted-foreground">
          View all your posts across different platforms
        </p>
      </div>

      <div className="flex-1">
        <PostHistory />
      </div>
    </div>
  );
}
