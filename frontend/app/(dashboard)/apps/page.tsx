"use client";

import { ConnectedApps } from "@/components/apps/ConnectedApps";
import { Puzzle } from "lucide-react";

export default function AppsPage() {
  return (
    <div className="flex h-full flex-col items-center p-8">
      <div className="w-full max-w-5xl mx-auto space-y-12">
        
        {/* Header - Centered */}
        <div className="text-center space-y-3">
          <div className="flex items-center justify-center gap-3 mb-4">
            <Puzzle className="h-10 w-10 text-primary" />
          </div>
          <h1 className="text-4xl font-bold tracking-tight">Connected Apps</h1>
          <p className="text-lg text-muted-foreground">
            Manage your social media connections and integrations
          </p>
        </div>

        {/* Apps Content */}
        <ConnectedApps />
      </div>
    </div>
  );
}

