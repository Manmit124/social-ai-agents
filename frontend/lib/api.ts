import { createClient } from '@/lib/supabase/client';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Helper to get auth token from Supabase session
const getAuthToken = async (): Promise<string | null> => {
  if (typeof window === 'undefined') return null;
  
  try {
    const supabase = createClient();
    const { data: { session } } = await supabase.auth.getSession();
    return session?.access_token || null;
  } catch (error) {
    console.error('Error getting auth token:', error);
    return null;
  }
};

export interface GenerateTweetResponse {
  success: boolean;
  data?: {
    content: string;
    hashtags: string[];
    final_content: string;
    char_count: number;
  };
  error?: string;
}

export interface PostTweetResponse {
  success: boolean;
  tweet_id?: string;
  url?: string;
  error?: string;
}

export interface TweetHistoryItem {
  id: string;
  prompt: string;
  content: string;
  posted_at: string;
  tweet_url?: string;
}

export interface HistoryResponse {
  success: boolean;
  tweets: TweetHistoryItem[];
  error?: string;
}

export const api = {
  // Generic GET method
  async get(endpoint: string, options?: RequestInit) {
    const token = await getAuthToken();
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` }),
      ...options?.headers,
    };

    const response = await fetch(`${API_URL}${endpoint}`, {
      method: 'GET',
      headers,
      ...options,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Request failed' }));
      throw { response: { status: response.status, data: error } };
    }

    return response.json();
  },

  // Generic POST method
  async post(endpoint: string, data?: any, options?: RequestInit) {
    const token = await getAuthToken();
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` }),
      ...options?.headers,
    };

    const response = await fetch(`${API_URL}${endpoint}`, {
      method: 'POST',
      headers,
      body: data ? JSON.stringify(data) : undefined,
      ...options,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Request failed' }));
      throw { response: { status: response.status, data: error } };
    }

    return response.json();
  },

  // Legacy methods for backward compatibility
  async generateTweet(prompt: string): Promise<GenerateTweetResponse> {
    const response = await fetch(`${API_URL}/api/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ prompt }),
    });

    if (!response.ok) {
      throw new Error('Failed to generate tweet');
    }

    return response.json();
  },

  async postTweet(content: string, user_prompt: string): Promise<PostTweetResponse> {
    const response = await fetch(`${API_URL}/api/post`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ content, user_prompt }),
    });

    if (!response.ok) {
      throw new Error('Failed to post tweet');
    }

    return response.json();
  },

  async getHistory(): Promise<HistoryResponse> {
    const response = await fetch(`${API_URL}/api/history`);

    if (!response.ok) {
      throw new Error('Failed to fetch history');
    }

    return response.json();
  },
};


