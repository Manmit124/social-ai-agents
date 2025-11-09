"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/hooks/auth/useAuth";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import Logo from "@/components/logo/logo";
import { Sparkles, Zap, Shield, TrendingUp, ArrowRight, Twitter, Linkedin, MessageSquare } from "lucide-react";

export default function Home() {
  const router = useRouter();
  const { user, isLoading } = useAuth();

  useEffect(() => {
    if (!isLoading && user) {
      router.push("/dashboard");
    }
  }, [user, isLoading, router]);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto"></div>
          <p className="mt-4 text-muted-foreground">Loading...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-background via-primary/5 to-background">
      {/* Animated Background Elements */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-1/4 left-1/4 w-[600px] h-[600px] bg-primary/20 rounded-full blur-3xl animate-pulse"></div>
        <div className="absolute bottom-1/4 right-1/4 w-[500px] h-[500px] bg-primary/25 rounded-full blur-3xl animate-pulse delay-1000"></div>
        <div className="absolute top-1/2 left-1/2 w-[400px] h-[400px] bg-primary/15 rounded-full blur-3xl animate-pulse delay-2000"></div>
        <div className="absolute top-3/4 left-1/3 w-[300px] h-[300px] bg-orange-500/20 rounded-full blur-3xl animate-pulse delay-1000"></div>
      </div>

      {/* Navigation */}
      <nav className="relative z-10 border-b border-border backdrop-blur-sm bg-background/80">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <span className="text-xl font-bold text-foreground">
                Mataroo
              </span>
            </div>
            <div className="flex items-center gap-4">
              <Link href="/pricing" className="text-sm font-medium text-muted-foreground hover:text-foreground transition-colors">
                Pricing
              </Link>
              <Link href="/login">
                <Button variant="ghost">
                  Sign In
                </Button>
              </Link>
              <Link href="/signup">
                <Button>
                  Get Started
                </Button>
              </Link>
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative z-10 container mx-auto px-4 pt-20 pb-32">
        <div className="text-center max-w-5xl mx-auto">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 border border-primary/20 mb-8 animate-fade-in">
            <Sparkles className="w-4 h-4 text-primary" />
            <span className="text-sm text-primary">AI-Powered Social Media Automation</span>
          </div>
          
          <h1 className="text-5xl md:text-7xl font-bold text-foreground mb-6 leading-tight animate-slide-up">
            Transform Your Social Media
            <span className="block text-primary mt-2">
              With AI Agents
            </span>
          </h1>
          
          <p className="text-xl text-muted-foreground mb-10 max-w-3xl mx-auto animate-slide-up delay-100">
            Generate engaging content and post across X, LinkedIn, and Reddit automatically. 
            Let AI handle your social media while you focus on what matters.
          </p>
          
          <div className="flex flex-wrap gap-4 justify-center animate-slide-up delay-200">
            <Link href="/signup">
              <Button size="lg" className="text-lg px-8 py-6 rounded-full shadow-lg hover-scale">
                Start Free Trial
                <ArrowRight className="ml-2 h-5 w-5" />
              </Button>
            </Link>
            <Link href="/dashboard">
              <Button size="lg" variant="outline" className="text-lg px-8 py-6 rounded-full hover-scale">
                View Demo
              </Button>
            </Link>
          </div>

          {/* Social Platform Icons */}
          <div className="flex items-center justify-center gap-8 mt-16 animate-fade-in delay-300">
            <div className="flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors">
              <Twitter className="w-6 h-6" />
              <span>X (Twitter)</span>
            </div>
            <div className="flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors">
              <Linkedin className="w-6 h-6" />
              <span>LinkedIn</span>
            </div>
            <div className="flex items-center gap-2 text-muted-foreground hover:text-foreground transition-colors">
              <MessageSquare className="w-6 h-6" />
              <span>Reddit</span>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="relative z-10 mt-0">
        {/* Black Section - Footer Content */}
        <div className="bg-black py-8">
          <div className="container mx-auto px-4">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
              <div>
                <h3 className="font-semibold mb-4 text-white">Mataroo</h3>
                <p className="text-sm text-gray-400">
                  AI-powered social media content generation and posting platform.
                </p>
              </div>
              <div>
                <h3 className="font-semibold mb-4 text-white">Legal</h3>
                <ul className="space-y-2 text-sm">
                  <li>
                    <Link href="/privacy" className="text-gray-400 hover:text-white transition-colors">
                      Privacy Policy
                    </Link>
                  </li>
                  <li>
                    <Link href="/terms" className="text-gray-400 hover:text-white transition-colors">
                      Terms & Conditions
                    </Link>
                  </li>
                  <li>
                    <Link href="/refund" className="text-gray-400 hover:text-white transition-colors">
                      Refund Policy
                    </Link>
                  </li>
                </ul>
              </div>
              <div>
                <h3 className="font-semibold mb-4 text-white">Support</h3>
                <ul className="space-y-2 text-sm">
                  <li>
                    <Link href="/contact" className="text-gray-400 hover:text-white transition-colors">
                      Contact Us
                    </Link>
                  </li>
                  <li>
                    <Link href="/pricing" className="text-gray-400 hover:text-white transition-colors">
                      Pricing
                    </Link>
                  </li>
                </ul>
              </div>
              <div>
                <h3 className="font-semibold mb-4 text-white">Contact</h3>
                <ul className="space-y-2 text-sm">
                  <li>
                    <a href="mailto:manmittiwade124@gmail.com" className="text-gray-400 hover:text-white transition-colors">
                      manmittiwade124@gmail.com
                    </a>
                  </li>
                </ul>
              </div>
            </div>
            <div className="border-t border-gray-800 pt-8 text-center text-sm text-gray-400">
              <p>&copy; {new Date().getFullYear()} Mataroo. All rights reserved.</p>
            </div>
          </div>
        </div>
      </footer>

      <style jsx global>{`
        @keyframes fade-in {
          from { opacity: 0; }
          to { opacity: 1; }
        }
        @keyframes slide-up {
          from { 
            opacity: 0;
            transform: translateY(30px);
          }
          to { 
            opacity: 1;
            transform: translateY(0);
          }
        }
        .animate-fade-in {
          animation: fade-in 1s ease-out;
        }
        .animate-slide-up {
          animation: slide-up 0.8s ease-out;
        }
        .delay-100 {
          animation-delay: 0.1s;
          animation-fill-mode: both;
        }
        .delay-200 {
          animation-delay: 0.2s;
          animation-fill-mode: both;
        }
        .delay-300 {
          animation-delay: 0.3s;
          animation-fill-mode: both;
        }
        .delay-1000 {
          animation-delay: 1s;
        }
        .delay-2000 {
          animation-delay: 2s;
        }
      `}</style>
    </div>
  );
}


