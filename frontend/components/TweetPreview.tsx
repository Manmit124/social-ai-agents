'use client';

import { Card, CardContent, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Twitter, RefreshCw, Check } from 'lucide-react';

interface TweetPreviewProps {
  content: string;
  hashtags: string[];
  finalContent: string;
  charCount: number;
  onPost: () => Promise<void>;
  onRegenerate: () => void;
  isPosting: boolean;
  posted: boolean;
  tweetUrl?: string;
}

export function TweetPreview({
  content,
  hashtags,
  finalContent,
  charCount,
  onPost,
  onRegenerate,
  isPosting,
  posted,
  tweetUrl,
}: TweetPreviewProps) {
  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="flex items-center justify-between">
          <span>Preview</span>
          <span className={`text-sm ${charCount > 280 ? 'text-destructive' : 'text-muted-foreground'}`}>
            {charCount}/280
          </span>
        </CardTitle>
      </CardHeader>
      <CardContent>
        <div className="bg-muted p-4 rounded-md space-y-3">
          <p className="text-foreground whitespace-pre-wrap">{content}</p>
          {hashtags.length > 0 && (
            <p className="text-primary font-medium">{hashtags.join(' ')}</p>
          )}
        </div>
      </CardContent>
      <CardFooter className="flex gap-3">
        <Button
          onClick={onRegenerate}
          variant="outline"
          disabled={isPosting || posted}
          className="flex-1"
        >
          <RefreshCw className="mr-2 h-4 w-4" />
          Regenerate
        </Button>
        {!posted ? (
          <Button
            onClick={onPost}
            disabled={isPosting || charCount > 280}
            className="flex-1"
          >
            <Twitter className="mr-2 h-4 w-4" />
            {isPosting ? 'Posting...' : 'Post to Twitter'}
          </Button>
        ) : (
          <Button
            variant="secondary"
            disabled
            className="flex-1"
          >
            <Check className="mr-2 h-4 w-4" />
            Posted
          </Button>
        )}
      </CardFooter>
      {posted && tweetUrl && (
        <CardFooter className="pt-0">
          <a
            href={tweetUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="text-sm text-primary hover:underline w-full text-center"
          >
            View on Twitter →
          </a>
        </CardFooter>
      )}
    </Card>
  );
}


