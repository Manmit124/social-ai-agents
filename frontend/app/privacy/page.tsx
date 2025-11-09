"use client";

import Link from "next/link";

export default function PrivacyPolicyPage() {
  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-16 max-w-4xl">
        <h1 className="text-4xl font-bold mb-8">Privacy Policy</h1>
        <p className="text-sm text-muted-foreground mb-8">Last updated: {new Date().toLocaleDateString()}</p>

        <div className="prose prose-slate dark:prose-invert max-w-none space-y-6">
          <section>
            <h2 className="text-2xl font-semibold mb-4">1. Introduction</h2>
            <p className="text-muted-foreground mb-4">
              Welcome to Mataroo ("we," "our," or "us"). We are committed to protecting your privacy and ensuring the security of your personal information. This Privacy Policy explains how we collect, use, store, and protect your data when you use our AI-powered social media content generation service.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-4">2. Information We Collect</h2>
            <div className="space-y-4">
              <div>
                <h3 className="text-xl font-semibold mb-2">2.1 Personal Information</h3>
                <ul className="list-disc pl-6 space-y-2 text-muted-foreground">
                  <li>Name and email address (collected during account registration)</li>
                  <li>Payment information (processed securely through Razorpay - we do not store your payment card details)</li>
                  <li>Account credentials for connected social media platforms (Twitter/X, GitHub)</li>
                </ul>
              </div>
              <div>
                <h3 className="text-xl font-semibold mb-2">2.2 Usage Data</h3>
                <ul className="list-disc pl-6 space-y-2 text-muted-foreground">
                  <li>Content generated and posted through our service</li>
                  <li>Post history and analytics</li>
                  <li>Platform usage patterns and preferences</li>
                </ul>
              </div>
              <div>
                <h3 className="text-xl font-semibold mb-2">2.3 Technical Data</h3>
                <ul className="list-disc pl-6 space-y-2 text-muted-foreground">
                  <li>IP address and device information</li>
                  <li>Browser type and version</li>
                  <li>Cookies and similar tracking technologies</li>
                </ul>
              </div>
            </div>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-4">3. How We Use Your Information</h2>
            <p className="text-muted-foreground mb-4">We use your information to:</p>
            <ul className="list-disc pl-6 space-y-2 text-muted-foreground">
              <li>Provide and improve our AI-powered content generation service</li>
              <li>Process payments and manage subscriptions</li>
              <li>Personalize content using RAG (Retrieval Augmented Generation) based on your GitHub commits and writing style</li>
              <li>Connect and post to your social media accounts (Twitter/X)</li>
              <li>Send service-related communications and updates</li>
              <li>Ensure platform security and prevent fraud</li>
              <li>Comply with legal obligations</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-4">4. Data Storage and Security</h2>
            <p className="text-muted-foreground mb-4">
              We implement industry-standard security measures to protect your data:
            </p>
            <ul className="list-disc pl-6 space-y-2 text-muted-foreground">
              <li>Data is encrypted in transit and at rest</li>
              <li>Access to personal data is restricted to authorized personnel only</li>
              <li>Regular security audits and updates</li>
              <li>Secure authentication and authorization protocols</li>
            </ul>
            <p className="text-muted-foreground mt-4">
              Your data is stored on secure servers. We retain your data only as long as necessary to provide our services or as required by law.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-4">5. Third-Party Processors</h2>
            <p className="text-muted-foreground mb-4">
              We use trusted third-party services to operate our platform:
            </p>
            <ul className="list-disc pl-6 space-y-2 text-muted-foreground">
              <li><strong>Razorpay:</strong> Payments are processed securely via Razorpay. We do not store your payment card details. Razorpay's privacy policy applies to payment transactions.</li>
              <li><strong>Supabase:</strong> Database and authentication services</li>
              <li><strong>Google Gemini:</strong> AI content generation and embeddings</li>
              <li><strong>Twitter/X API:</strong> For posting content to your connected accounts</li>
              <li><strong>GitHub API:</strong> For accessing your commits to personalize content</li>
            </ul>
            <p className="text-muted-foreground mt-4">
              These third parties are contractually obligated to protect your data and use it only for the purposes we specify.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-4">6. Cookies</h2>
            <p className="text-muted-foreground mb-4">
              We use cookies and similar technologies to:
            </p>
            <ul className="list-disc pl-6 space-y-2 text-muted-foreground">
              <li>Maintain your session and authentication state</li>
              <li>Remember your preferences</li>
              <li>Analyze platform usage and improve our service</li>
            </ul>
            <p className="text-muted-foreground mt-4">
              You can control cookies through your browser settings, but disabling cookies may affect platform functionality.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-4">7. Your Rights</h2>
            <p className="text-muted-foreground mb-4">You have the right to:</p>
            <ul className="list-disc pl-6 space-y-2 text-muted-foreground">
              <li>Access your personal data</li>
              <li>Correct inaccurate data</li>
              <li>Request deletion of your data</li>
              <li>Export your data</li>
              <li>Withdraw consent for data processing</li>
              <li>Disconnect your social media accounts at any time</li>
            </ul>
            <p className="text-muted-foreground mt-4">
              To exercise these rights, please contact us at <a href="mailto:manmittiwade124@gmail.com" className="text-primary hover:underline">manmittiwade124@gmail.com</a>.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-4">8. Data Retention</h2>
            <p className="text-muted-foreground">
              We retain your personal data for as long as your account is active or as needed to provide our services. If you delete your account, we will delete or anonymize your data within 30 days, except where we are required to retain it for legal or regulatory purposes.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-4">9. Children's Privacy</h2>
            <p className="text-muted-foreground">
              Our service is not intended for users under 18 years of age. We do not knowingly collect personal information from children. If you believe we have collected information from a child, please contact us immediately.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-4">10. Changes to This Policy</h2>
            <p className="text-muted-foreground">
              We may update this Privacy Policy from time to time. We will notify you of any material changes by posting the new policy on this page and updating the "Last updated" date. Your continued use of our service after changes become effective constitutes acceptance of the updated policy.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-4">11. Contact Us</h2>
            <p className="text-muted-foreground mb-4">
              If you have questions, concerns, or requests regarding this Privacy Policy or your personal data, please contact us:
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

