/**
 * GitHub Data Status Component
 * 
 * Displays GitHub data freshness status with refresh recommendations
 */

'use client';

import React from 'react';
import { useGitHubStatus, useFetchGitHubData, useTimeAgo } from '@/hooks/api/useGitHub';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';

export function GitHubDataStatus() {
  const { data: status, isLoading, error } = useGitHubStatus();
  const fetchData = useFetchGitHubData();
  const timeAgo = useTimeAgo(status?.last_fetch_time || null);

  const handleRefresh = async () => {
    try {
      await fetchData.mutateAsync({ days: 30 });
    } catch (error) {
      console.error('Failed to fetch GitHub data:', error);
    }
  };

  if (isLoading) {
    return (
      <Card className="p-6 border-border">
        <div className="animate-pulse space-y-4">
          <div className="h-4 bg-muted rounded w-3/4"></div>
          <div className="h-4 bg-muted rounded w-1/2"></div>
        </div>
      </Card>
    );
  }

  if (error) {
    const errorMessage = error instanceof Error ? error.message : 'Failed to load GitHub status';
    const isNotConnected = errorMessage.includes('Not authenticated') || errorMessage.includes('GitHub not connected');
    
    return (
      <Card className="p-6 border-border">
        <div className="text-center py-4 space-y-2">
          <p className="text-muted-foreground text-sm">
            {isNotConnected ? 'Connect your GitHub account to view status' : 'Failed to load GitHub status'}
          </p>
        </div>
      </Card>
    );
  }

  if (!status) {
    return null;
  }

  // Determine status badge color and text
  const getStatusBadge = () => {
    if (!status.has_data) {
      return {
        color: 'bg-muted text-muted-foreground',
        text: 'No Data',
        icon: '⚪'
      };
    }
    if (status.needs_refresh) {
      return {
        color: 'bg-primary/10 text-primary',
        text: 'Needs Refresh',
        icon: '⚠️'
      };
    }
    return {
      color: 'bg-primary/10 text-primary',
      text: 'Fresh',
      icon: '✅'
    };
  };

  const statusBadge = getStatusBadge();

  return (
    <Card className="p-6 border-border">
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-foreground">Data Sync</h3>
          <span className={`px-3 py-1 rounded-full text-sm font-medium ${statusBadge.color}`}>
            {statusBadge.icon} {statusBadge.text}
          </span>
        </div>

        {/* Sync Info */}
        {status.has_data && (
          <div className="space-y-3">
            <div className="flex items-center justify-between text-sm">
              <span className="text-muted-foreground">Last synced:</span>
              <span className="font-medium text-foreground">{timeAgo}</span>
            </div>
            {status.hours_since_fetch !== null && (
              <div className="flex items-center justify-between text-sm">
                <span className="text-muted-foreground">Hours ago:</span>
                <span className="font-medium text-foreground">{status.hours_since_fetch.toFixed(1)}h</span>
              </div>
            )}
            <div className="flex items-center justify-between text-sm">
              <span className="text-muted-foreground">Total stored:</span>
              <span className="font-medium text-foreground">{status.total_commits} commits</span>
            </div>
          </div>
        )}

        {/* Refresh Reason */}
        {status.refresh_reason && (
          <div className="p-3 bg-muted/50 rounded-lg border border-border">
            <p className="text-sm text-muted-foreground">{status.refresh_reason}</p>
          </div>
        )}

        {/* Action Button */}
        <Button
          onClick={handleRefresh}
          disabled={fetchData.isPending}
          className="w-full"
          variant={status.needs_refresh ? 'default' : 'outline'}
        >
          {fetchData.isPending ? (
            <>
              <span className="animate-spin mr-2">⏳</span>
              Syncing...
            </>
          ) : status.has_data ? (
            <>
              <span className="mr-2">🔄</span>
              Sync Data
            </>
          ) : (
            <>
              <span className="mr-2">📦</span>
              Fetch GitHub Data
            </>
          )}
        </Button>

        {/* Success/Error Messages */}
        {fetchData.isSuccess && (
          <div className="p-3 bg-primary/10 border border-primary/20 rounded-lg">
            <p className="text-sm text-foreground">
              ✅ Synced {fetchData.data.data.new_commits} new commits
              {fetchData.data.data.skipped_duplicates > 0 && 
                ` (${fetchData.data.data.skipped_duplicates} duplicates skipped)`
              }
            </p>
          </div>
        )}

        {fetchData.isError && (
          <div className="p-3 bg-destructive/10 border border-destructive/20 rounded-lg">
            <p className="text-sm text-destructive">
              ❌ Sync failed: {fetchData.error?.message || 'Unknown error'}
            </p>
          </div>
        )}
      </div>
    </Card>
  );
}

export default GitHubDataStatus;

