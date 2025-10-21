"use client";

import { Button } from "@/components/ui/button";
import { Twitter } from "lucide-react";
import { useConnections } from "@/hooks/api/useConnections";

export function ConnectTwitter() {
  const { connectTwitter, isConnected } = useConnections();

  const handleConnect = () => {
    connectTwitter.mutate();
  };

  const isTwitterConnected = isConnected("twitter");

  if (isTwitterConnected) {
    return null; // Don't show button if already connected
  }

  return (
    <Button
      onClick={handleConnect}
      disabled={connectTwitter.isPending}
      className="w-full"
    >
      <Twitter className="mr-2 h-4 w-4" />
      {connectTwitter.isPending ? "Connecting..." : "Connect Twitter"}
    </Button>
  );
}

