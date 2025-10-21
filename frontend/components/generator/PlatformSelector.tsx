"use client";

import { Twitter, Linkedin, MessageCircle } from "lucide-react";
import { cn } from "@/lib/utils";
import { useConnections } from "@/hooks/api/useConnections";

export type Platform = "twitter" | "linkedin" | "reddit";

interface PlatformOption {
  id: Platform;
  name: string;
  icon: React.ComponentType<{ className?: string }>;
  color: string;
  bgColor: string;
  available: boolean;
}

interface PlatformSelectorProps {
  selected: Platform;
  onSelect: (platform: Platform) => void;
}

export function PlatformSelector({ selected, onSelect }: PlatformSelectorProps) {
  const { isConnected } = useConnections();

  const platforms: PlatformOption[] = [
    {
      id: "twitter",
      name: "Twitter",
      icon: Twitter,
      color: "text-blue-500",
      bgColor: "bg-blue-500/10 hover:bg-blue-500/20",
      available: isConnected("twitter"),
    },
    {
      id: "linkedin",
      name: "LinkedIn",
      icon: Linkedin,
      color: "text-blue-700",
      bgColor: "bg-blue-700/10 hover:bg-blue-700/20",
      available: false, // Phase 2
    },
    {
      id: "reddit",
      name: "Reddit",
      icon: MessageCircle,
      color: "text-orange-500",
      bgColor: "bg-orange-500/10 hover:bg-orange-500/20",
      available: false, // Phase 3
    },
  ];

  return (
    <div className="space-y-2">
      <label className="text-sm font-medium text-foreground">
        Select Platform
      </label>
      <div className="grid grid-cols-3 gap-3">
        {platforms.map((platform) => {
          const Icon = platform.icon;
          const isSelected = selected === platform.id;
          const isDisabled = !platform.available;

          return (
            <button
              key={platform.id}
              onClick={() => !isDisabled && onSelect(platform.id)}
              disabled={isDisabled}
              className={cn(
                "relative flex flex-col items-center justify-center gap-2 rounded-lg border-2 p-4 transition-all",
                isSelected
                  ? "border-primary bg-primary/5 shadow-sm"
                  : isDisabled
                  ? "border-border bg-muted cursor-not-allowed opacity-50"
                  : "border-border hover:border-primary/50",
                !isDisabled && "cursor-pointer"
              )}
            >
              <Icon
                className={cn(
                  "h-6 w-6",
                  isSelected ? "text-primary" : isDisabled ? "text-muted-foreground" : platform.color
                )}
              />
              <span
                className={cn(
                  "text-sm font-medium",
                  isSelected ? "text-primary" : isDisabled ? "text-muted-foreground" : "text-foreground"
                )}
              >
                {platform.name}
              </span>
              {isDisabled && (
                <span className="absolute top-1 right-1 rounded-full bg-muted px-2 py-0.5 text-xs text-muted-foreground">
                  Soon
                </span>
              )}
              {!isDisabled && !isSelected && (
                <span className="absolute top-1 right-1 h-2 w-2 rounded-full bg-green-500" />
              )}
            </button>
          );
        })}
      </div>
      {!isConnected(selected) && (
        <p className="text-sm text-destructive">
          Please connect your {selected.charAt(0).toUpperCase() + selected.slice(1)} account in Settings first.
        </p>
      )}
    </div>
  );
}

