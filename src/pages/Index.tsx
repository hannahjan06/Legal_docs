import { useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { mockAuth } from '@/lib/auth';
import { MessageSquare, FileText, BarChart3, LogIn, UserPlus } from 'lucide-react';

const Index = () => {
  const navigate = useNavigate();

  useEffect(() => {
    // Redirect to dashboard if already authenticated
    if (mockAuth.isAuthenticated()) {
      navigate('/dashboard');
    }
  }, [navigate]);

  const features = [
    {
      icon: FileText,
      title: 'PDF Analysis',
      description: 'Upload and analyze PDF documents with AI-powered extraction'
    },
    {
      icon: MessageSquare,
      title: 'Smart Summarization',
      description: 'Get intelligent summaries and key insights from your documents'
    },
    {
      icon: BarChart3,
      title: 'Flowchart Generation',
      description: 'Create visual flowcharts from process descriptions automatically'
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-warm">
      {/* Hero Section */}
      <div className="relative overflow-hidden">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <div className="text-center">
            <div className="flex justify-center mb-8">
              <div className="w-16 h-16 bg-gradient-primary rounded-2xl flex items-center justify-center shadow-large">
                <MessageSquare className="w-8 h-8 text-primary-foreground" />
              </div>
            </div>
            
            <h1 className="text-4xl md:text-6xl font-bold mb-6">
              <span className="bg-gradient-primary bg-clip-text text-transparent">
                AI Document Assistant
              </span>
            </h1>
            
            <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
              Transform your PDF documents with intelligent analysis, summarization, 
              and flowchart generation powered by advanced AI agents.
            </p>

            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Button 
                asChild
                size="lg"
                className="bg-gradient-primary hover:opacity-90 transition-all duration-200 shadow-medium"
              >
                <Link to="/signup">
                  <UserPlus className="w-5 h-5 mr-2" />
                  Get Started Free
                </Link>
              </Button>
              
              <Button 
                asChild
                variant="outline" 
                size="lg"
                className="hover:shadow-soft transition-all duration-200"
              >
                <Link to="/login">
                  <LogIn className="w-5 h-5 mr-2" />
                  Sign In
                </Link>
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold mb-4">Powerful AI Agents</h2>
          <p className="text-muted-foreground max-w-2xl mx-auto">
            Our specialized AI agents work together to provide comprehensive document analysis
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          {features.map((feature, index) => {
            const Icon = feature.icon;
            return (
              <Card key={index} className="shadow-medium hover:shadow-large transition-all duration-300 bg-gradient-card">
                <CardHeader className="text-center pb-4">
                  <div className="w-12 h-12 bg-gradient-primary rounded-xl flex items-center justify-center mx-auto mb-4 shadow-soft">
                    <Icon className="w-6 h-6 text-primary-foreground" />
                  </div>
                  <CardTitle className="text-xl">{feature.title}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-muted-foreground text-center leading-relaxed">
                    {feature.description}
                  </p>
                </CardContent>
              </Card>
            );
          })}
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-card border-t border-border">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className="text-center">
            <h2 className="text-3xl font-bold mb-4">Ready to get started?</h2>
            <p className="text-muted-foreground mb-8">
              Join thousands of users who trust our AI-powered document analysis
            </p>
            <Button 
              asChild
              size="lg"
              className="bg-gradient-primary hover:opacity-90 transition-all duration-200 shadow-medium"
            >
              <Link to="/signup">
                Create Your Account
              </Link>
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Index;