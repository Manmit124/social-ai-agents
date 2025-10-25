"use client";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Twitter, CheckCircle2, XCircle } from "lucide-react";
import { useConnections, type Connection } from "@/hooks/api/useConnections";

interface ConnectedAccountProps {
  connection: Connection;
}

export function ConnectedAccount({ connection }: ConnectedAccountProps) {
  const { disconnectAccount } = useConnections();

  const handleDisconnect = () => {
    if (confirm(`Are you sure you want to disconnect ${connection.platform}?`)) {
      disconnectAccount.mutate(connection.platform);
    }
  };

  const getIcon = () => {
    switch (connection.platform) {
      case "twitter":
        return <Twitter className="h-5 w-5" />;
      default:
        return null;
    }
  };

  const getPlatformName = () => {
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




