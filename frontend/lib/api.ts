const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

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


