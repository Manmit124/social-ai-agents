"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useAuth } from "@/hooks/auth/useAuth";
import { cn } from "@/lib/utils";
import Logo from "@/components/logo/logo";
import { 
  MessageSquare, 
  PlusCircle, 
  History, 
  Settings,
  LogOut,
  Twitter,
  Sparkles,
  Puzzle
} from "lucide-react";

const navigation = [
  { name: "Generate Tweet", href: "/dashboard", icon: Sparkles },
  { name: "Apps", href: "/apps", icon: Puzzle },
  { name: "History", href: "/history", icon: History },
  { name: "Settings", href: "/settings", icon: Settings },
];

export function Sidebar() {
  const pathname = usePathname();
  const { logout, isLoggingOut, user } = useAuth();

  return (
    <div className="flex h-screen w-20 flex-col items-center border-r bg-sidebar py-6">
      {/* Logo */}
      <Link href="/dashboard" className="mb-8">
        <div className="flex items-center justify-center hover:opacity-80 transition-opacity">
          <Logo  />
        </div>
      </Link>

      {/* Navigation */}
      <nav className="flex flex-1 flex-col items-center space-y-4">
        {navigation.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.name}
              href={item.href}
              className={cn(
                "group flex h-12 w-12 items-center justify-center rounded-xl transition-all duration-200",
                isActive
                  ? "bg-sidebar-accent text-sidebar-accent-foreground"
                  : "text-muted-foreground hover:bg-sidebar-accent hover:text-sidebar-accent-foreground"
              )}
              title={item.name}
            >
              <item.icon className="h-5 w-5" />
            </Link>
          );
        })}
      </nav>

      {/* User Profile & Logout */}
      <div className="flex flex-col items-center space-y-4">
        <button
          onClick={() => logout()}
          disabled={isLoggingOut}
          className="group flex h-12 w-12 items-center justify-center rounded-xl text-muted-foreground transition-all duration-200 hover:bg-destructive/10 hover:text-destructive"
          title="Logout"
        >
          <LogOut className="h-5 w-5" />
        </button>
        
        {/* User Avatar */}
        <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary text-sm font-semibold text-primary-foreground shadow-lg">
          {user?.email?.charAt(0).toUpperCase() || "U"}
        </div>
      </div>
    </div>
  );
}

