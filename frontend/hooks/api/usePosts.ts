"use client";

import { useQuery, useQueryClient } from "@tanstack/react-query";
import { createClient } from "@/lib/supabase/client";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface Post {
  id: string;
  platform: string;
  user_prompt: string;
  generated_content: string;
  hashtags: string[];
  platform_post_id?: string;
  platform_post_url?: string;
  status: string;
  created_at: string;
}

export interface PostsResponse {
  success: boolean;
  posts: Post[];
  error?: string;
}

/**
 * Hook to fetch user's post history
 */
export function usePosts(platform?: string) {
  const queryClient = useQueryClient();
  const supabase = createClient();

  // Fetch posts
  const {
    data: posts,
    isLoading,
    error,
    refetch
  } = useQuery({
    queryKey: ["posts", platform],
    queryFn: async (): Promise<Post[]> => {
      // Get session token
      const { data: { session } } = await supabase.auth.getSession();
      
      if (!session) {
        throw new Error("Not authenticated");
      }

      const url = new URL(`${API_URL}/api/history`);
      if (platform) {
        url.searchParams.append("platform", platform);
      }

      const response = await fetch(url.toString(), {
        headers: {
          "Authorization": `Bearer ${session.access_token}`,
        },
      });

      if (!response.ok) {
        throw new Error("Failed to fetch posts");
      }

      const data: PostsResponse = await response.json();
      return data.posts;
    },
    staleTime: 30 * 1000, // 30 seconds
    refetchOnWindowFocus: true,
  });

  // Get posts for a specific platform
  const getPostsByPlatform = (targetPlatform: string): Post[] => {
    return posts?.filter((post) => post.platform === targetPlatform) ?? [];
  };

  // Get recent posts
  const getRecentPosts = (limit: number = 10): Post[] => {
    return posts?.slice(0, limit) ?? [];
  };

  return {
    posts: posts ?? [],
    isLoading,
    error,
    refetch,
    getPostsByPlatform,
    getRecentPosts,
  };
}

