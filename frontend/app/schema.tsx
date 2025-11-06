export function JsonLd() {
  const schema = {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": "Mataroo.com",
    "applicationCategory": "BusinessApplication",
    "operatingSystem": "Web",
    "offers": {
      "@type": "Offer",
      "price": "0",
      "priceCurrency": "USD"
    },
    "description": "AI-powered social media content generator. Automate your X, LinkedIn, and Reddit posts with intelligent AI agents powered by LangGraph and Google Gemini.",
    "featureList": [
      "AI-powered content generation",
      "Multi-platform posting (X, LinkedIn, Reddit)",
      "OAuth 2.0 integration",
      "Real-time content preview",
      "Post history tracking",
      "Automated hashtag generation"
    ],
    "screenshot": "/favicon_io/android-chrome-512x512.png",
    "aggregateRating": {
      "@type": "AggregateRating",
      "ratingValue": "5",
      "ratingCount": "1"
    }
  };

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schema) }}
    />
  );
}

