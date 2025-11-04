/**
 * GitHub Insights Component
 * 
 * Displays AI-generated insights with "Use for Tweet" button
 */

'use client';

import React from 'react';
import { useRouter } from 'next/navigation';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { useGitHubContext, useAnalyzeGitHub } from '@/hooks/api/useGitHub';
import { Sparkles, RefreshCw, ArrowRight, Lightbulb, Target } from 'lucide-react';

export function GitHubInsights() {
  const router = useRouter();
  const { data: context, isLoading, error } = useGitHubContext();
  const analyzeGitHub = useAnalyzeGitHub();

  const handleRefreshInsights = async () => {
    try {
      await analyzeGitHub.mutateAsync();
    } catch (error) {
      console.error('Failed to refresh insights:', error);
    }
  };

  const handleUseForTweet = () => {
    if (context?.ai_insights?.summary_for_social) {
      // Navigate to dashboard with pre-filled prompt
      const prompt = context.ai_insights.summary_for_social;
      router.push(`/dashboard?prompt=${encodeURIComponent(prompt)}`);
    }
  };

  if (isLoading) {
    return (
      <Card className="p-6 border-border">
        <div className="animate-pulse space-y-4">
          <div className="h-4 bg-muted rounded w-1/3"></div>
          <div className="h-4 bg-muted rounded w-full"></div>
          <div className="h-4 bg-muted rounded w-2/3"></div>
        </div>
      </Card>
    );
  }

  if (error || !context) {
    return null;
  }

  // Show "Generate Insights" button if no AI insights yet
  if (!context.ai_insights) {
    return (
      <Card className="p-6 border-border text-center space-y-4">
        <div className="flex justify-center">
          <div className="bg-primary/10 p-4 rounded-full">
            <Sparkles className="w-8 h-8 text-primary" />
          </div>
        </div>
        <div className="space-y-2">
          <h3 className="text-lg font-semibold text-foreground">AI Insights</h3>
          <p className="text-sm text-muted-foreground max-w-md mx-auto">
            Get AI-powered insights about your coding activity to create engaging social media content
          </p>
        </div>
        <Button
          onClick={handleRefreshInsights}
          disabled={analyzeGitHub.isPending}
          className="gap-2"
        >
          {analyzeGitHub.isPending ? (
            <>
              <RefreshCw className="w-4 h-4 animate-spin" />
              Generating...
            </>
          ) : (
            <>
              <Sparkles className="w-4 h-4" />
              Generate AI Insights
            </>
          )}
        </Button>
        {analyzeGitHub.isError && (
          <p className="text-sm text-destructive">
            Failed to generate insights. Please try again.
          </p>
        )}
      </Card>
    );
  }

  const insights = context.ai_insights;

  return (
    <Card className="p-6 border-border space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Sparkles className="w-5 h-5 text-primary" />
          <h3 className="text-lg font-semibold text-foreground">AI Insights</h3>
        </div>
        <Button
          onClick={handleRefreshInsights}
          disabled={analyzeGitHub.isPending}
          variant="outline"
          size="sm"
          className="gap-2"
        >
          {analyzeGitHub.isPending ? (
            <>
              <RefreshCw className="w-4 h-4 animate-spin" />
              Refreshing...
            </>
          ) : (
            <>
              <RefreshCw className="w-4 h-4" />
              Refresh
            </>
          )}
        </Button>
      </div>

      {/* Focus Areas */}
      {insights.focus_areas && insights.focus_areas.length > 0 && (
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <Target className="w-4 h-4 text-muted-foreground" />
            <p className="text-sm font-medium text-muted-foreground">Focus Areas</p>
          </div>
          <div className="flex flex-wrap gap-2">
            {insights.focus_areas.map((area, index) => (
              <span
                key={index}
                className="px-3 py-1.5 bg-primary/10 text-primary rounded-md text-sm font-medium"
              >
                {area}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Key Achievements */}
      {insights.key_achievements && insights.key_achievements.length > 0 && (
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <Lightbulb className="w-4 h-4 text-muted-foreground" />
            <p className="text-sm font-medium text-muted-foreground">Key Achievements</p>
          </div>
          <ul className="space-y-2">
            {insights.key_achievements.map((achievement, index) => (
              <li key={index} className="flex items-start gap-2 text-sm text-foreground">
                <span className="text-primary mt-0.5">•</span>
                <span>{achievement}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Summary for Social Media */}
      {insights.summary_for_social && (
        <div className="pt-4 border-t border-border space-y-4">
          <div>
            <p className="text-sm font-medium text-muted-foreground mb-2">
              Ready for Social Media
            </p>
            <div className="p-4 bg-muted/50 rounded-lg border border-border">
              <p className="text-foreground leading-relaxed">
                {insights.summary_for_social}
              </p>
            </div>
          </div>

          {/* Use for Tweet Button */}
          <Button
            onClick={handleUseForTweet}
            className="w-full gap-2"
            size="lg"
          >
            <Sparkles className="w-4 h-4" />
            Use for Tweet
            <ArrowRight className="w-4 h-4" />
          </Button>
        </div>
      )}

      {/* Generated timestamp */}
      {insights.generated_at && (
        <p className="text-xs text-muted-foreground text-center">
          Generated {new Date(insights.generated_at).toLocaleString()}
        </p>
      )}

      {/* Error message if refresh failed */}
      {analyzeGitHub.isError && (
        <div className="p-3 bg-destructive/10 border border-destructive/20 rounded-lg">
          <p className="text-sm text-destructive">
            Failed to refresh insights. Please try again.
          </p>
        </div>
      )}
    </Card>
  );
}

export default GitHubInsights;

