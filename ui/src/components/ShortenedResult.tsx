import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Copy, CheckCheck } from "lucide-react";
import { useState } from "react";

interface ShortenedResultProps {
  shortUrl: string;
  handleReset: () => void;
}

const ShortenedResult = ({ shortUrl, handleReset }: ShortenedResultProps) => {
  const [copied, setCopied] = useState<boolean>(false);
  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(shortUrl);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error("Failed to copy:", err);
    }
  };

  return (
    <div className="space-y-4 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="h-px bg-linear-to-r from-transparent via-gray-300 to-transparent" />

      <div className="space-y-2">
        <Label
          htmlFor="short-url"
          className="text-sm font-medium text-green-700">
        </Label>
        <div className="flex gap-2">
          <Input
            id="short-url"
            type="text"
            value={shortUrl}
            readOnly
            className="h-12 text-base font-medium bg-green-50 border-green-200"/>
          <Button
            type="button"
            variant="outline"
            size="icon"
            className="h-12 w-12 border-green-200 hover:bg-green-50"
            onClick={handleCopy}>
            {copied ? (
              <CheckCheck className="w-5 h-5 text-green-600" />) : (<Copy className="w-5 h-5" />)}
          </Button>
        </div>
      </div>

      <div className="flex gap-2">
        <Button
          type="button"
          variant="outline"
          className="flex-1"
          onClick={() => window.open(shortUrl, "_blank")}>
          Open Link
        </Button>
        <Button
          type="button"
          variant="outline"
          className="flex-1"
          onClick={handleReset}>
          Shorten Another
        </Button>
      </div>
    </div>
  );
};

export default ShortenedResult;
