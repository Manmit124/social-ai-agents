/**
 * Data Sources Page
 * 
 * Overview of all connected data sources
 */

'use client';

import React from 'react';
import Link from 'next/link';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Github, Twitter, ArrowRight, CheckCircle2, Clock } from 'lucide-react';
import { useConnections } from '@/hooks/api/useConnections';

export default function DataPage() {
  const { isConnected, isLoading } = useConnections();
  
  const isGitHubConnected = isConnected('github');
  const isTwitterConnected = isConnected('twitter');

  const dataSources = [
    {
      id: 'github',
      name: 'GitHub',
      description: 'Connect your GitHub account to fetch commits and generate content based on your coding activity',
      icon: Github,
      href: '/data/github',
      isConnected: isGitHubConnected,
      isAvailable: true,
      color: 'text-primary',
      bgColor: 'bg-primary/10',
      stats: isGitHubConnected ? ['Commits tracked', 'Repositories synced', 'Auto-refresh enabled'] : [],
    },
    {
      id: 'twitter',
      name: 'Twitter',
      description: 'Connect your Twitter account to analyze your tweets and engagement metrics',
      icon: Twitter,
      href: '/data/twitter',
      isConnected: isTwitterConnected,
      isAvailable: true, // Now available!
      color: 'text-primary',
      bgColor: 'bg-primary/10',
      stats: isTwitterConnected ? ['Tweets analyzed', 'Style profile generated', 'Engagement tracked'] : [],
    },
  ];

  if (isLoading) {
    return (
      <div className="flex h-full flex-col p-8">
        <div className="w-full max-w-6xl mx-auto space-y-8">
          <div className="space-y-2">
            <div className="h-10 bg-muted rounded w-1/3 animate-pulse"></div>
            <div className="h-6 bg-muted rounded w-1/2 animate-pulse"></div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-full flex-col p-8">
      <div className="w-full max-w-6xl mx-auto space-y-8">
        
        {/* Header Section */}
        <div className="space-y-2">
          <h1 className="text-4xl font-bold tracking-tight">
            Data <span className="text-primary">Sources</span>
          </h1>
          <p className="text-lg text-muted-foreground">
            Connect and manage your data sources for personalized content generation
          </p>
        </div>

        {/* Data Sources Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {dataSources.map((source) => {
            const Icon = source.icon;
            
            return (
              <Card 
                key={source.id} 
                className="p-8 border-border hover:border-primary/50 transition-all duration-200 relative overflow-hidden group"
              >
                {/* Background decoration */}
                <div className="absolute top-0 right-0 w-32 h-32 bg-primary/5 rounded-full blur-3xl group-hover:bg-primary/10 transition-all duration-300"></div>
                
                <div className="relative space-y-6">
                  {/* Header */}
                  <div className="flex items-start justify-between">
                    <div className="flex items-center gap-4">
                      <div className={`${source.bgColor} p-4 rounded-xl`}>
                        <Icon className={`w-8 h-8 ${source.color}`} />
                      </div>
                      <div>
                        <h3 className="text-2xl font-bold text-foreground">{source.name}</h3>
                        {source.isConnected && (
                          <div className="flex items-center gap-1 mt-1">
                            <CheckCircle2 className="w-4 h-4 text-primary" />
                            <span className="text-sm text-primary font-medium">Connected</span>
                          </div>
                        )}
                        {!source.isAvailable && (
                          <div className="flex items-center gap-1 mt-1">
                            <Clock className="w-4 h-4 text-muted-foreground" />
                            <span className="text-sm text-muted-foreground font-medium">Coming Soon</span>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>

                  {/* Description */}
                  <p className="text-muted-foreground">
                    {source.description}
                  </p>

                  {/* Stats */}
                  {source.stats.length > 0 && (
                    <div className="flex flex-wrap gap-2">
                      {source.stats.map((stat, index) => (
                        <span
                          key={index}
                          className="px-3 py-1 bg-muted text-muted-foreground rounded-full text-xs font-medium"
                        >
                          {stat}
                        </span>
                      ))}
                    </div>
                  )}

                  {/* Action Button */}
                  <div className="pt-2">
                    {source.isAvailable ? (
                      <Link href={source.href}>
                        <Button 
                          variant={source.isConnected ? "outline" : "default"}
                          className="w-full group/btn"
                        >
                          {source.isConnected ? 'Manage Data' : 'Connect Now'}
                          <ArrowRight className="ml-2 h-4 w-4 group-hover/btn:translate-x-1 transition-transform" />
                        </Button>
                      </Link>
                    ) : (
                      <Button 
                        variant="outline"
                        disabled
                        className="w-full"
                      >
                        Coming Soon
                      </Button>
                    )}
                  </div>
                </div>
              </Card>
            );
          })}
        </div>

        {/* Info Section */}
        <div className="p-6 bg-card border border-border rounded-lg">
          <h3 className="font-semibold text-foreground mb-3 flex items-center gap-2">
            <span className="text-primary">💡</span>
            Why connect data sources?
          </h3>
          <ul className="text-sm text-muted-foreground space-y-2">
            <li className="flex items-start gap-2">
              <span className="text-primary mt-0.5">•</span>
              <span>Generate personalized content based on your real activity and achievements</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-primary mt-0.5">•</span>
              <span>AI analyzes your data to create authentic and engaging posts</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-primary mt-0.5">•</span>
              <span>All data is stored securely and only used for your content generation</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-primary mt-0.5">•</span>
              <span>Smart refresh ensures your data is always up-to-date without wasting API calls</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}

