import { Button } from '@/components/ui/button';
import { mockAuth } from '@/lib/auth';
import { useNavigate } from 'react-router-dom';
import { useToast } from '@/hooks/use-toast';
import { LogOut, MessageSquare } from 'lucide-react';

const Navbar = () => {
  const navigate = useNavigate();
  const { toast } = useToast();
  const user = mockAuth.getCurrentUser();

  const handleLogout = () => {
    mockAuth.logout();
    toast({
      title: "Signed out successfully",
      description: "Thanks for using AI Chat Assistant!",
    });
    navigate('/login');
  };

  return (
    <nav className="bg-card border-b border-border shadow-soft">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo */}
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-primary rounded-lg flex items-center justify-center shadow-soft">
              <MessageSquare className="w-5 h-5 text-primary-foreground" />
            </div>
            <span className="text-xl font-bold bg-gradient-primary bg-clip-text text-transparent">
              AI Assistant
            </span>
          </div>

          {/* User info and logout */}
          <div className="flex items-center space-x-4">
            {user && (
              <div className="hidden sm:block">
                <span className="text-sm text-muted-foreground">Welcome, </span>
                <span className="text-sm font-medium text-foreground">{user.name}</span>
              </div>
            )}
            <Button 
              variant="outline" 
              size="sm"
              onClick={handleLogout}
              className="hover:shadow-soft transition-all duration-200"
            >
              <LogOut className="w-4 h-4 mr-2" />
              Logout
            </Button>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;