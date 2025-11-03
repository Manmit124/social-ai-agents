/**
 * GitHub Data Page
 * 
 * View and manage GitHub activity data
 */

'use client';

import React from 'react';
import { GitHubDataStatus, GitHubActivity } from '@/components/github';
import { useConnections } from '@/hooks/api/useConnections';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import { Github, Sparkles } from 'lucide-react';

export default function GitHubPage() {
  const { isConnected, connectGitHub, isLoading } = useConnections();
  const isGitHubConnected = isConnected('github');

  // Loading state
  if (isLoading) {
    return (
      <div className="flex h-full flex-col p-8">
        <div className="w-full max-w-7xl mx-auto space-y-8">
          <div className="space-y-2">
            <div className="h-10 bg-muted rounded w-1/3 animate-pulse"></div>
            <div className="h-6 bg-muted rounded w-1/2 animate-pulse"></div>
          </div>
        </div>
      </div>
    );
  }

  // Not connected state
  if (!isGitHubConnected) {
    return (
      <div className="flex h-full flex-col items-center justify-center p-8">
        <div className="w-full max-w-2xl mx-auto space-y-8">
          
          {/* Hero Card */}
          <Card className="p-12 border-border text-center space-y-6">
            <div className="flex justify-center">
              <div className="relative">
                <div className="absolute inset-0 bg-primary/20 rounded-full blur-2xl"></div>
                <div className="relative bg-primary/10 p-6 rounded-full">
                  <Github className="w-16 h-16 text-primary" />
                </div>
              </div>
            </div>

            <div className="space-y-3">
              <h1 className="text-3xl font-bold tracking-tight">
                Connect Your <span className="text-primary">GitHub</span>
              </h1>
              <p className="text-lg text-muted-foreground max-w-md mx-auto">
                Connect your GitHub account to fetch your commits and generate personalized content based on your coding activity
              </p>
            </div>

            <div className="pt-4">
              <Button
                onClick={() => connectGitHub.mutate()}
                disabled={connectGitHub.isPending}
                size="lg"
                className="text-lg px-8 py-6"
              >
                <Github className="mr-2 h-5 w-5" />
                {connectGitHub.isPending ? 'Connecting...' : 'Connect GitHub'}
              </Button>
            </div>

            {connectGitHub.isError && (
              <div className="p-3 bg-destructive/10 border border-destructive/20 rounded-lg">
                <p className="text-sm text-destructive">
                  Failed to connect GitHub. Please try again.
                </p>
              </div>
            )}
          </Card>

          {/* Features Section */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <Card className="p-6 border-border space-y-2">
              <div className="text-primary text-2xl">🔒</div>
              <h3 className="font-semibold text-foreground">Secure</h3>
              <p className="text-sm text-muted-foreground">
                Your data is stored securely and never shared
              </p>
            </Card>

            <Card className="p-6 border-border space-y-2">
              <div className="text-primary text-2xl">⚡</div>
              <h3 className="font-semibold text-foreground">Smart Refresh</h3>
              <p className="text-sm text-muted-foreground">
                Only fetches new commits to save API calls
              </p>
            </Card>

            <Card className="p-6 border-border space-y-2">
              <div className="text-primary text-2xl">
                <Sparkles className="w-6 h-6" />
              </div>
              <h3 className="font-semibold text-foreground">AI-Powered</h3>
              <p className="text-sm text-muted-foreground">
                Generate content based on your activity
              </p>
            </Card>
          </div>
        </div>
      </div>
    );
  }

  // Connected state - show normal dashboard
  return (
    <div className="flex h-full flex-col p-8">
      <div className="w-full max-w-7xl mx-auto space-y-8">
        
        {/* Header Section */}
        <div className="space-y-2">
          <h1 className="text-4xl font-bold tracking-tight">
            GitHub <span className="text-primary">Integration</span>
          </h1>
          <p className="text-lg text-muted-foreground">
            View and manage your GitHub activity data
          </p>
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column - Status */}
          <div className="lg:col-span-1">
            <GitHubDataStatus />
          </div>

          {/* Right Column - Activity */}
          <div className="lg:col-span-2">
            <GitHubActivity />
          </div>
        </div>

        {/* Info Section */}
        <div className="p-6 bg-card border border-border rounded-lg">
          <h3 className="font-semibold text-foreground mb-3 flex items-center gap-2">
            <span className="text-primary">💡</span>
            How it works
          </h3>
          <ul className="text-sm text-muted-foreground space-y-2">
            <li className="flex items-start gap-2">
              <span className="text-primary mt-0.5">•</span>
              <span>Your GitHub commits are fetched and stored securely</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-primary mt-0.5">•</span>
              <span>Data refreshes automatically when older than 24 hours</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-primary mt-0.5">•</span>
              <span>Only new commits are fetched to save API calls</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-primary mt-0.5">•</span>
              <span>This data will be used to generate personalized content</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}

