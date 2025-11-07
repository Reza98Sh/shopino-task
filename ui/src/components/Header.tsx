
import { CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Link2 } from 'lucide-react';

const Header = () => (
  <CardHeader dir='rtl' className="text-center space-y-2">
    <div className="flex justify-center mb-2">
      <div className="bg-indigo-600 p-3 rounded-full">
        <Link2 className="w-8 h-8 text-white" />
      </div>
    </div>
    <CardTitle className="text-3xl font-bold text-gray-800">
      سرویس کوتاه کننده لینک
    </CardTitle>
    <CardDescription className="text-base">
      لینک های بلند را به لینک های کوتاه قابل اشتراک گذاری تبدیل کنید.
    </CardDescription>
  </CardHeader>
);

export default Header;
