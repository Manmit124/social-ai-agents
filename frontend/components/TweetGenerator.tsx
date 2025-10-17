'use client';

import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Textarea } from '@/components/ui/textarea';
import { Button } from '@/components/ui/button';
import { Sparkles } from 'lucide-react';
import { api } from '@/lib/api';
import { TweetPreview } from './TweetPreview';
import { TweetHistory } from './TweetHistory';
import type { TweetHistoryItem } from '@/lib/api';

interface GeneratedTweet {
  content: string;
  hashtags: string[];
  finalContent: string;
  charCount: number;
}

export function TweetGenerator() {
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [generatedTweet, setGeneratedTweet] = useState<GeneratedTweet | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isPosting, setIsPosting] = useState(false);
  const [posted, setPosted] = useState(false);
  const [tweetUrl, setTweetUrl] = useState<string | undefined>();
  const [history, setHistory] = useState<TweetHistoryItem[]>([]);

  const loadHistory = async () => {
    try {
      const response = await api.getHistory();
      if (response.success) {
        setHistory(response.tweets);
      }
    } catch (err) {
      console.error('Failed to load history:', err);
    }
  };

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      setError('Please enter a prompt');
      return;
    }

    setLoading(true);
    setError(null);
    setGeneratedTweet(null);
    setPosted(false);
    setTweetUrl(undefined);

    try {
      const response = await api.generateTweet(prompt);

      if (response.success && response.data) {
        setGeneratedTweet({
          content: response.data.content,
          hashtags: response.data.hashtags,
          finalContent: response.data.final_content,
          charCount: response.data.char_count,
        });
      } else {
        setError(response.error || 'Failed to generate tweet');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate tweet');
    } finally {
      setLoading(false);
    }
  };

  const handlePost = async () => {
    if (!generatedTweet) return;

    setIsPosting(true);
    setError(null);

    try {
      const response = await api.postTweet(generatedTweet.finalContent, prompt);

      if (response.success) {
        setPosted(true);
        setTweetUrl(response.url);
        // Reload history
        await loadHistory();
      } else {
        setError(response.error || 'Failed to post tweet');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to post tweet');
    } finally {
      setIsPosting(false);
    }
  };

  const handleRegenerate = () => {
    setGeneratedTweet(null);
    setPosted(false);
    setTweetUrl(undefined);
    handleGenerate();
  };

  // Load history on mount
  useState(() => {
    loadHistory();
  });

  return (
    <div className="space-y-6">
      <Card className="w-full">
        <CardHeader>
          <CardTitle>AI Tweet Generator</CardTitle>
          <CardDescription>
            Enter a prompt and let AI generate an engaging tweet for you
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <Textarea
              placeholder="What would you like to tweet about? (e.g., 'Write about AI and creativity')"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              rows={4}
              className="resize-none"
            />
          </div>

          <Button
            onClick={handleGenerate}
            disabled={loading || !prompt.trim()}
            className="w-full"
            size="lg"
          >
            <Sparkles className="mr-2 h-5 w-5" />
            {loading ? 'Generating...' : 'Generate Tweet'}
          </Button>

          {error && (
            <div className="bg-destructive/10 text-destructive px-4 py-3 rounded-md text-sm">
              {error}
            </div>
          )}
        </CardContent>
      </Card>

      {generatedTweet && (
        <TweetPreview
          content={generatedTweet.content}
          hashtags={generatedTweet.hashtags}
          finalContent={generatedTweet.finalContent}
          charCount={generatedTweet.charCount}
          onPost={handlePost}
          onRegenerate={handleRegenerate}
          isPosting={isPosting}
          posted={posted}
          tweetUrl={tweetUrl}
        />
      )}

      <TweetHistory tweets={history} />
    </div>
  );
}


