/**
 * GitHub Activity Component
 * 
 * Displays recent GitHub commits
 */

'use client';

import React, { useState } from 'react';
import { useGitHubActivity, useFormatDate } from '@/hooks/api/useGitHub';
import { Card } from '@/components/ui/card';

export function GitHubActivity() {
  const [limit, setLimit] = useState(10);
  const [days, setDays] = useState<number | undefined>(30);
  const { data: activity, isLoading, error } = useGitHubActivity(limit, days);

  if (isLoading) {
    return (
      <Card className="p-6 border-border">
        <div className="animate-pulse space-y-4">
          {[...Array(3)].map((_, i) => (
            <div key={i} className="space-y-2">
              <div className="h-4 bg-muted rounded w-3/4"></div>
              <div className="h-3 bg-muted rounded w-1/2"></div>
            </div>
          ))}
        </div>
      </Card>
    );
  }

  if (error) {
    const errorMessage = error instanceof Error ? error.message : 'Failed to load GitHub activity';
    const isNotConnected = errorMessage.includes('Not authenticated') || errorMessage.includes('GitHub not connected');
    
    return (
      <Card className="p-6 border-border">
        <div className="text-center py-8 space-y-2">
          <p className="text-muted-foreground">
            {isNotConnected ? 'Connect your GitHub account to view activity' : 'Failed to load GitHub activity'}
          </p>
        </div>
      </Card>
    );
  }

  if (!activity || activity.commits.length === 0) {
    return (
      <Card className="p-6 border-border">
        <div className="text-center py-8">
          <p className="text-muted-foreground mb-2">No GitHub activity found</p>
          <p className="text-sm text-muted-foreground">
            Connect your GitHub account and fetch data to see your commits
          </p>
        </div>
      </Card>
    );
  }

  return (
    <Card className="p-6 border-border">
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between flex-wrap gap-4">
          <h3 className="text-lg font-semibold text-foreground">Recent Commits</h3>
          <div className="flex gap-2">
            <select
              value={days || 'all'}
              onChange={(e) => setDays(e.target.value === 'all' ? undefined : Number(e.target.value))}
              className="text-sm border border-border bg-background text-foreground rounded-md px-3 py-1.5 focus:outline-none focus:ring-2 focus:ring-primary"
            >
              <option value="7">Last 7 days</option>
              <option value="30">Last 30 days</option>
              <option value="90">Last 90 days</option>
              <option value="all">All time</option>
            </select>
            <select
              value={limit}
              onChange={(e) => setLimit(Number(e.target.value))}
              className="text-sm border border-border bg-background text-foreground rounded-md px-3 py-1.5 focus:outline-none focus:ring-2 focus:ring-primary"
            >
              <option value="10">10 commits</option>
              <option value="25">25 commits</option>
              <option value="50">50 commits</option>
              <option value="100">100 commits</option>
            </select>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 gap-4 p-4 bg-muted/50 rounded-lg border border-border">
          <div className="space-y-1">
            <p className="text-sm text-muted-foreground">Showing</p>
            <p className="text-lg font-semibold text-foreground">{activity.commits.length} commits</p>
          </div>
          <div className="space-y-1">
            <p className="text-sm text-muted-foreground">Total</p>
            <p className="text-lg font-semibold text-foreground">{activity.total_commits} commits</p>
          </div>
        </div>

        {/* Commits List */}
        <div className="space-y-3 max-h-[600px] overflow-y-auto pr-2">
          {activity.commits.map((commit) => (
            <CommitCard key={commit.id} commit={commit} />
          ))}
        </div>
      </div>
    </Card>
  );
}

interface CommitCardProps {
  commit: {
    id: string;
    repository_name: string;
    commit_hash: string;
    commit_message: string;
    commit_date: string;
    language: string | null;
  };
}

function CommitCard({ commit }: CommitCardProps) {
  const formatDate = useFormatDate(commit.commit_date);

  return (
    <div className="p-4 border border-border rounded-lg hover:bg-muted/30 transition-all duration-200 hover:border-primary/50">
      <div className="flex items-start justify-between gap-4">
        <div className="flex-1 min-w-0">
          {/* Commit Message */}
          <p className="font-medium text-foreground mb-2 line-clamp-2">
            {commit.commit_message.split('\n')[0]}
          </p>
          
          {/* Repository and Language */}
          <div className="flex items-center gap-2 flex-wrap">
            <span className="inline-flex items-center px-2 py-1 bg-primary/10 text-primary rounded text-xs font-medium">
              📁 {commit.repository_name}
            </span>
            {commit.language && (
              <span className="inline-flex items-center px-2 py-1 bg-muted text-muted-foreground rounded text-xs font-medium">
                {commit.language}
              </span>
            )}
          </div>
        </div>

        {/* Date and Hash */}
        <div className="text-right flex-shrink-0">
          <p className="text-xs text-muted-foreground mb-1">{formatDate}</p>
          <code className="text-xs text-muted-foreground font-mono bg-muted px-1.5 py-0.5 rounded">
            {commit.commit_hash.substring(0, 7)}
          </code>
        </div>
      </div>
    </div>
  );
}

export default GitHubActivity;

