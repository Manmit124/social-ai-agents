"use client";

import { useAuth } from "@/hooks/auth/useAuth";
import { ContentGenerator } from "@/components/generator/ContentGenerator";
import { PostHistory } from "@/components/history/PostHistory";

export default function DashboardPage() {
  const { user } = useAuth();

  return (
    <div className="flex h-full flex-col p-8">
      <div className="mb-8">
        <h1 className="mb-2 text-3xl font-bold text-foreground">
          Welcome back{user?.email ? `, ${user.email.split('@')[0]}` : ''}!
        </h1>
        <p className="text-muted-foreground">
          Generate engaging content for your social media platforms with AI
        </p>
      </div>

      <div className="grid flex-1 gap-6 lg:grid-cols-2">
        {/* Content Generator */}
        <div className="flex flex-col">
          <ContentGenerator />
        </div>

        {/* Post History */}
        <div className="flex flex-col">
          <PostHistory />
        </div>
      </div>
    </div>
  );
}
