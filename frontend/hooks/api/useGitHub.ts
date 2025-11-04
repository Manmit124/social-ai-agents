/**
 * GitHub API Hooks
 * 
 * Custom React Query hooks for GitHub data operations
 */

'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { createClient } from '@/lib/supabase/client';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Types
export interface GitHubStatus {
  total_commits: number;
  last_fetch_time: string | null;
  last_commit_date: string | null;
  needs_refresh: boolean;
  hours_since_fetch: number | null;
  refresh_reason: string;
  has_data: boolean;
  repositories_count: number;
  repositories: string[];
}

export interface GitHubCommit {
  id: string;
  repository_name: string;
  commit_hash: string;
  commit_message: string;
  commit_date: string;
  language: string | null;
  collected_at: string;
}

export interface GitHubActivity {
  commits: GitHubCommit[];
  total_commits: number;
  repositories: string[];
  last_fetch: {
    last_fetch_time: string;
    last_commit_date: string | null;
    total_commits_fetched: number;
    fetch_type: string;
  } | null;
}

export interface FetchDataResponse {
  success: boolean;
  message: string;
  data: {
    new_commits: number;
    skipped_duplicates: number;
    repositories_checked: number;
    fetch_type: string;
  };
}

export interface RefreshCheck {
  should_refresh: boolean;
  hours_since_fetch: number | null;
  last_fetch_time: string | null;
  reason: string;
}

/**
 * Hook to get GitHub data status
 */
export function useGitHubStatus() {
  const supabase = createClient();

  return useQuery<GitHubStatus>({
    queryKey: ['github', 'status'],
    queryFn: async () => {
      // Get session token
      const { data: { session } } = await supabase.auth.getSession();
      
      if (!session) {
        throw new Error('Not authenticated');
      }

      const response = await fetch(`${API_URL}/api/github/status`, {
        headers: {
          'Authorization': `Bearer ${session.access_token}`,
        },
      });

      if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Failed to fetch status' }));
        throw new Error(error.detail || 'Failed to fetch GitHub status');
      }

      const result = await response.json();
      return result.data;
    },
    // Refetch every 5 minutes to keep status fresh
    refetchInterval: 5 * 60 * 1000,
    // Keep previous data while fetching
    placeholderData: (previousData) => previousData,
  });
}

/**
 * Hook to get GitHub activity (commits)
 */
export function useGitHubActivity(limit: number = 100, days?: number) {
  const supabase = createClient();

  return useQuery<GitHubActivity>({
    queryKey: ['github', 'activity', limit, days],
    queryFn: async () => {
      // Get session token
      const { data: { session } } = await supabase.auth.getSession();
      
      if (!session) {
        throw new Error('Not authenticated');
      }

      const params = new URLSearchParams();
      params.append('limit', limit.toString());
      if (days) params.append('days', days.toString());
      
      const response = await fetch(`${API_URL}/api/github/activity?${params.toString()}`, {
        headers: {
          'Authorization': `Bearer ${session.access_token}`,
        },
      });

      if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Failed to fetch activity' }));
        throw new Error(error.detail || 'Failed to fetch GitHub activity');
      }

      const result = await response.json();
      return result.data;
    },
    // Only fetch if user has data
    enabled: true,
  });
}

/**
 * Hook to check if refresh is needed
 */
export function useRefreshCheck(hoursThreshold: number = 24) {
  const supabase = createClient();

  return useQuery<RefreshCheck>({
    queryKey: ['github', 'refresh-check', hoursThreshold],
    queryFn: async () => {
      // Get session token
      const { data: { session } } = await supabase.auth.getSession();
      
      if (!session) {
        throw new Error('Not authenticated');
      }

      const response = await fetch(`${API_URL}/api/github/refresh-check?hours_threshold=${hoursThreshold}`, {
        headers: {
          'Authorization': `Bearer ${session.access_token}`,
        },
      });

      if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Failed to check refresh' }));
        throw new Error(error.detail || 'Failed to check refresh status');
      }

      const result = await response.json();
      return result.data;
    },
    // Check every 10 minutes
    refetchInterval: 10 * 60 * 1000,
  });
}

/**
 * Hook to fetch GitHub data (mutation)
 */
export function useFetchGitHubData() {
  const queryClient = useQueryClient();
  const supabase = createClient();

  return useMutation<FetchDataResponse, Error, { days?: number }>({
    mutationFn: async ({ days = 30 }) => {
      // Get session token
      const { data: { session } } = await supabase.auth.getSession();
      
      if (!session) {
        throw new Error('Not authenticated');
      }

      const response = await fetch(`${API_URL}/api/github/fetch-data?days=${days}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${session.access_token}`,
        },
      });

      if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Failed to fetch data' }));
        throw new Error(error.detail || 'Failed to fetch GitHub data');
      }

      return await response.json();
    },
    onSuccess: () => {
      // Invalidate and refetch GitHub queries
      queryClient.invalidateQueries({ queryKey: ['github'] });
    },
  });
}

/**
 * Hook to get time ago string
 */
export function useTimeAgo(dateString: string | null): string {
  if (!dateString) return 'Never';

  const date = new Date(dateString);
  const now = new Date();
  const seconds = Math.floor((now.getTime() - date.getTime()) / 1000);

  if (seconds < 60) return 'Just now';
  if (seconds < 3600) return `${Math.floor(seconds / 60)} minutes ago`;
  if (seconds < 86400) return `${Math.floor(seconds / 3600)} hours ago`;
  if (seconds < 604800) return `${Math.floor(seconds / 86400)} days ago`;
  
  return date.toLocaleDateString();
}

/**
 * Hook to format commit date
 */
export function useFormatDate(dateString: string | null): string {
  if (!dateString) return 'N/A';
  
  const date = new Date(dateString);
  return date.toLocaleString('en-US', {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}

/**
 * Types for GitHub Context
 */
export interface GitHubContext {
  id: string;
  user_id: string;
  current_projects: string[];
  tech_stack: string[];
  recent_activity_summary: string;
  ai_insights: {
    focus_areas: string[];
    key_achievements: string[];
    summary_for_social: string;
    generated_at: string;
  } | null;
  activity_stats: {
    commits_last_7_days: number;
    commits_last_30_days: number;
    average_commits_per_day: number;
    most_active_day: string;
    most_active_time: string;
  };
  last_github_fetch: string;
  last_updated: string;
}

/**
 * Hook to get GitHub context (cached)
 */
export function useGitHubContext() {
  const supabase = createClient();

  return useQuery<GitHubContext | null>({
    queryKey: ['github', 'context'],
    queryFn: async () => {
      // Get session token
      const { data: { session } } = await supabase.auth.getSession();
      
      if (!session) {
        throw new Error('Not authenticated');
      }

      const response = await fetch(`${API_URL}/api/github/context`, {
        headers: {
          'Authorization': `Bearer ${session.access_token}`,
        },
      });

      if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Failed to fetch context' }));
        throw new Error(error.detail || 'Failed to fetch GitHub context');
      }

      const result = await response.json();
      return result.data;
    },
    // Refetch every 10 minutes
    refetchInterval: 10 * 60 * 1000,
  });
}

/**
 * Hook to analyze GitHub data with AI (manual refresh)
 */
export function useAnalyzeGitHub() {
  const queryClient = useQueryClient();
  const supabase = createClient();

  return useMutation<GitHubContext, Error>({
    mutationFn: async () => {
      // Get session token
      const { data: { session } } = await supabase.auth.getSession();
      
      if (!session) {
        throw new Error('Not authenticated');
      }

      const response = await fetch(`${API_URL}/api/github/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${session.access_token}`,
        },
      });

      if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Failed to analyze data' }));
        throw new Error(error.detail || 'Failed to analyze GitHub data');
      }

      const result = await response.json();
      return result.data;
    },
    onSuccess: () => {
      // Invalidate and refetch context
      queryClient.invalidateQueries({ queryKey: ['github', 'context'] });
    },
  });
}

