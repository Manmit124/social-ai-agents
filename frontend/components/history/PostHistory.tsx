"use client";

import { useState } from "react";
import { History, Linkedin, MessageCircle, ExternalLink, RefreshCw } from "lucide-react";
import { Button } from "@/components/ui/button";
import { usePosts } from "@/hooks/api/usePosts";
import { formatDistanceToNow } from "date-fns";
import { XIcon } from "@/components/icons/XIcon";

type PlatformFilter = "all" | "twitter" | "linkedin" | "reddit";

const platformIcons = {
  twitter: XIcon,
  linkedin: Linkedin,
  reddit: MessageCircle,
};

const platformColors = {
  twitter: "text-foreground",
  linkedin: "text-blue-700",
  reddit: "text-orange-500",
};

export function PostHistory() {
  const [filter, setFilter] = useState<PlatformFilter>("all");
  const { posts, isLoading, error, refetch } = usePosts(filter === "all" ? undefined : filter);

  const filters: { value: PlatformFilter; label: string }[] = [
    { value: "all", label: "All" },
    { value: "twitter", label: "X" },
    { value: "linkedin", label: "LinkedIn" },
    { value: "reddit", label: "Reddit" },
  ];

  return (
    <div className="space-y-6">
      {/* Filter Bar */}
      <div className="flex items-center justify-between">
        {/* Filter Pills */}
        <div className="inline-flex items-center gap-2 rounded-full bg-muted/50 p-1.5 backdrop-blur-sm border">
          {filters.map((f) => (
            <button
              key={f.value}
              onClick={() => setFilter(f.value)}
              className={`rounded-full px-5 py-2 text-sm font-medium transition-all ${
                filter === f.value
                  ? "bg-primary text-primary-foreground shadow-lg scale-105"
                  : "text-muted-foreground hover:bg-background/80"
              }`}
            >
              {f.label}
            </button>
          ))}
        </div>

        {/* Refresh Button */}
        <Button
          variant="outline"
          size="sm"
          onClick={() => refetch()}
          disabled={isLoading}
          className="rounded-xl"
        >
          <RefreshCw className={`h-4 w-4 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
          Refresh
        </Button>
      </div>

      {/* Loading State */}
      {isLoading && (
        <div className="flex items-center justify-center py-16">
          <div className="h-12 w-12 animate-spin rounded-full border-4 border-primary border-t-transparent" />
        </div>
      )}

      {/* Error State */}
      {error && (
        <div className="rounded-2xl bg-destructive/10 border border-destructive/20 p-6 text-center">
          <p className="text-sm text-destructive font-medium">
            Failed to load posts. Please try again.
          </p>
        </div>
      )}

      {/* Empty State */}
      {!isLoading && !error && posts.length === 0 && (
        <div className="flex flex-col items-center justify-center py-16 text-center rounded-2xl border-2 border-dashed bg-muted/20">
          <History className="mb-4 h-16 w-16 text-muted-foreground" />
          <h3 className="mb-2 text-xl font-semibold">
            No posts yet
          </h3>
          <p className="text-sm text-muted-foreground">
            Generate and post your first content to see it here
          </p>
        </div>
      )}

      {/* Posts List */}
      {!isLoading && !error && posts.length > 0 && (
        <div className="space-y-4">
          {posts.map((post) => {
            const Icon = platformIcons[post.platform as keyof typeof platformIcons];
            const colorClass = platformColors[post.platform as keyof typeof platformColors];
            const timeAgo = post.created_at
              ? formatDistanceToNow(new Date(post.created_at), { addSuffix: true })
              : "Unknown time";

            return (
              <div
                key={post.id}
                className="rounded-2xl border-2 bg-card/80 backdrop-blur-sm p-6 shadow-lg hover:shadow-xl transition-all"
              >
                {/* Header */}
                <div className="mb-4 flex items-start justify-between">
                  <div className="flex items-center gap-3">
                    {Icon && <Icon className={`h-5 w-5 ${colorClass}`} />}
                    <div>
                      <span className="text-sm font-semibold capitalize">
                        {post.platform === "twitter" ? "X" : post.platform}
                      </span>
                      <span className="text-xs text-muted-foreground ml-2">
                        {timeAgo}
                      </span>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    {/* Status Badge */}
                    <span
                      className={`inline-flex items-center rounded-full px-3 py-1 text-xs font-medium ${
                        post.status === "posted"
                          ? "bg-green-500/10 text-green-700 dark:text-green-400 border border-green-500/20"
                          : "bg-yellow-500/10 text-yellow-700 dark:text-yellow-400 border border-yellow-500/20"
                      }`}
                    >
                      {post.status}
                    </span>
                    {post.platform_post_url && (
                      <a
                        href={post.platform_post_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-primary hover:text-primary/80 transition-colors"
                      >
                        <ExternalLink className="h-5 w-5" />
                      </a>
                    )}
                  </div>
                </div>

                {/* Prompt */}
                {post.user_prompt && (
                  <div className="mb-3 rounded-xl bg-muted/50 p-3">
                    <p className="text-sm text-muted-foreground italic">
                      "{post.user_prompt}"
                    </p>
                  </div>
                )}

                {/* Content */}
                <p className="text-base leading-relaxed mb-3">
                  {post.generated_content}
                </p>

                {/* Hashtags */}
                {post.hashtags && post.hashtags.length > 0 && (
                  <div className="flex flex-wrap gap-2">
                    {post.hashtags.map((tag, index) => (
                      <span
                        key={index}
                        className="rounded-full bg-primary/10 px-3 py-1 text-xs font-medium text-primary"
                      >
                        {tag}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}

