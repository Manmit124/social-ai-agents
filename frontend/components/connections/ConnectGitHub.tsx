"use client";

import { Button } from "@/components/ui/button";
import { useConnections } from "@/hooks/api/useConnections";
import { Github } from "lucide-react";

export function ConnectGitHub() {
  const { connectGitHub, isConnected } = useConnections();

  const handleConnect = () => {
    connectGitHub.mutate();
  };

  const isGitHubConnected = isConnected("github");

  if (isGitHubConnected) {
    return null; // Don't show button if already connected
  }

  return (
    <Button
      onClick={handleConnect}
      disabled={connectGitHub.isPending}
      className="w-full"
    >
      <Github className="mr-2 h-4 w-4" />
      {connectGitHub.isPending ? "Connecting..." : "Connect GitHub"}
    </Button>
  );
}


