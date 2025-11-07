
import { useState } from 'react';

export interface ShortenResponse {
  short_url: string;
  original_url: string;
}

export function useUrlShortener() {
  const [longUrl, setLongUrl] = useState<string>('');
  const [shortUrl, setShortUrl] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string>('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setShortUrl('');
    setLoading(true);

    try {
      const response = await fetch('/api/long-url', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: longUrl }),
      });

      if (!response.ok) {
        throw new Error('Failed to shorten URL');
      }

      const data: ShortenResponse = await response.json();
      setShortUrl(data.short_url);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setLongUrl('');
    setShortUrl('');
    setError('');
  };

  return {
    longUrl,
    setLongUrl,
    shortUrl,
    loading,
    error,
    handleSubmit,
    handleReset,
  };
}
