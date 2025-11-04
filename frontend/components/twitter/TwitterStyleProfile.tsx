"use client";

import { useEffect, useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { api } from "@/lib/api";

interface StyleProfile {
  user_id: string;
  average_length: number;
  min_length: number;
  max_length: number;
  tone: string;
  uses_emojis: boolean;
  emoji_percentage: number;
  common_emojis: string[];
  common_hashtags: string[];
  preferred_topics: string[];
  best_performing_content: {
    best_topics: string[];
    best_length: number;
    best_time: string;
    avg_engagement: number;
    top_performing_tweets?: Array<{
      text: string;
      engagement: number;
      likes: number;
      retweets: number;
    }>;
  };
  last_updated: string;
}

export function TwitterStyleProfile() {
  const [profile, setProfile] = useState<StyleProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [regenerating, setRegenerating] = useState(false);

  const fetchProfile = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await api.get("/api/twitter/style-profile");
      
      if (data.success) {
        setProfile(data.profile);
      } else {
        setError("Failed to load style profile");
      }
    } catch (err: any) {
      console.error("Error fetching style profile:", err);
      if (err.response?.status === 404) {
        setError("No style profile found. Please fetch your tweets first.");
      } else {
        setError(err.response?.data?.detail || "Failed to load style profile");
      }
    } finally {
      setLoading(false);
    }
  };

  const handleRegenerate = async () => {
    try {
      setRegenerating(true);
      setError(null);
      const data = await api.post("/api/twitter/regenerate-style-profile");
      
      if (data.success) {
        setProfile(data.profile);
      }
    } catch (err: any) {
      console.error("Error regenerating profile:", err);
      setError(err.response?.data?.detail || "Failed to regenerate profile");
    } finally {
      setRegenerating(false);
    }
  };

  useEffect(() => {
    fetchProfile();
  }, []);

  if (loading) {
    return (
      <div className="space-y-4">
        <Skeleton className="h-8 w-64" />
        <Skeleton className="h-32 w-full" />
        <Skeleton className="h-32 w-full" />
        <Skeleton className="h-32 w-full" />
      </div>
    );
  }

  if (error) {
    return (
      <Card className="p-6">
        <div className="text-center space-y-4">
          <p className="text-red-500">{error}</p>
          <Button onClick={fetchProfile} variant="outline">
            Try Again
          </Button>
        </div>
      </Card>
    );
  }

  if (!profile) {
    return (
      <Card className="p-6">
        <p className="text-center text-gray-500">No style profile available</p>
      </Card>
    );
  }

  const getToneColor = (tone: string) => {
    const colors: Record<string, string> = {
      enthusiastic: "bg-orange-500/10 text-orange-600 dark:text-orange-400 border-orange-500/20",
      professional: "bg-blue-500/10 text-blue-600 dark:text-blue-400 border-blue-500/20",
      casual_professional: "bg-purple-500/10 text-purple-600 dark:text-purple-400 border-purple-500/20",
      casual: "bg-green-500/10 text-green-600 dark:text-green-400 border-green-500/20",
      curious: "bg-yellow-500/10 text-yellow-600 dark:text-yellow-400 border-yellow-500/20",
      informative: "bg-primary/10 text-primary border-primary/20",
      neutral: "bg-muted text-muted-foreground border-border",
    };
    return colors[tone] || colors.neutral;
  };

  const formatTone = (tone: string) => {
    return tone
      .split("_")
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(" ");
  };

  return (
    <div className="space-y-6">
      {/* Header with Regenerate Button */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-foreground">Style Profile</h2>
          <p className="text-sm text-muted-foreground mt-1">
            Last updated: {new Date(profile.last_updated).toLocaleDateString()}
          </p>
        </div>
        <Button
          onClick={handleRegenerate}
          disabled={regenerating}
          variant="outline"
          size="sm"
        >
          {regenerating ? "Regenerating..." : "Regenerate"}
        </Button>
      </div>

      {/* Top Section - 2 Column Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left: Writing Style & Tweet Length */}
        <div className="space-y-6">
          {/* Writing Style */}
          <Card className="p-6 border-border">
            <h3 className="text-lg font-semibold text-foreground mb-4">Writing Style</h3>
            <div className="space-y-4">
              <div>
                <p className="text-sm text-muted-foreground mb-2">Tone</p>
                <span
                  className={`inline-block px-3 py-1 rounded-full text-sm font-medium border ${getToneColor(
                    profile.tone
                  )}`}
                >
                  {formatTone(profile.tone)}
                </span>
              </div>
              <div>
                <p className="text-sm text-muted-foreground mb-2">Emoji Usage</p>
                <div className="flex items-center gap-2">
                  <span className="text-2xl">
                    {profile.uses_emojis ? "✅" : "❌"}
                  </span>
                  <span className="text-sm text-foreground">
                    {profile.emoji_percentage}% of tweets
                  </span>
                </div>
              </div>
            </div>
          </Card>

          {/* Tweet Length Stats */}
          <Card className="p-6 border-border">
            <h3 className="text-lg font-semibold text-foreground mb-4">Tweet Length</h3>
            <div className="grid grid-cols-3 gap-4">
              <div className="text-center">
                <p className="text-sm text-muted-foreground mb-1">Average</p>
                <p className="text-3xl font-bold text-primary">
                  {profile.average_length}
                </p>
                <p className="text-xs text-muted-foreground">chars</p>
              </div>
              <div className="text-center">
                <p className="text-sm text-muted-foreground mb-1">Min</p>
                <p className="text-3xl font-bold text-primary">
                  {profile.min_length}
                </p>
                <p className="text-xs text-muted-foreground">chars</p>
              </div>
              <div className="text-center">
                <p className="text-sm text-muted-foreground mb-1">Max</p>
                <p className="text-3xl font-bold text-primary">
                  {profile.max_length}
                </p>
                <p className="text-xs text-muted-foreground">chars</p>
              </div>
            </div>
          </Card>
        </div>

        {/* Right: Common Elements */}
        <div className="space-y-6">
          {/* Common Emojis */}
          {profile.common_emojis && profile.common_emojis.length > 0 && (
            <Card className="p-6 border-border">
              <h3 className="text-lg font-semibold text-foreground mb-4">Common Emojis</h3>
              <div className="flex flex-wrap gap-3">
                {profile.common_emojis.map((emoji, index) => (
                  <span key={index} className="text-4xl">
                    {emoji}
                  </span>
                ))}
              </div>
            </Card>
          )}

          {/* Common Hashtags */}
          {profile.common_hashtags && profile.common_hashtags.length > 0 && (
            <Card className="p-6 border-border">
              <h3 className="text-lg font-semibold text-foreground mb-4">Common Hashtags</h3>
              <div className="flex flex-wrap gap-2">
                {profile.common_hashtags.map((hashtag, index) => (
                  <span
                    key={index}
                    className="px-3 py-1 bg-primary/10 text-primary rounded-full text-sm font-medium border border-primary/20"
                  >
                    #{hashtag}
                  </span>
                ))}
              </div>
            </Card>
          )}
        </div>
      </div>

      {/* Preferred Topics - Full Width */}
      {profile.preferred_topics && profile.preferred_topics.length > 0 && (
        <Card className="p-6 border-border">
          <h3 className="text-lg font-semibold text-foreground mb-4">Preferred Topics</h3>
          <div className="flex flex-wrap gap-2">
            {profile.preferred_topics.map((topic, index) => (
              <span
                key={index}
                className="px-3 py-1 bg-secondary text-secondary-foreground rounded-full text-sm font-medium border border-border"
              >
                {topic}
              </span>
            ))}
          </div>
        </Card>
      )}

      {/* Best Performing Content - Full Width */}
      {profile.best_performing_content && (
        <Card className="p-6 border-border">
          <h3 className="text-lg font-semibold text-foreground mb-4">
            Performance Insights
          </h3>
          <div className="space-y-6">
            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="text-center p-4 bg-muted/30 rounded-lg">
                <p className="text-sm text-muted-foreground mb-2">Optimal Length</p>
                <p className="text-3xl font-bold text-primary">
                  {profile.best_performing_content.best_length}
                </p>
                <p className="text-xs text-muted-foreground mt-1">characters</p>
              </div>
              <div className="text-center p-4 bg-muted/30 rounded-lg">
                <p className="text-sm text-muted-foreground mb-2">Best Time</p>
                <p className="text-3xl font-bold text-primary">
                  {profile.best_performing_content.best_time}
                </p>
                <p className="text-xs text-muted-foreground mt-1">to post</p>
              </div>
              <div className="text-center p-4 bg-muted/30 rounded-lg">
                <p className="text-sm text-muted-foreground mb-2">Avg Engagement</p>
                <p className="text-3xl font-bold text-primary">
                  {profile.best_performing_content.avg_engagement}
                </p>
                <p className="text-xs text-muted-foreground mt-1">interactions</p>
              </div>
            </div>

            {/* Top Performing Topics */}
            {profile.best_performing_content.best_topics &&
              profile.best_performing_content.best_topics.length > 0 && (
                <div>
                  <p className="text-sm font-medium text-foreground mb-3">
                    🏆 Top Performing Topics
                  </p>
                  <div className="flex flex-wrap gap-2">
                    {profile.best_performing_content.best_topics.map(
                      (topic, index) => (
                        <span
                          key={index}
                          className="px-3 py-1 bg-primary/10 text-primary rounded-full text-sm font-medium border border-primary/20"
                        >
                          #{topic}
                        </span>
                      )
                    )}
                  </div>
                </div>
              )}

            {/* Top Performing Tweets */}
            {profile.best_performing_content.top_performing_tweets &&
              profile.best_performing_content.top_performing_tweets.length > 0 && (
                <div>
                  <p className="text-sm font-medium text-foreground mb-3">
                    ⭐ Your Best Tweets
                  </p>
                  <div className="space-y-3">
                    {profile.best_performing_content.top_performing_tweets.map(
                      (tweet, index) => (
                        <div
                          key={index}
                          className="p-4 bg-muted/50 rounded-lg border border-border hover:border-primary/50 transition-colors"
                        >
                          <p className="text-sm text-foreground mb-3 leading-relaxed">{tweet.text}</p>
                          <div className="flex items-center gap-4 text-xs text-muted-foreground">
                            <span className="flex items-center gap-1">
                              <span>❤️</span>
                              <span>{tweet.likes}</span>
                            </span>
                            <span className="flex items-center gap-1">
                              <span>🔄</span>
                              <span>{tweet.retweets}</span>
                            </span>
                            <span className="ml-auto font-semibold text-primary">
                              {tweet.engagement} total
                            </span>
                          </div>
                        </div>
                      )
                    )}
                  </div>
                </div>
              )}
          </div>
        </Card>
      )}
    </div>
  );
}

