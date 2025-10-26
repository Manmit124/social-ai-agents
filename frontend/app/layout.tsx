import type { Metadata } from "next"
import { Inter } from "next/font/google"
import "./globals.css"
import { AuthProvider } from "@/components/auth/AuthProvider"
import { JsonLd } from "./schema"

const inter = Inter({ subsets: ["latin"] })

export const metadata: Metadata = {
  title: {
    default: "Mataru.ai - AI-Powered Social Media Content Generator",
    template: "%s | Mataru.ai"
  },
  description: "Generate and post engaging content across X, LinkedIn, and Reddit using AI agents. Automate your social media with Mataru.ai - powered by LangGraph and Google Gemini.",
  keywords: [
    "AI social media generator",
    "automated content posting",
    "X content generator",
    "AI post generator",
    "social media automation",
    "LangGraph",
    "Google Gemini AI",
    "OAuth social media",
    "multi-platform posting",
    "AI content creation",
    "Mataru.ai"
  ],
  authors: [{ name: "Mataru.ai Team" }],
  creator: "Mataru.ai",
  publisher: "Mataru.ai",
  applicationName: "Mataru.ai",
  metadataBase: new URL(process.env.NEXT_PUBLIC_APP_URL || "http://localhost:3000"),
  openGraph: {
    type: "website",
    locale: "en_US",
    url: "/",
    title: "Mataru.ai - AI-Powered Social Media Content Generator",
    description: "Generate and post engaging content across social media platforms using AI agents. Automate your X, LinkedIn, and Reddit posts with intelligent AI.",
    siteName: "Mataru.ai",
    images: [
      {
        url: "/favicon_io/android-chrome-512x512.png",
        width: 512,
        height: 512,
        alt: "Mataru.ai Logo"
      }
    ]
  },
  twitter: {
    card: "summary_large_image",
    title: "Mataru.ai - AI-Powered Social Media Content Generator",
    description: "Generate and post engaging content across social media platforms using AI agents. Automate your social media with intelligent AI.",
    images: ["/favicon_io/android-chrome-512x512.png"],
    creator: "@mataruai"
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-video-preview": -1,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },
  icons: {
    icon: [
      { url: "/favicon_io/favicon-16x16.png", sizes: "16x16", type: "image/png" },
      { url: "/favicon_io/favicon-32x32.png", sizes: "32x32", type: "image/png" },
      { url: "/favicon_io/favicon.ico" },
    ],
    apple: [
      { url: "/favicon_io/apple-touch-icon.png", sizes: "180x180", type: "image/png" },
    ],
    other: [
      { url: "/favicon_io/android-chrome-192x192.png", sizes: "192x192", type: "image/png" },
      { url: "/favicon_io/android-chrome-512x512.png", sizes: "512x512", type: "image/png" },
    ],
  },
  manifest: "/favicon_io/site.webmanifest",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" className="dark">
      <head>
        <JsonLd />
      </head>
      <body className={inter.className}>
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  )
}


