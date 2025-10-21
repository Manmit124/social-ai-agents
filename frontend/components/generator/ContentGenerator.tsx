"use client";

import { useState } from "react";
import { Sparkles, Send, Copy, Check } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { PlatformSelector, Platform } from "./PlatformSelector";
import { useContent } from "@/hooks/api/useContent";
import { useConnections } from "@/hooks/api/useConnections";

export function ContentGenerator() {
  const [platform, setPlatform] = useState<Platform>("twitter");
  const [prompt, setPrompt] = useState("");
  const [copied, setCopied] = useState(false);

  const { generateContent, postContent, isGenerating, isPosting, generatedContent, postResult } = useContent();
  const { isConnected } = useConnections();

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
    <div className="space-y-6">
      {/* Platform Selector */}
      <PlatformSelector selected={platform} onSelect={setPlatform} />

      {/* Prompt Input */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Sparkles className="h-5 w-5 text-primary" />
            What do you want to share?
          </CardTitle>
          <CardDescription>
            Describe your idea and let AI create engaging content for {platform}
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <Textarea
            placeholder={`Example: "Share an insight about the future of AI in healthcare..."`}
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            rows={4}
            className="resize-none"
            disabled={isGenerating}
          />
          <Button
            onClick={handleGenerate}
            disabled={!canGenerate}
            className="w-full"
            size="lg"
          >
            {isGenerating ? (
              <>
                <Sparkles className="mr-2 h-4 w-4 animate-spin" />
                Generating...
              </>
            ) : (
              <>
                <Sparkles className="mr-2 h-4 w-4" />
                Generate Content
              </>
            )}
          </Button>
        </CardContent>
      </Card>

      {/* Generated Content Preview */}
      {generatedContent && (
        <Card className="border-primary/50">
          <CardHeader>
            <CardTitle className="flex items-center justify-between">
              <span>Generated Content</span>
              <span className="text-sm font-normal text-muted-foreground">
                {generatedContent.char_count} characters
              </span>
            </CardTitle>
            <CardDescription>
              Review and post to {platform}
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {/* Content Preview */}
            <div className="rounded-lg bg-muted p-4">
              <p className="whitespace-pre-wrap text-foreground">
                {generatedContent.final_content}
              </p>
            </div>

            {/* Hashtags */}
            {generatedContent.hashtags.length > 0 && (
              <div className="flex flex-wrap gap-2">
                {generatedContent.hashtags.map((tag, index) => (
                  <span
                    key={index}
                    className="rounded-full bg-primary/10 px-3 py-1 text-sm text-primary"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            )}

            {/* Action Buttons */}
            <div className="flex gap-2">
              <Button
                onClick={handleCopy}
                variant="outline"
                className="flex-1"
              >
                {copied ? (
                  <>
                    <Check className="mr-2 h-4 w-4" />
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
                className="flex-1"
                size="lg"
              >
                {isPosting ? (
                  <>
                    <Send className="mr-2 h-4 w-4 animate-pulse" />
                    Posting...
                  </>
                ) : postResult ? (
                  <>
                    <Check className="mr-2 h-4 w-4" />
                    Posted!
                  </>
                ) : (
                  <>
                    <Send className="mr-2 h-4 w-4" />
                    Post to {platform.charAt(0).toUpperCase() + platform.slice(1)}
                  </>
                )}
              </Button>
            </div>

            {/* Success Message */}
            {postResult && postResult.url && (
              <div className="rounded-lg bg-green-500/10 p-4 text-center">
                <p className="text-sm text-green-700 dark:text-green-400">
                  Successfully posted!{" "}
                  <a
                    href={postResult.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="font-medium underline hover:no-underline"
                  >
                    View post
                  </a>
                </p>
              </div>
            )}
          </CardContent>
        </Card>
      )}
    </div>
  );
}

