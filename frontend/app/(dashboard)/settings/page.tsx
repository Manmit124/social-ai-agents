"use client";

import { useAuth } from "@/hooks/auth/useAuth";
import { User, Mail, Settings as SettingsIcon } from "lucide-react";

export default function SettingsPage() {
  const { user } = useAuth();

  return (
    <div className="flex h-full flex-col items-center p-8">
      <div className="w-full max-w-3xl mx-auto space-y-12">
        
        {/* Header - Centered */}
        <div className="text-center space-y-3">
          <div className="flex items-center justify-center gap-3 mb-4">
            <SettingsIcon className="h-10 w-10 text-primary" />
          </div>
          <h1 className="text-4xl font-bold tracking-tight">Settings</h1>
          <p className="text-lg text-muted-foreground">
            Manage your account and preferences
          </p>
        </div>

        {/* Account Section */}
        <div className="space-y-6">
          <div className="rounded-2xl border-2 bg-card/80 backdrop-blur-sm p-8 shadow-lg">
            <div className="flex items-center gap-3 mb-6">
              <User className="h-6 w-6 text-primary" />
              <h2 className="text-2xl font-semibold">Account Information</h2>
            </div>
            
            <div className="space-y-4">
              <div className="flex items-center gap-4 rounded-xl bg-muted/50 p-5">
                <Mail className="h-5 w-5 text-muted-foreground" />
                <div className="flex-1">
                  <p className="text-sm font-medium text-muted-foreground mb-1">Email Address</p>
                  <p className="text-base font-medium">{user?.email}</p>
                </div>
              </div>
              
              <div className="rounded-xl bg-primary/5 border border-primary/20 p-5">
                <p className="text-sm text-muted-foreground text-center">
                  ✨ More settings and customization options coming soon!
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

