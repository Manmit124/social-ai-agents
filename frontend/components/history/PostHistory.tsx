"use client";

import { useState } from "react";
import { History, Twitter, Linkedin, MessageCircle, ExternalLink, Filter } from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { usePosts } from "@/hooks/api/usePosts";
import { formatDistanceToNow } from "date-fns";

type PlatformFilter = "all" | "twitter" | "linkedin" | "reddit";

const platformIcons = {
  twitter: Twitter,
  linkedin: Linkedin,
  reddit: MessageCircle,
};

const platformColors = {
  twitter: "text-blue-500",
  linkedin: "text-blue-700",
  reddit: "text-orange-500",
};

export function PostHistory() {
  const [filter, setFilter] = useState<PlatformFilter>("all");
  const { posts, isLoading, error, refetch } = usePosts(filter === "all" ? undefined : filter);

  const filters: { value: PlatformFilter; label: string }[] = [
    { value: "all", label: "All" },
    { value: "twitter", label: "Twitter" },
    { value: "linkedin", label: "LinkedIn" },
    { value: "reddit", label: "Reddit" },
  ];

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="flex items-center gap-2">
              <History className="h-5 w-5 text-primary" />
              Post History
            </CardTitle>
            <CardDescription>
              Your recent posts across all platforms
            </CardDescription>
          </div>
          <Button
            variant="outline"
            size="sm"
            onClick={() => refetch()}
            disabled={isLoading}
          >
            Refresh
          </Button>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Filter Tabs */}
        <div className="flex gap-2 border-b pb-2">
          {filters.map((f) => (
            <button
              key={f.value}
              onClick={() => setFilter(f.value)}
              className={`rounded-lg px-3 py-1.5 text-sm font-medium transition-colors ${
                filter === f.value
                  ? "bg-primary text-primary-foreground"
                  : "text-muted-foreground hover:bg-muted hover:text-foreground"
              }`}
            >
              {f.label}
            </button>
          ))}
        </div>

        {/* Loading State */}
        {isLoading && (
          <div className="flex items-center justify-center py-8">
            <div className="h-8 w-8 animate-spin rounded-full border-4 border-primary border-t-transparent" />
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="rounded-lg bg-destructive/10 p-4 text-center text-sm text-destructive">
            Failed to load posts. Please try again.
          </div>
        )}

        {/* Empty State */}
        {!isLoading && !error && posts.length === 0 && (
          <div className="flex flex-col items-center justify-center py-12 text-center">
            <History className="mb-4 h-12 w-12 text-muted-foreground" />
            <h3 className="mb-2 text-lg font-semibold text-foreground">
              No posts yet
            </h3>
            <p className="text-sm text-muted-foreground">
              Generate and post your first content to see it here
            </p>
          </div>
        )}

        {/* Posts List */}
        {!isLoading && !error && posts.length > 0 && (
          <div className="space-y-3">
            {posts.map((post) => {
              const Icon = platformIcons[post.platform as keyof typeof platformIcons];
              const colorClass = platformColors[post.platform as keyof typeof platformColors];
              const timeAgo = post.created_at
                ? formatDistanceToNow(new Date(post.created_at), { addSuffix: true })
                : "Unknown time";

              return (
                <div
                  key={post.id}
                  className="rounded-lg border bg-card p-4 transition-colors hover:bg-muted/50"
                >
                  {/* Header */}
                  <div className="mb-2 flex items-start justify-between">
                    <div className="flex items-center gap-2">
                      {Icon && <Icon className={`h-4 w-4 ${colorClass}`} />}
                      <span className="text-sm font-medium capitalize text-foreground">
                        {post.platform}
                      </span>
                      <span className="text-xs text-muted-foreground">•</span>
                      <span className="text-xs text-muted-foreground">
                        {timeAgo}
                      </span>
                    </div>
                    {post.platform_post_url && (
                      <a
                        href={post.platform_post_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-primary hover:underline"
                      >
                        <ExternalLink className="h-4 w-4" />
                      </a>
                    )}
                  </div>

                  {/* Prompt */}
                  {post.user_prompt && (
                    <p className="mb-2 text-sm text-muted-foreground italic">
                      "{post.user_prompt}"
                    </p>
                  )}

                  {/* Content */}
                  <p className="text-sm text-foreground line-clamp-3">
                    {post.generated_content}
                  </p>

                  {/* Hashtags */}
                  {post.hashtags && post.hashtags.length > 0 && (
                    <div className="mt-2 flex flex-wrap gap-1">
                      {post.hashtags.map((tag, index) => (
                        <span
                          key={index}
                          className="rounded-full bg-primary/10 px-2 py-0.5 text-xs text-primary"
                        >
                          {tag}
                        </span>
                      ))}
                    </div>
                  )}

                  {/* Status */}
                  <div className="mt-2 flex items-center gap-2">
                    <span
                      className={`inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium ${
                        post.status === "posted"
                          ? "bg-green-500/10 text-green-700 dark:text-green-400"
                          : "bg-yellow-500/10 text-yellow-700 dark:text-yellow-400"
                      }`}
                    >
                      {post.status}
                    </span>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </CardContent>
    </Card>
  );
}

