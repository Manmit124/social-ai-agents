"use client";

import Link from "next/link";

export default function TermsPage() {
  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-16 max-w-4xl">
        <h1 className="text-4xl font-bold mb-8">Terms & Conditions</h1>
        <p className="text-sm text-muted-foreground mb-8">Last updated: {new Date().toLocaleDateString()}</p>

        <div className="prose prose-slate dark:prose-invert max-w-none space-y-6">
          <section>
            <h2 className="text-2xl font-semibold mb-4">1. Agreement to Terms</h2>
            <p className="text-muted-foreground mb-4">
              By accessing or using Mataroo ("the Service"), you agree to be bound by these Terms & Conditions ("Terms"). If you disagree with any part of these terms, you may not access the Service.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-4">2. Service Description</h2>
            <p className="text-muted-foreground mb-4">
              Mataroo is an AI-powered social media content generation and posting platform that:
            </p>
            <ul className="list-disc pl-6 space-y-2 text-muted-foreground">
              <li>Generates social media content using AI (powered by Google Gemini)</li>
              <li>Personalizes content using RAG (Retrieval Augmented Generation) based on your GitHub commits and writing style</li>
              <li>Posts content to your connected social media accounts (currently Twitter/X)</li>
              <li>Provides content history and analytics</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-4">3. User Accounts</h2>
            <div className="space-y-4">
              <p className="text-muted-foreground">
                To use our Service, you must:
              </p>
              <ul className="list-disc pl-6 space-y-2 text-muted-foreground">
                <li>Be at least 18 years old</li>
                <li>Provide accurate and complete registration information</li>
                <li>Maintain the security of your account credentials</li>
                <li>Notify us immediately of any unauthorized access</li>
                <li>Be responsible for all activities under your account</li>
              </ul>
            </div>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-4">4. Subscription Plans</h2>
            <div className="space-y-4">
              <div>
                <h3 className="text-xl font-semibold mb-2">4.1 Free Plan</h3>
                <ul className="list-disc pl-6 space-y-2 text-muted-foreground">
                  <li>5 posts per month</li>
                  <li>30-day post history</li>
                  <li>All core features included</li>
                </ul>
              </div>
              <div>
                <h3 className="text-xl font-semibold mb-2">4.2 Pro Plan</h3>
                <ul className="list-disc pl-6 space-y-2 text-muted-foreground">
                  <li>Unlimited posts per month</li>
                  <li>Unlimited post history</li>
                  <li>Email support</li>
                  <li>Billed monthly at $5/month (or equivalent in INR)</li>
                </ul>
              </div>
              <p className="text-muted-foreground mt-4">
                <strong>Payments:</strong> All payments are processed securely via Razorpay. By subscribing to Pro, you agree to Razorpay's payment terms and conditions.
              </p>
            </div>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-4">5. Payment Terms</h2>
            <ul className="list-disc pl-6 space-y-2 text-muted-foreground">
              <li>Pro subscriptions are billed monthly in advance</li>
              <li>Payments are processed through Razorpay</li>
              <li>You authorize us to charge your payment method for recurring subscriptions</li>
              <li>If payment fails, your subscription may be suspended or cancelled</li>
              <li>All fees are non-refundable once the subscription period has started, except as stated in our Refund Policy</li>
              <li>We reserve the right to change pricing with 30 days' notice</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-4">6. Acceptable Use</h2>
            <p className="text-muted-foreground mb-4">You agree not to:</p>
            <ul className="list-disc pl-6 space-y-2 text-muted-foreground">
              <li>Use the Service for illegal or unauthorized purposes</li>
              <li>Generate or post content that is harmful, abusive, defamatory, or violates any laws</li>
              <li>Impersonate others or misrepresent your identity</li>
              <li>Attempt to gain unauthorized access to the Service or other accounts</li>
              <li>Interfere with or disrupt the Service or servers</li>
              <li>Use automated systems to access the Service without permission</li>
              <li>Reverse engineer or attempt to extract source code</li>
              <li>Share your account credentials with others</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-4">7. Content and Intellectual Property</h2>
            <div className="space-y-4">
              <div>
                <h3 className="text-xl font-semibold mb-2">7.1 Your Content</h3>
                <p className="text-muted-foreground">
                  You retain ownership of content you generate and post through our Service. By using the Service, you grant us a license to use, store, and process your content to provide and improve our services.
                </p>
              </div>
              <div>
                <h3 className="text-xl font-semibold mb-2">7.2 Our Intellectual Property</h3>
                <p className="text-muted-foreground">
                  The Service, including its design, features, and AI technology, is owned by Mataroo and protected by intellectual property laws. You may not copy, modify, or distribute any part of the Service without our written permission.
                </p>
              </div>
            </div>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-4">8. Third-Party Services</h2>
            <p className="text-muted-foreground mb-4">
              Our Service integrates with third-party platforms:
            </p>
            <ul className="list-disc pl-6 space-y-2 text-muted-foreground">
              <li><strong>Twitter/X:</strong> For posting content. You must comply with Twitter's Terms of Service.</li>
              <li><strong>GitHub:</strong> For accessing your commits for personalization. You must comply with GitHub's Terms of Service.</li>
              <li><strong>Razorpay:</strong> For payment processing. Payment transactions are subject to Razorpay's terms.</li>
            </ul>
            <p className="text-muted-foreground mt-4">
              We are not responsible for the policies or practices of third-party services.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-4">9. Service Availability</h2>
            <p className="text-muted-foreground">
              We strive to maintain high availability but do not guarantee uninterrupted or error-free service. We may perform maintenance, updates, or modifications that temporarily affect service availability. We are not liable for any downtime or service interruptions.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-4">10. Limitation of Liability</h2>
            <p className="text-muted-foreground mb-4">
              To the maximum extent permitted by law:
            </p>
            <ul className="list-disc pl-6 space-y-2 text-muted-foreground">
              <li>The Service is provided "as is" without warranties of any kind</li>
              <li>We are not liable for any indirect, incidental, or consequential damages</li>
              <li>Our total liability is limited to the amount you paid us in the 12 months preceding the claim</li>
              <li>We are not responsible for content generated by AI that may be inaccurate or inappropriate</li>
              <li>You are responsible for reviewing and approving all content before posting</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-4">11. Termination</h2>
            <div className="space-y-4">
              <p className="text-muted-foreground">
                <strong>By You:</strong> You may cancel your subscription at any time. Cancellation takes effect at the end of your current billing period.
              </p>
              <p className="text-muted-foreground">
                <strong>By Us:</strong> We may suspend or terminate your account if you violate these Terms, engage in fraudulent activity, or for any other reason with or without notice.
              </p>
              <p className="text-muted-foreground">
                Upon termination, your access to the Service will cease, and we may delete your data in accordance with our Privacy Policy.
              </p>
            </div>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-4">12. Dispute Resolution</h2>
            <p className="text-muted-foreground mb-4">
              Any disputes arising from these Terms or the Service shall be resolved through:
            </p>
            <ul className="list-disc pl-6 space-y-2 text-muted-foreground">
              <li>First, contact us at <a href="mailto:manmittiwade124@gmail.com" className="text-primary hover:underline">manmittiwade124@gmail.com</a> to attempt resolution</li>
              <li>If unresolved, disputes shall be subject to the exclusive jurisdiction of courts in Nagpur, India</li>
              <li>Indian law shall govern these Terms</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-4">13. Changes to Terms</h2>
            <p className="text-muted-foreground">
              We reserve the right to modify these Terms at any time. We will notify you of material changes by posting the updated Terms on this page and updating the "Last updated" date. Your continued use of the Service after changes become effective constitutes acceptance of the updated Terms.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-4">14. Contact Information</h2>
            <p className="text-muted-foreground mb-4">
              For questions about these Terms, please contact us:
            </p>
            <div className="bg-muted p-4 rounded-lg">
              <p className="text-muted-foreground mb-2"><strong>Email:</strong> <a href="mailto:manmittiwade124@gmail.com" className="text-primary hover:underline">manmittiwade124@gmail.com</a></p>
              <p className="text-muted-foreground"><strong>Address:</strong> Flat no.303 Mangaldeep Apartment, Bhamti Nagar, Sainath Nagar, Trimurtee Nagar, Near NIT garden, Nagpur - 440022, India</p>
            </div>
          </section>
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
      </div>
    </div>
  );
}

