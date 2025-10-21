"use client";

import { History, Twitter } from "lucide-react";

export default function HistoryPage() {
  return (
    <div className="flex h-full flex-col p-8">
      <div className="mb-8">
        <h1 className="mb-2 text-3xl font-bold text-foreground">Tweet History</h1>
        <p className="text-muted-foreground">View all your generated tweets</p>
      </div>

      <div className="flex flex-1 flex-col items-center justify-center">
        <div className="text-center">
          <div className="mb-4 flex justify-center">
            <div className="rounded-full bg-muted p-6">
              <History className="h-12 w-12 text-muted-foreground" />
            </div>
          </div>
          <h2 className="mb-2 text-xl font-semibold text-foreground">No tweets yet</h2>
          <p className="text-muted-foreground">
            Your generated tweets will appear here
          </p>
        </div>
      </div>
    </div>
  );
}

