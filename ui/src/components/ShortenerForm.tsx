
import type { FormEvent } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';

interface ShortenerFormProps {
  longUrl: string;
  setLongUrl: (value: string) => void;
  loading: boolean;
  error: string;
  handleSubmit: (e: FormEvent) => void;
}

const ShortenerForm = ({
  longUrl,
  setLongUrl,
  loading,
  error,
  handleSubmit,
}: ShortenerFormProps) => (
  <form onSubmit={handleSubmit} className="space-y-4">
    <div className="space-y-2">
      <Label dir='rtl'  htmlFor="long-url" className="text-sm font-medium">
        لینک خود را وارد کنید:
      </Label>
      <Input
        id="long-url"
        type="url"
        placeholder="https://example.com/very/long/url/path"
        value={longUrl}
        onChange={(e) => setLongUrl(e.target.value)}
        required
        className="h-12 text-base"
        disabled={loading}
      />
    </div>

    {error && (
      <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
        {error}
      </div>
    )}

    <Button
      type="submit"
      className="w-full h-12 text-base font-semibold bg-indigo-600 hover:bg-indigo-700"
      disabled={loading || !longUrl}
    >
      {loading ? (
        <span className="flex items-center gap-2">
          <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin" />
          در حال کوتاه کردن...
        </span>
      ) : (
        'کوتاه کن'
      )}
    </Button>
  </form>
);

export default ShortenerForm;
