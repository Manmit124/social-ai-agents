"use client";

import { useSubscription } from "@/hooks/api/useSubscription";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { CheckCircle2, Crown, AlertCircle } from "lucide-react";
import { useRouter } from "next/navigation";
import Link from "next/link";

export function SubscriptionStatus() {
  const { data, isLoading } = useSubscription();
  const router = useRouter();

  if (isLoading) {
    return (
      <Card>
        <CardContent className="p-6">
          <div className="animate-pulse">
            <div className="h-4 bg-muted rounded w-1/4 mb-2"></div>
            <div className="h-8 bg-muted rounded w-1/2"></div>
          </div>
        </CardContent>
      </Card>
    );
  }

  const subscription = data?.subscription;
  if (!subscription) return null;

  const isPro = subscription.plan_type === "pro";
  const postsUsed = subscription.posts_used || 0;
  const postsLimit = subscription.posts_limit || 5;
  const remaining = subscription.remaining;
  const isUnlimited = remaining === "unlimited" || postsLimit === -1;
  const usagePercentage = isUnlimited ? 0 : (postsUsed / postsLimit) * 100;
  const isNearLimit = !isUnlimited && postsUsed >= postsLimit * 0.8;
  const isAtLimit = !isUnlimited && postsUsed >= postsLimit;

  return (
    <Card className={isPro ? "border-primary" : ""}>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            {isPro ? (
              <Crown className="h-5 w-5 text-primary" />
            ) : (
              <CheckCircle2 className="h-5 w-5 text-muted-foreground" />
            )}
            <CardTitle className="text-lg">
              {isPro ? "Pro Plan" : "Free Plan"}
            </CardTitle>
          </div>
          {isPro && (
            <span className="text-xs bg-primary/10 text-primary px-2 py-1 rounded-full">
              Active
            </span>
          )}
        </div>
        <CardDescription>
          {isPro 
            ? "Unlimited posts and advanced features" 
            : "5 posts per month included"}
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {!isPro && (
          <div className="space-y-2">
            <div className="flex items-center justify-between text-sm">
              <span className="text-muted-foreground">Posts used this month</span>
              <span className="font-medium">
                {postsUsed} / {postsLimit}
              </span>
            </div>
            <div className="w-full bg-muted rounded-full h-2">
              <div
                className={`h-2 rounded-full transition-all ${
                  isAtLimit
                    ? "bg-destructive"
                    : isNearLimit
                    ? "bg-orange-500"
                    : "bg-primary"
                }`}
                style={{ width: `${Math.min(usagePercentage, 100)}%` }}
              />
            </div>
            {isAtLimit && (
              <div className="flex items-center gap-2 text-sm text-destructive">
                <AlertCircle className="h-4 w-4" />
                <span>You've reached your monthly limit. Upgrade to Pro for unlimited posts.</span>
              </div>
            )}
            {isNearLimit && !isAtLimit && (
              <div className="flex items-center gap-2 text-sm text-orange-500">
                <AlertCircle className="h-4 w-4" />
                <span>You're running low on posts. Upgrade to Pro for unlimited posts.</span>
              </div>
            )}
          </div>
        )}

        {isPro && (
          <div className="flex items-center gap-2 text-sm text-primary">
            <CheckCircle2 className="h-4 w-4" />
            <span>Unlimited posts available</span>
          </div>
        )}

        {!isPro && (
          <Link href="/#pricing">
            <Button className="w-full" variant={isAtLimit ? "default" : "outline"}>
              {isAtLimit ? "Upgrade to Pro" : "Upgrade for Unlimited Posts"}
            </Button>
          </Link>
        )}

        {isPro && (
          <div className="text-xs text-muted-foreground text-center">
            Pro subscription active. Manage your subscription in settings.
          </div>
        )}
      </CardContent>
    </Card>
  );
}

