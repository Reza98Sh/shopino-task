
import { Card, CardContent } from "@/components/ui/card";
import Header from "./components/Header";
import ShortenerForm from "./components/ShortenerForm";
import ShortenedResult from "./components/ShortenedResult";
import { useUrlShortener } from "./hooks/useUrlShortener";
import "./App.css";

function App() {
  const {
    error,
    longUrl,
    loading,
    shortUrl,

    setLongUrl,
    handleReset,
    handleSubmit,
  } = useUrlShortener();

  return (
    <div className="min-h-screen bg-blue-50 flex items-center justify-center p-4">
      <Card className="w-full max-w-2xl shadow-2xl">
        <Header />
        <CardContent className="space-y-6">
         {!shortUrl && <ShortenerForm
            longUrl={longUrl}
            setLongUrl={setLongUrl}
            loading={loading}
            error={error}
            handleSubmit={handleSubmit}
          />}
          {shortUrl && (
            <ShortenedResult
              shortUrl={shortUrl}
              handleReset={handleReset}
            />
          )}
        </CardContent>
      </Card>
    </div>
  );
}

export default App;
