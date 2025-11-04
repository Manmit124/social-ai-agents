"use client";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { CheckCircle2, XCircle } from "lucide-react";
import { useConnections, type Connection } from "@/hooks/api/useConnections";
import { XIcon } from "@/components/icons/XIcon";

interface ConnectedAccountProps {
  connection: Connection;
}

export function ConnectedAccount({ connection }: ConnectedAccountProps) {
  const { disconnectAccount } = useConnections();

  const handleDisconnect = () => {
    const platformName = connection.platform === "twitter" ? "X" : connection.platform;
    
    // Special warning for GitHub with data deletion info
    if (connection.platform === "github") {
      const confirmed = confirm(
        `⚠️ Disconnect GitHub?\n\n` +
        `This will permanently delete:\n` +
        `• All stored commits\n` +
        `• AI insights and analysis\n` +
        `• Activity statistics\n` +
        `• User context data\n\n` +
        `You'll need to re-fetch and re-analyze data if you reconnect.\n\n` +
        `Continue with disconnect?`
      );
      
      if (confirmed) {
        disconnectAccount.mutate(connection.platform);
      }
    } else {
      // Standard confirmation for other platforms
      if (confirm(`Are you sure you want to disconnect ${platformName}?`)) {
        disconnectAccount.mutate(connection.platform);
      }
    }
  };

  const getIcon = () => {
    switch (connection.platform) {
      case "twitter":
        return <XIcon className="h-5 w-5" />;
      default:
        return null;
    }
  };

  const getPlatformName = () => {
    if (connection.platform === "twitter") return "X";
    return connection.platform.charAt(0).toUpperCase() + connection.platform.slice(1);
  };

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            {getIcon()}
            <CardTitle>{getPlatformName()}</CardTitle>
          </div>
          {connection.is_active ? (
            <CheckCircle2 className="h-5 w-5 text-primary" />
          ) : (
            <XCircle className="h-5 w-5 text-destructive" />
          )}
        </div>
        <CardDescription>
          {connection.platform_username ? `@${connection.platform_username}` : "Connected"}
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="flex items-center justify-between">
          <div className="text-sm text-muted-foreground">
            {connection.connected_at && (
              <p>Connected {new Date(connection.connected_at).toLocaleDateString()}</p>
            )}
          </div>
          <Button
            variant="destructive"
            size="sm"
            onClick={handleDisconnect}
            disabled={disconnectAccount.isPending}
          >
            {disconnectAccount.isPending ? "Disconnecting..." : "Disconnect"}
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}




