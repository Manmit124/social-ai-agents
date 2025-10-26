"use client";

import { useState, useEffect } from "react";
import { Sparkles, Send, Copy, Check, Loader2, Zap } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Skeleton } from "@/components/ui/skeleton";
import { PlatformSelector, Platform } from "./PlatformSelector";
import { useContent } from "@/hooks/api/useContent";
import { useConnections } from "@/hooks/api/useConnections";

export function ContentGenerator() {
  const [platform, setPlatform] = useState<Platform>("twitter");
  const [prompt, setPrompt] = useState("");
  const [copied, setCopied] = useState(false);
  const [showSkeleton, setShowSkeleton] = useState(false);

  const { generateContent, postContent, isGenerating, isPosting, generatedContent, postResult } = useContent();
  const { isConnected } = useConnections();

  // Show skeleton when generating starts
  useEffect(() => {
    if (isGenerating) {
      setShowSkeleton(true);
    } else if (generatedContent) {
      // Small delay to make the transition smooth
      setTimeout(() => setShowSkeleton(false), 300);
    }
  }, [isGenerating, generatedContent]);

  const handleGenerate = () => {
    if (!prompt.trim()) return;
    
    generateContent.mutate({
      prompt: prompt.trim(),
      platform,
    });
  };

  const handlePost = () => {
    if (!generatedContent) return;

    postContent.mutate({
      content: generatedContent.final_content,
      user_prompt: prompt,
      platform,
      hashtags: generatedContent.hashtags,
    });
  };

  const handleCopy = async () => {
    if (!generatedContent) return;
    
    await navigator.clipboard.writeText(generatedContent.final_content);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const canGenerate = prompt.trim().length > 0 && !isGenerating;
  const canPost = generatedContent && !isPosting && isConnected(platform) && !postResult;

  return (
    <div className="space-y-8">
      {/* Platform Selector - Centered */}
      <div className="flex justify-center">
        <PlatformSelector selected={platform} onSelect={setPlatform} />
      </div>

      {/* Main Input Area - Clean & Minimal */}
      <div className="space-y-4">
        <div className="relative">
          <Textarea
            placeholder="What do you want to share today? Describe your idea..."
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            rows={6}
            className="resize-none text-lg border-2 focus:border-primary transition-colors rounded-2xl px-6 py-5 bg-card/50 backdrop-blur-sm"
            disabled={isGenerating}
          />
        </div>

        {/* Generate Button */}
        <Button
          onClick={handleGenerate}
          disabled={!canGenerate}
          className={`w-full h-14 text-base rounded-xl shadow-lg hover:shadow-xl transition-all ${
            canGenerate ? 'hover:scale-105 active:scale-95' : ''
          }`}
          size="lg"
        >
          {isGenerating ? (
            <>
              <Loader2 className="mr-2 h-5 w-5 animate-spin" />
              Creating magic...
            </>
          ) : (
            <>
              <Sparkles className={`mr-2 h-5 w-5 ${canGenerate ? 'animate-pulse' : ''}`} />
              Generate Content
            </>
          )}
        </Button>

        {/* Connection Warning */}
        {!isConnected(platform) && (
          <div className="text-center">
            <p className="text-sm text-muted-foreground">
              Connect your {platform === "twitter" ? "X" : platform.charAt(0).toUpperCase() + platform.slice(1)} account in{" "}
              <a href="/settings" className="text-primary hover:underline font-medium">
                Settings
              </a>{" "}
              to post directly
            </p>
          </div>
        )}
      </div>

      {/* Loading Skeleton - Fast & Smooth */}
      {showSkeleton && isGenerating && (
        <div className="space-y-6 animate-in fade-in slide-in-from-bottom-2 duration-300">
          <div className="rounded-2xl border-2 border-primary/30 bg-gradient-to-br from-primary/5 to-primary/10 backdrop-blur-sm p-6 shadow-xl relative overflow-hidden">
            {/* Animated gradient overlay */}
            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-primary/10 to-transparent animate-shimmer" />
            
            {/* AI Thinking Indicator */}
            <div className="flex items-center gap-3 mb-6 relative z-10">
              <div className="relative">
                <Sparkles className="h-6 w-6 text-primary animate-pulse" />
                <Zap className="h-4 w-4 text-primary absolute -top-1 -right-1 animate-ping" />
              </div>
              <div className="space-y-1">
                <h3 className="text-lg font-semibold text-primary animate-pulse">AI is crafting your content...</h3>
                <p className="text-xs text-muted-foreground">This will only take a moment</p>
              </div>
            </div>

            {/* Content Skeleton */}
            <div className="space-y-4 relative z-10">
              <Skeleton className="h-4 w-full" />
              <Skeleton className="h-4 w-[95%]" />
              <Skeleton className="h-4 w-[90%]" />
              <Skeleton className="h-4 w-[85%]" />
              <Skeleton className="h-4 w-[70%]" />
            </div>

            {/* Hashtags Skeleton */}
            <div className="flex gap-2 mt-6 relative z-10">
              <Skeleton className="h-7 w-20 rounded-full" />
              <Skeleton className="h-7 w-24 rounded-full" />
              <Skeleton className="h-7 w-20 rounded-full" />
            </div>

            {/* Progress dots */}
            <div className="flex justify-center gap-2 mt-6 relative z-10">
              <div className="h-2 w-2 rounded-full bg-primary animate-bounce" style={{ animationDelay: '0ms' }} />
              <div className="h-2 w-2 rounded-full bg-primary animate-bounce" style={{ animationDelay: '150ms' }} />
              <div className="h-2 w-2 rounded-full bg-primary animate-bounce" style={{ animationDelay: '300ms' }} />
            </div>
          </div>
        </div>
      )}

      {/* Generated Content Preview - Elevated Card */}
      {generatedContent && !showSkeleton && (
        <div className="space-y-6 animate-in fade-in slide-in-from-bottom-2 duration-500">
          {/* Content Card */}
          <div className="rounded-2xl border-2 border-primary/20 bg-card/80 backdrop-blur-sm p-6 shadow-xl animate-in zoom-in-95 duration-300">
            {/* Header */}
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <Check className="h-5 w-5 text-green-500 animate-in zoom-in duration-300" />
                <h3 className="text-lg font-semibold">Your Content</h3>
              </div>
              <span className="text-sm text-muted-foreground bg-muted px-3 py-1 rounded-full animate-in slide-in-from-right duration-300">
                {generatedContent.char_count} chars
              </span>
            </div>

            {/* Content */}
            <div className="rounded-xl bg-muted/50 p-5 mb-4 animate-in fade-in duration-500" style={{ animationDelay: '100ms' }}>
              <p className="whitespace-pre-wrap text-base leading-relaxed">
                {generatedContent.final_content}
              </p>
            </div>

            {/* Hashtags */}
            {generatedContent.hashtags.length > 0 && (
              <div className="flex flex-wrap gap-2 mb-4">
                {generatedContent.hashtags.map((tag, index) => (
                  <span
                    key={index}
                    className="rounded-full bg-primary/10 px-4 py-1.5 text-sm font-medium text-primary animate-in zoom-in duration-300"
                    style={{ animationDelay: `${200 + index * 50}ms` }}
                  >
                    {tag}
                  </span>
                ))}
              </div>
            )}

            {/* Action Buttons */}
            <div className="flex gap-3 animate-in slide-in-from-bottom duration-300" style={{ animationDelay: '300ms' }}>
              <Button
                onClick={handleCopy}
                variant="outline"
                className="flex-1 h-12 rounded-xl hover:scale-105 transition-transform"
                size="lg"
              >
                {copied ? (
                  <>
                    <Check className="mr-2 h-4 w-4 animate-in zoom-in duration-200" />
                    Copied!
                  </>
                ) : (
                  <>
                    <Copy className="mr-2 h-4 w-4" />
                    Copy
                  </>
                )}
              </Button>
              <Button
                onClick={handlePost}
                disabled={!canPost}
                className="flex-1 h-12 rounded-xl shadow-lg hover:scale-105 transition-transform"
                size="lg"
              >
                {isPosting ? (
                  <>
                    <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                    Posting...
                  </>
                ) : postResult ? (
                  <>
                    <Check className="mr-2 h-4 w-4 animate-in zoom-in duration-200" />
                    Posted!
                  </>
                ) : (
                  <>
                    <Send className="mr-2 h-4 w-4" />
                    Post Now
                  </>
                )}
              </Button>
            </div>

            {/* Success Message */}
            {postResult && postResult.url && (
              <div className="mt-4 rounded-xl bg-green-500/10 border border-green-500/20 p-4 text-center animate-in slide-in-from-bottom duration-300">
                <p className="text-sm text-green-700 dark:text-green-400 font-medium">
                  🎉 Successfully posted!{" "}
                  <a
                    href={postResult.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="underline hover:no-underline"
                  >
                    View post
                  </a>
                </p>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

