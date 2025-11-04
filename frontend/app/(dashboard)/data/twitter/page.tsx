/**
 * Twitter Data Page
 * 
 * View and analyze your Twitter data
 */

'use client';

import React, { useState } from 'react';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Download, RefreshCw } from 'lucide-react';
import { TwitterStyleProfile } from '@/components/twitter';
import { api } from '@/lib/api';
import { useAuth } from '@/hooks/auth/useAuth';

export default function TwitterDataPage() {
  const { user } = useAuth();
  const [fetching, setFetching] = useState(false);
  const [fetchResult, setFetchResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleFetchTweets = async () => {
    try {
      setFetching(true);
      setError(null);
      setFetchResult(null);

      const data = await api.post('/api/twitter/fetch-tweets?limit=20');
      
      if (data.success) {
        setFetchResult(data);
      } else {
        setError('Failed to fetch tweets');
      }
    } catch (err: any) {
      console.error('Error fetching tweets:', err);
      
      // Check for rate limit error
      if (err.response?.status === 429) {
        setError('⏱️ Twitter API rate limit reached. Please wait 15 minutes and try again. Twitter limits how many requests you can make per 15-minute window.');
      } else {
        setError(err.response?.data?.detail || 'Failed to fetch tweets. Make sure your Twitter account is connected.');
      }
    } finally {
      setFetching(false);
    }
  };

  return (
    <div className="flex h-full flex-col p-8">
      <div className="w-full max-w-7xl mx-auto space-y-8">
        
        {/* Header Section */}
        <div className="space-y-2">
          <h1 className="text-4xl font-bold tracking-tight">
            Twitter <span className="text-primary">Integration</span>
          </h1>
          <p className="text-lg text-muted-foreground">
            Analyze your tweets and writing style
          </p>
        </div>

        {/* Fetch Button Section */}
        <div className="flex justify-end">
          <Button
            onClick={handleFetchTweets}
            disabled={fetching}
            size="lg"
            className="gap-2"
          >
            {fetching ? (
              <>
                <RefreshCw className="w-4 h-4 animate-spin" />
                Fetching Tweets...
              </>
            ) : (
              <>
                <Download className="w-4 h-4" />
                Fetch Tweets
              </>
            )}
          </Button>
        </div>

        {/* Fetch Result Message */}
        {fetchResult && (
          <Card className="p-4 bg-green-50 dark:bg-green-950 border-green-200 dark:border-green-800">
            <div className="flex items-start gap-3">
              <div className="text-2xl">✅</div>
              <div className="flex-1">
                <p className="font-medium text-green-900 dark:text-green-100">
                  {fetchResult.message}
                </p>
                <p className="text-sm text-green-700 dark:text-green-300 mt-1">
                  New tweets: {fetchResult.new_tweets} | Already stored: {fetchResult.existing_tweets}
                </p>
                {fetchResult.errors && fetchResult.errors.length > 0 && (
                  <p className="text-xs text-orange-600 dark:text-orange-400 mt-1">
                    Some errors occurred during fetch
                  </p>
                )}
              </div>
            </div>
          </Card>
        )}

        {/* Error Message */}
        {error && (
          <Card className="p-4 bg-destructive/10 border-destructive/20">
            <div className="flex items-start gap-3">
              <div className="text-2xl">❌</div>
              <div className="flex-1">
                <p className="font-medium text-destructive">Error</p>
                <p className="text-sm text-destructive/80 mt-1">{error}</p>
              </div>
            </div>
          </Card>
        )}

        {/* Twitter Style Profile Component */}
        <TwitterStyleProfile />

        {/* How to use Section - BOTTOM */}
        <div className="p-6 bg-card border border-border rounded-lg">
          <h3 className="font-semibold text-foreground mb-3 flex items-center gap-2">
            <span className="text-primary">💡</span>
            How to use
          </h3>
          <ul className="text-sm text-muted-foreground space-y-2">
            <li className="flex items-start gap-2">
              <span className="text-primary mt-0.5">•</span>
              <span>Make sure your Twitter account is connected in Settings</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-primary mt-0.5">•</span>
              <span>Click "Fetch Tweets" to import your last 20 tweets from Twitter</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-primary mt-0.5">•</span>
              <span>Your style profile will be automatically generated and analyzed</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-primary mt-0.5">•</span>
              <span>View your writing patterns, tone, and best performing content insights</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-primary mt-0.5">•</span>
              <span>Use the "Regenerate" button to update your style profile anytime</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}

