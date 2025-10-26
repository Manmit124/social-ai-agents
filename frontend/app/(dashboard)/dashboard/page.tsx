"use client";

import { useAuth } from "@/hooks/auth/useAuth";
import { ContentGenerator } from "@/components/generator/ContentGenerator";

export default function DashboardPage() {
  const { user } = useAuth();

  return (
    <div className="flex h-full flex-col items-center justify-center p-8">
      {/* Centered Content Container */}
      <div className="w-full max-w-3xl mx-auto space-y-12">
        
        {/* Hero Section - Minimal & Centered */}
        <div className="text-center space-y-3">
          <h1 className="text-5xl font-bold tracking-tight">
            Just create with <span className="text-primary">AI</span>
          </h1>
          <p className="text-lg text-muted-foreground">
            Generate engaging content for your social media platforms
          </p>
        </div>

        {/* Content Generator */}
        <ContentGenerator />
      </div>
    </div>
  );
}
