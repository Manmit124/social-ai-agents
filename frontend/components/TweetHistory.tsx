'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { TweetHistoryItem } from '@/lib/api';
import { ExternalLink } from 'lucide-react';

interface TweetHistoryProps {
  tweets: TweetHistoryItem[];
}

export function TweetHistory({ tweets }: TweetHistoryProps) {
  if (tweets.length === 0) {
    return null;
  }

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Recent Tweets</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {tweets.map((tweet) => (
            <div
              key={tweet.id}
              className="border-b pb-4 last:border-b-0 last:pb-0"
            >
              <p className="text-sm text-muted-foreground mb-1">
                Prompt: {tweet.prompt}
              </p>
              <p className="text-foreground mb-2">{tweet.content}</p>
              <div className="flex items-center justify-between">
                <span className="text-xs text-muted-foreground">
                  {new Date(tweet.posted_at).toLocaleString()}
                </span>
                {tweet.tweet_url && (
                  <a
                    href={tweet.tweet_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-xs text-primary hover:underline flex items-center gap-1"
                  >
                    View <ExternalLink className="h-3 w-3" />
                  </a>
                )}
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}


