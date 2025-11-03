/**
 * Twitter Data Page
 * 
 * Coming Soon - Twitter integration
 */

'use client';

import React from 'react';
import Link from 'next/link';
import { Card } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Twitter, ArrowLeft, Sparkles, BarChart3, TrendingUp, Users } from 'lucide-react';

export default function TwitterDataPage() {
  return (
    <div className="flex h-full flex-col items-center justify-center p-8">
      <div className="w-full max-w-3xl mx-auto space-y-8">
        
        {/* Back Button */}
        <Link href="/data">
          <Button variant="ghost" className="gap-2">
            <ArrowLeft className="w-4 h-4" />
            Back to Data Sources
          </Button>
        </Link>

        {/* Hero Card */}
        <Card className="p-12 border-border text-center space-y-6">
          <div className="flex justify-center">
            <div className="relative">
              <div className="absolute inset-0 bg-primary/20 rounded-full blur-3xl animate-pulse"></div>
              <div className="relative bg-primary/10 p-6 rounded-full">
                <Twitter className="w-16 h-16 text-primary" />
              </div>
            </div>
          </div>

          <div className="space-y-3">
            <h1 className="text-4xl font-bold tracking-tight">
              Twitter <span className="text-primary">Integration</span>
            </h1>
            <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 border border-primary/20">
              <Sparkles className="w-4 h-4 text-primary" />
              <span className="text-sm text-primary font-medium">Coming Soon</span>
            </div>
            <p className="text-lg text-muted-foreground max-w-xl mx-auto pt-2">
              We're working on bringing Twitter data integration to help you analyze your tweets, 
              engagement metrics, and generate even better content based on what resonates with your audience.
            </p>
          </div>
        </Card>

        {/* Planned Features */}
        <div className="space-y-4">
          <h2 className="text-xl font-semibold text-foreground text-center">
            Planned Features
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Card className="p-6 border-border space-y-3">
              <div className="flex items-center gap-3">
                <div className="bg-primary/10 p-3 rounded-lg">
                  <BarChart3 className="w-5 h-5 text-primary" />
                </div>
                <h3 className="font-semibold text-foreground">Tweet Analytics</h3>
              </div>
              <p className="text-sm text-muted-foreground">
                Track your tweet performance, engagement rates, and identify what content works best
              </p>
            </Card>

            <Card className="p-6 border-border space-y-3">
              <div className="flex items-center gap-3">
                <div className="bg-primary/10 p-3 rounded-lg">
                  <TrendingUp className="w-5 h-5 text-primary" />
                </div>
                <h3 className="font-semibold text-foreground">Trending Topics</h3>
              </div>
              <p className="text-sm text-muted-foreground">
                Discover trending topics in your niche and get AI suggestions for timely content
              </p>
            </Card>

            <Card className="p-6 border-border space-y-3">
              <div className="flex items-center gap-3">
                <div className="bg-primary/10 p-3 rounded-lg">
                  <Users className="w-5 h-5 text-primary" />
                </div>
                <h3 className="font-semibold text-foreground">Audience Insights</h3>
              </div>
              <p className="text-sm text-muted-foreground">
                Understand your audience better with detailed analytics and engagement patterns
              </p>
            </Card>

            <Card className="p-6 border-border space-y-3">
              <div className="flex items-center gap-3">
                <div className="bg-primary/10 p-3 rounded-lg">
                  <Sparkles className="w-5 h-5 text-primary" />
                </div>
                <h3 className="font-semibold text-foreground">Smart Suggestions</h3>
              </div>
              <p className="text-sm text-muted-foreground">
                Get AI-powered content suggestions based on your past successful tweets
              </p>
            </Card>
          </div>
        </div>

        {/* Notify Section */}
        <Card className="p-6 bg-muted/50 border-border text-center space-y-3">
          <p className="text-sm text-muted-foreground">
            Want to be notified when Twitter integration is ready?
          </p>
          <p className="text-xs text-muted-foreground">
            We'll send you an email as soon as this feature launches!
          </p>
        </Card>
      </div>
    </div>
  );
}

