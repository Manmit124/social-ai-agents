import { TweetGenerator } from '@/components/TweetGenerator';

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-background to-muted">
      <div className="container mx-auto px-4 py-8 max-w-3xl">
        <div className="mb-8 text-center">
          <h1 className="text-4xl font-bold mb-2">AI Tweet Generator</h1>
          <p className="text-muted-foreground">
            Powered by Gemini & LangGraph
          </p>
        </div>
        
        <TweetGenerator />
      </div>
    </main>
  );
}


