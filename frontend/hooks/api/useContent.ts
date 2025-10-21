"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { createClient } from "@/lib/supabase/client";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface GenerateContentRequest {
  prompt: string;
  platform: "twitter" | "linkedin" | "reddit";
}

export interface GeneratedContent {
  platform: string;
  content: string;
  hashtags: string[];
  final_content: string;
  char_count: number;
}

export interface GenerateContentResponse {
  success: boolean;
  data?: GeneratedContent;
  error?: string;
}

export interface PostContentRequest {
  content: string;
  user_prompt: string;
  platform: "twitter" | "linkedin" | "reddit";
  hashtags?: string[];
}

export interface PostContentResponse {
  success: boolean;
  post_id?: string;
  url?: string;
  error?: string;
}

/**
 * Hook to generate and post content to social media platforms
 */
export function useContent() {
  const queryClient = useQueryClient();
  const supabase = createClient();

  // Generate content mutation
  const generateContent = useMutation({
    mutationFn: async (request: GenerateContentRequest): Promise<GeneratedContent> => {
      // Get session token
      const { data: { session } } = await supabase.auth.getSession();
      
      if (!session) {
        throw new Error("Not authenticated");
      }

      const response = await fetch(`${API_URL}/api/generate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${session.access_token}`,
        },
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Failed to generate content");
      }

      const result: GenerateContentResponse = await response.json();
      
      if (!result.success || !result.data) {
        throw new Error(result.error || "Failed to generate content");
      }

      return result.data;
    },
    onError: (error) => {
      console.error("Error generating content:", error);
    },
  });

  // Post content mutation
  const postContent = useMutation({
    mutationFn: async (request: PostContentRequest): Promise<PostContentResponse> => {
      // Get session token
      const { data: { session } } = await supabase.auth.getSession();
      
      if (!session) {
        throw new Error("Not authenticated");
      }

      const response = await fetch(`${API_URL}/api/post`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${session.access_token}`,
        },
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Failed to post content");
      }

      const result: PostContentResponse = await response.json();
      
      if (!result.success) {
        throw new Error(result.error || "Failed to post content");
      }

      return result;
    },
    onSuccess: () => {
      // Invalidate posts query to refresh history
      queryClient.invalidateQueries({ queryKey: ["posts"] });
    },
    onError: (error) => {
      console.error("Error posting content:", error);
    },
  });

  return {
    generateContent,
    postContent,
    isGenerating: generateContent.isPending,
    isPosting: postContent.isPending,
    generatedContent: generateContent.data,
    postResult: postContent.data,
    generateError: generateContent.error,
    postError: postContent.error,
  };
}

