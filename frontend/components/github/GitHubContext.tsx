/**
 * GitHub Context Component
 * 
 * Displays user's GitHub context (projects, tech stack, activity stats)
 */

'use client';

import React from 'react';
import { Card } from '@/components/ui/card';
import { useGitHubContext } from '@/hooks/api/useGitHub';
import { Code2, Folder, TrendingUp } from 'lucide-react';

export function GitHubContext() {
  const { data: context, isLoading, error } = useGitHubContext();

  if (isLoading) {
    return (
      <div className="space-y-6">
        <Card className="p-6 border-border">
          <div className="animate-pulse space-y-4">
            <div className="h-4 bg-muted rounded w-1/3"></div>
            <div className="h-4 bg-muted rounded w-1/2"></div>
          </div>
        </Card>
      </div>
    );
  }

  if (error || !context) {
    return null; // Don't show if no context available
  }

  return (
    <div className="space-y-6">
      {/* Coding Context Card */}
      <Card className="p-6 border-border">
        <div className="space-y-6">
          {/* Header */}
          <div className="flex items-center gap-2">
            <Code2 className="w-5 h-5 text-primary" />
            <h3 className="text-lg font-semibold text-foreground">Your Coding Context</h3>
          </div>

          {/* Current Projects */}
          {context.current_projects && context.current_projects.length > 0 && (
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <Folder className="w-4 h-4 text-muted-foreground" />
                <p className="text-sm font-medium text-muted-foreground">Current Projects</p>
              </div>
              <div className="flex flex-wrap gap-2">
                {context.current_projects.map((project, index) => (
                  <span
                    key={index}
                    className="px-3 py-1.5 bg-primary/10 text-primary rounded-md text-sm font-medium"
                  >
                    {project}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Tech Stack */}
          {context.tech_stack && context.tech_stack.length > 0 && (
            <div className="space-y-2">
              <div className="flex items-center gap-2">
                <Code2 className="w-4 h-4 text-muted-foreground" />
                <p className="text-sm font-medium text-muted-foreground">Tech Stack</p>
              </div>
              <div className="flex flex-wrap gap-2">
                {context.tech_stack.slice(0, 8).map((tech, index) => (
                  <span
                    key={index}
                    className="px-3 py-1.5 bg-muted text-muted-foreground rounded-md text-sm font-medium"
                  >
                    {tech}
                  </span>
                ))}
                {context.tech_stack.length > 8 && (
                  <span className="px-3 py-1.5 bg-muted text-muted-foreground rounded-md text-sm font-medium">
                    +{context.tech_stack.length - 8} more
                  </span>
                )}
              </div>
            </div>
          )}

          {/* Recent Activity Summary */}
          {context.recent_activity_summary && (
            <div className="pt-4 border-t border-border">
              <p className="text-sm text-muted-foreground">
                <span className="font-medium text-foreground">Recent Focus:</span>{' '}
                {context.recent_activity_summary}
              </p>
            </div>
          )}
        </div>
      </Card>

      {/* Activity Stats Card */}
      <Card className="p-6 border-border">
        <div className="space-y-6">
          {/* Header */}
          <div className="flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-primary" />
            <h3 className="text-lg font-semibold text-foreground">Activity Stats</h3>
          </div>

          {/* Stats Grid */}
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-1">
              <p className="text-sm text-muted-foreground">Last 7 days</p>
              <p className="text-2xl font-bold text-foreground">
                {context.activity_stats?.commits_last_7_days || 0}
              </p>
              <p className="text-xs text-muted-foreground">commits</p>
            </div>

            <div className="space-y-1">
              <p className="text-sm text-muted-foreground">Last 30 days</p>
              <p className="text-2xl font-bold text-foreground">
                {context.activity_stats?.commits_last_30_days || 0}
              </p>
              <p className="text-xs text-muted-foreground">commits</p>
            </div>

            <div className="space-y-1">
              <p className="text-sm text-muted-foreground">Daily Average</p>
              <p className="text-2xl font-bold text-foreground">
                {context.activity_stats?.average_commits_per_day || 0}
              </p>
              <p className="text-xs text-muted-foreground">commits/day</p>
            </div>

            <div className="space-y-1">
              <p className="text-sm text-muted-foreground">Most Active</p>
              <p className="text-lg font-bold text-foreground">
                {context.activity_stats?.most_active_day || 'N/A'}
              </p>
              <p className="text-xs text-muted-foreground">
                {context.activity_stats?.most_active_time || ''}
              </p>
            </div>
          </div>
        </div>
      </Card>
    </div>
  );
}

export default GitHubContext;

