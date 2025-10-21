"use client";

import { useAuth } from "@/hooks/auth/useAuth";
import { useConnections } from "@/hooks/api/useConnections";
import { Settings, User, Twitter, Bell } from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { ConnectTwitter } from "@/components/connections/ConnectTwitter";
import { ConnectedAccount } from "@/components/connections/ConnectedAccount";

export default function SettingsPage() {
  const { user } = useAuth();
  const { connections, isLoading } = useConnections();

  return (
    <div className="flex h-full flex-col p-8">
      <div className="mb-8">
        <h1 className="mb-2 text-3xl font-bold text-foreground">Settings</h1>
        <p className="text-muted-foreground">Manage your account and preferences</p>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <div className="flex items-center space-x-2">
              <User className="h-5 w-5 text-primary" />
              <CardTitle>Account</CardTitle>
            </div>
            <CardDescription>
              Your account information
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-2">
              <div>
                <p className="text-sm text-muted-foreground">Email</p>
                <p className="text-foreground">{user?.email}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <div className="flex items-center space-x-2">
              <Twitter className="h-5 w-5 text-primary" />
              <CardTitle>Connected Accounts</CardTitle>
            </div>
            <CardDescription>
              Manage your social media connections
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            {isLoading ? (
              <p className="text-sm text-muted-foreground">Loading connections...</p>
            ) : connections && connections.length > 0 ? (
              <>
                <div className="space-y-4">
                  {connections.map((connection) => (
                    <ConnectedAccount key={connection.platform} connection={connection} />
                  ))}
                </div>
                {!connections.some(c => c.platform === "twitter") && (
                  <ConnectTwitter />
                )}
              </>
            ) : (
              <div className="space-y-4">
                <p className="text-sm text-muted-foreground">
                  No accounts connected yet
                </p>
                <ConnectTwitter />
              </div>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <div className="flex items-center space-x-2">
              <Bell className="h-5 w-5 text-primary" />
              <CardTitle>Notifications</CardTitle>
            </div>
            <CardDescription>
              Configure your notification preferences
            </CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              Notification settings coming soon
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <div className="flex items-center space-x-2">
              <Settings className="h-5 w-5 text-primary" />
              <CardTitle>Preferences</CardTitle>
            </div>
            <CardDescription>
              Customize your experience
            </CardDescription>
          </CardHeader>
          <CardContent>
            <p className="text-sm text-muted-foreground">
              Preference settings coming soon
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}

