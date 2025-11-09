"use client";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Mail, MapPin, MessageSquare } from "lucide-react";

export default function ContactPage() {
  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-16 max-w-4xl">
        <h1 className="text-4xl font-bold mb-4">Contact Us</h1>
        <p className="text-muted-foreground mb-12">
          Have questions, need support, or want to get in touch? We're here to help.
        </p>

        <div className="grid md:grid-cols-2 gap-8 mb-12">
          {/* Email Card */}
          <Card>
            <CardHeader>
              <div className="flex items-center gap-3 mb-2">
                <Mail className="h-6 w-6 text-primary" />
                <CardTitle>Email Support</CardTitle>
              </div>
              <CardDescription>
                Send us an email and we'll get back to you as soon as possible
              </CardDescription>
            </CardHeader>
            <CardContent>
              <a 
                href="mailto:manmittiwade124@gmail.com" 
                className="text-primary hover:underline font-medium"
              >
                manmittiwade124@gmail.com
              </a>
              <p className="text-sm text-muted-foreground mt-2">
                Response time: Within 24-48 hours
              </p>
            </CardContent>
          </Card>

          {/* Address Card */}
          <Card>
            <CardHeader>
              <div className="flex items-center gap-3 mb-2">
                <MapPin className="h-6 w-6 text-primary" />
                <CardTitle>Registered Address</CardTitle>
              </div>
              <CardDescription>
                Our business location
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-muted-foreground">
                Flat no.303 Mangaldeep Apartment<br />
                Bhamti Nagar, Sainath Nagar<br />
                Trimurtee Nagar, Near NIT garden<br />
                Nagpur - 440022<br />
                India
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Support Information */}
        <Card>
          <CardHeader>
            <div className="flex items-center gap-3 mb-2">
              <MessageSquare className="h-6 w-6 text-primary" />
              <CardTitle>Customer Support</CardTitle>
            </div>
            <CardDescription>
              How to reach us for different types of inquiries
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <h3 className="font-semibold mb-2">General Inquiries</h3>
              <p className="text-sm text-muted-foreground">
                For general questions about Mataroo, our services, or features, email us at{" "}
                <a href="mailto:manmittiwade124@gmail.com" className="text-primary hover:underline">
                  manmittiwade124@gmail.com
                </a>
              </p>
            </div>
            <div>
              <h3 className="font-semibold mb-2">Technical Support</h3>
              <p className="text-sm text-muted-foreground">
                Pro plan subscribers receive priority email support. Free plan users can contact us for general assistance.
              </p>
            </div>
            <div>
              <h3 className="font-semibold mb-2">Billing & Refunds</h3>
              <p className="text-sm text-muted-foreground">
                For payment issues, refund requests, or subscription questions, email us with "Billing" or "Refund Request" in the subject line.
              </p>
            </div>
            <div>
              <h3 className="font-semibold mb-2">Privacy & Data Requests</h3>
              <p className="text-sm text-muted-foreground">
                For privacy concerns, data access requests, or account deletion requests, email us with "Privacy" in the subject line.
              </p>
            </div>
            <div>
              <h3 className="font-semibold mb-2">Customer Grievances</h3>
              <p className="text-sm text-muted-foreground">
                If you have a complaint or grievance, please contact us at{" "}
                <a href="mailto:manmittiwade124@gmail.com" className="text-primary hover:underline">
                  manmittiwade124@gmail.com
                </a>{" "}
                with "Grievance" in the subject line. We will address your concern within 5-7 business days.
              </p>
            </div>
          </CardContent>
        </Card>

        {/* Quick Actions */}
        <div className="mt-8 space-y-4">
          <h2 className="text-2xl font-semibold mb-4">Quick Links</h2>
          <div className="grid md:grid-cols-3 gap-4">
            <a href="/pricing">
              <Button variant="outline" className="w-full">
                View Pricing
              </Button>
            </a>
            <a href="/privacy">
              <Button variant="outline" className="w-full">
                Privacy Policy
              </Button>
            </a>
            <a href="/terms">
              <Button variant="outline" className="w-full">
                Terms & Conditions
              </Button>
            </a>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="mt-0">
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
                    <a href="/privacy" className="text-gray-400 hover:text-white transition-colors">
                      Privacy Policy
                    </a>
                  </li>
                  <li>
                    <a href="/terms" className="text-gray-400 hover:text-white transition-colors">
                      Terms & Conditions
                    </a>
                  </li>
                  <li>
                    <a href="/refund" className="text-gray-400 hover:text-white transition-colors">
                      Refund Policy
                    </a>
                  </li>
                </ul>
              </div>
              <div>
                <h3 className="font-semibold mb-4 text-white">Support</h3>
                <ul className="space-y-2 text-sm">
                  <li>
                    <a href="/contact" className="text-gray-400 hover:text-white transition-colors">
                      Contact Us
                    </a>
                  </li>
                  <li>
                    <a href="/pricing" className="text-gray-400 hover:text-white transition-colors">
                      Pricing
                    </a>
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
    </div>
  );
}

