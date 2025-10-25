"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/hooks/auth/useAuth";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import Logo from "@/components/logo/logo";

export default function Home() {
  const router = useRouter();
  const { user, isLoading } = useAuth();

  useEffect(() => {
    if (!isLoading && user) {
      router.push("/dashboard");
    }
  }, [user, isLoading, router]);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="mt-4 text-muted-foreground">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <main className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        <div className="mb-8 text-center">
          <div className="flex justify-center mb-4">
            <Logo className="w-24 h-24" />
          </div>
          <h1 className="text-4xl font-bold mb-2 text-foreground">
            Mataru.ai
          </h1>
          <p className="text-muted-foreground">
            AI-Powered Social Media Content Generator
          </p>
        </div>
        
        <div className="grid gap-6 md:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle>Welcome to Mataru.ai</CardTitle>
              <CardDescription>
                Generate and post engaging content using AI agents with multi-platform support
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <h3 className="font-semibold">Features:</h3>
                <ul className="text-sm text-muted-foreground space-y-1">
                  <li>• AI-powered content generation</li>
                  <li>• Multi-platform posting (Twitter, LinkedIn, Reddit)</li>
                  <li>• OAuth 2.0 integration</li>
                  <li>• Real-time content preview</li>
                  <li>• Post history tracking</li>
                </ul>
              </div>
              <div className="flex space-x-2">
                <Button asChild>
                  <Link href="/login">Sign In</Link>
                </Button>
                <Button variant="outline" asChild>
                  <Link href="/signup">Sign Up</Link>
                </Button>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>How it works</CardTitle>
              <CardDescription>
                Simple steps to get started
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-start space-x-3">
                  <div className="flex-shrink-0 w-6 h-6 bg-primary/10 text-primary rounded-full flex items-center justify-center text-sm font-semibold">
                    1
                  </div>
                  <div>
                    <h4 className="font-medium">Connect your accounts</h4>
                    <p className="text-sm text-muted-foreground">Link your social media accounts securely</p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <div className="flex-shrink-0 w-6 h-6 bg-primary/10 text-primary rounded-full flex items-center justify-center text-sm font-semibold">
                    2
                  </div>
                  <div>
                    <h4 className="font-medium">Generate content</h4>
                    <p className="text-sm text-muted-foreground">AI creates platform-specific content</p>
                  </div>
                </div>
                <div className="flex items-start space-x-3">
                  <div className="flex-shrink-0 w-6 h-6 bg-primary/10 text-primary rounded-full flex items-center justify-center text-sm font-semibold">
                    3
                  </div>
                  <div>
                    <h4 className="font-medium">Post & track</h4>
                    <p className="text-sm text-muted-foreground">Publish and monitor your posts</p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </main>
  );
}


