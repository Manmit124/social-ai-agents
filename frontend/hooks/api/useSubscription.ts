"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { api } from "@/lib/api";

interface Subscription {
  plan_type: "free" | "pro";
  status: "active" | "cancelled" | "expired";
  posts_used: number;
  posts_limit: number;
  remaining: number | "unlimited";
  current_period_end?: string;
}

interface SubscriptionResponse {
  success: boolean;
  subscription: Subscription;
}

// Get subscription status
export function useSubscription() {
  return useQuery<SubscriptionResponse>({
    queryKey: ["subscription"],
    queryFn: async () => {
      const response = await api.get("/api/subscription/status");
      return response;
    },
    refetchOnWindowFocus: true,
  });
}

// Create payment order
export function useCreateOrder() {
  return useMutation({
    mutationFn: async () => {
      const response = await api.post("/api/payments/create-order");
      return response;
    },
  });
}

// Verify payment
export function useVerifyPayment() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (paymentData: {
      razorpay_order_id: string;
      razorpay_payment_id: string;
      razorpay_signature: string;
    }) => {
      const response = await api.post("/api/payments/verify", paymentData);
      return response;
    },
    onSuccess: () => {
      // Refetch subscription status after successful payment
      queryClient.invalidateQueries({ queryKey: ["subscription"] });
    },
  });
}

