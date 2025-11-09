"use client";

import Link from "next/link";

export default function RefundPolicyPage() {
  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-16 max-w-4xl">
        <h1 className="text-4xl font-bold mb-8">Refund & Return Policy</h1>
        <p className="text-sm text-muted-foreground mb-8">Last updated: {new Date().toLocaleDateString()}</p>

        <div className="prose prose-slate dark:prose-invert max-w-none space-y-6">
          <section>
            <h2 className="text-2xl font-semibold mb-4">1. Overview</h2>
            <p className="text-muted-foreground mb-4">
              At Mataroo, we want you to be satisfied with your subscription. This Refund Policy outlines the terms and conditions for refunds of Pro subscription payments.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-4">2. Refund Eligibility</h2>
            <div className="space-y-4">
              <div>
                <h3 className="text-xl font-semibold mb-2">2.1 7-Day Refund Window</h3>
                <p className="text-muted-foreground mb-2">
                  You are eligible for a full refund if:
                </p>
                <ul className="list-disc pl-6 space-y-2 text-muted-foreground">
                  <li>You request a refund within 7 days of your payment</li>
                  <li>The subscription has not been activated or added to your account</li>
                  <li>You have not used any Pro features (unlimited posts) during the subscription period</li>
                </ul>
              </div>
              <div>
                <h3 className="text-xl font-semibold mb-2">2.2 No Refund After Activation</h3>
                <p className="text-muted-foreground">
                  Once your Pro subscription is activated and added to your account, and you have started using Pro features (such as posting unlimited content), refunds are not available. This includes:
                </p>
                <ul className="list-disc pl-6 space-y-2 text-muted-foreground mt-2">
                  <li>Subscriptions that have been active for more than 7 days</li>
                  <li>Subscriptions where Pro features have been used</li>
                  <li>Subscriptions that have been renewed for a new billing period</li>
                </ul>
              </div>
            </div>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-4">3. How to Request a Refund</h2>
            <p className="text-muted-foreground mb-4">
              To request a refund, please:
            </p>
            <ol className="list-decimal pl-6 space-y-2 text-muted-foreground">
              <li>Send an email to <a href="mailto:manmittiwade124@gmail.com" className="text-primary hover:underline">manmittiwade124@gmail.com</a> with the subject "Refund Request"</li>
              <li>Include your account email address and payment transaction ID (from Razorpay)</li>
              <li>Explain the reason for your refund request</li>
              <li>Provide proof of payment if requested</li>
            </ol>
            <p className="text-muted-foreground mt-4">
              We will review your request and respond within 5-7 business days.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-4">4. Refund Processing</h2>
            <div className="space-y-4">
              <div>
                <h3 className="text-xl font-semibold mb-2">4.1 Processing Time</h3>
                <p className="text-muted-foreground">
                  Once your refund request is approved, we will process the refund within 5-10 business days. The refund will be credited to your original payment method through Razorpay.
                </p>
              </div>
              <div>
                <h3 className="text-xl font-semibold mb-2">4.2 Refund Method</h3>
                <p className="text-muted-foreground">
                  Refunds will be processed to the same payment method used for the original transaction. If the original payment method is no longer available, we will contact you to arrange an alternative refund method.
                </p>
              </div>
              <div>
                <h3 className="text-xl font-semibold mb-2">4.3 Refund Amount</h3>
                <p className="text-muted-foreground">
                  Eligible refunds will be for the full amount paid. No partial refunds are available once the subscription is activated.
                </p>
              </div>
            </div>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-4">5. Non-Refundable Items</h2>
            <p className="text-muted-foreground mb-4">
              The following are not eligible for refunds:
            </p>
            <ul className="list-disc pl-6 space-y-2 text-muted-foreground">
              <li>Subscriptions that have been active for more than 7 days</li>
              <li>Subscriptions where Pro features have been used</li>
              <li>Free plan usage (no payment made)</li>
              <li>Any fees charged by payment processors (Razorpay) are non-refundable</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-4">6. Cancellation vs. Refund</h2>
            <div className="space-y-4">
              <p className="text-muted-foreground">
                <strong>Cancellation:</strong> You can cancel your Pro subscription at any time. Cancellation prevents future charges but does not entitle you to a refund for the current billing period.
              </p>
              <p className="text-muted-foreground">
                <strong>Refund:</strong> A refund is only available within the 7-day window and if the subscription has not been activated, as described in Section 2.
              </p>
            </div>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-4">7. Disputes and Chargebacks</h2>
            <p className="text-muted-foreground mb-4">
              If you have a dispute regarding a charge or believe there was an error in billing:
            </p>
            <ul className="list-disc pl-6 space-y-2 text-muted-foreground">
              <li>Contact us first at <a href="mailto:manmittiwade124@gmail.com" className="text-primary hover:underline">manmittiwade124@gmail.com</a> before initiating a chargeback</li>
              <li>We will work with you to resolve the issue promptly</li>
              <li>Chargebacks may result in account suspension or termination</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-4">8. Payment Processor</h2>
            <p className="text-muted-foreground">
              All payments are processed securely through Razorpay. Refund processing times and methods are subject to Razorpay's policies and your bank's processing times. We are not responsible for delays in refund processing beyond our control.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-4">9. Changes to This Policy</h2>
            <p className="text-muted-foreground">
              We reserve the right to modify this Refund Policy at any time. Changes will be posted on this page with an updated "Last updated" date. Continued use of our Service after changes constitutes acceptance of the updated policy.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold mb-4">10. Contact for Refund Requests</h2>
            <p className="text-muted-foreground mb-4">
              For refund requests or questions about this policy, please contact us:
            </p>
            <div className="bg-muted p-4 rounded-lg">
              <p className="text-muted-foreground mb-2"><strong>Email:</strong> <a href="mailto:manmittiwade124@gmail.com" className="text-primary hover:underline">manmittiwade124@gmail.com</a></p>
              <p className="text-muted-foreground mb-2"><strong>Subject:</strong> Refund Request</p>
              <p className="text-muted-foreground"><strong>Address:</strong> Flat no.303 Mangaldeep Apartment, Bhamti Nagar, Sainath Nagar, Trimurtee Nagar, Near NIT garden, Nagpur - 440022, India</p>
            </div>
            <p className="text-muted-foreground mt-4">
              We aim to respond to all refund requests within 5-7 business days.
            </p>
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

