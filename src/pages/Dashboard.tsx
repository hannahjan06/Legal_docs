import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { mockAuth } from '@/lib/auth';
import Navbar from '@/components/Navbar';
import Sidebar from '@/components/Sidebar';
import ChatInterface from '@/components/ChatInterface';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { FileText, Settings, BarChart3 } from 'lucide-react';

const Dashboard = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const navigate = useNavigate();

  useEffect(() => {
    // Check authentication on component mount
    if (!mockAuth.isAuthenticated()) {
      navigate('/login');
    }
  }, [navigate]);

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <ChatInterface />;
      
      case 'documents':
        return (
          <Card className="shadow-soft">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <FileText className="w-5 h-5" />
                Document Management
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-center py-12">
                <FileText className="w-16 h-16 mx-auto text-muted-foreground mb-4" />
                <h3 className="text-lg font-semibold mb-2">No documents yet</h3>
                <p className="text-muted-foreground mb-4">
                  Upload PDF documents through the chat interface to see them here.
                </p>
                <div className="bg-muted rounded-lg p-4 text-left">
                  <h4 className="font-medium mb-2">Coming Soon:</h4>
                  <ul className="text-sm text-muted-foreground space-y-1">
                    <li>• Document history and management</li>
                    <li>• Batch document processing</li>
                    <li>• Export summaries and flowcharts</li>
                    <li>• Search across all documents</li>
                  </ul>
                </div>
              </div>
            </CardContent>
          </Card>
        );
      
      case 'settings':
        return (
          <Card className="shadow-soft">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Settings className="w-5 h-5" />
                Settings & Configuration
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-6">
                <div>
                  <h3 className="text-lg font-semibold mb-4">AI Agent Configuration</h3>
                  <div className="grid gap-4">
                    <div className="p-4 border border-border rounded-lg">
                      <h4 className="font-medium mb-2">📄 PDF Reader Agent</h4>
                      <p className="text-sm text-muted-foreground mb-2">
                        Extract and process text content from PDF documents
                      </p>
                      <div className="text-xs bg-muted px-2 py-1 rounded">
                        // # PDF Reader Agent will be integrated here
                      </div>
                    </div>
                    
                    <div className="p-4 border border-border rounded-lg">
                      <h4 className="font-medium mb-2">📝 Summarization Agent</h4>
                      <p className="text-sm text-muted-foreground mb-2">
                        Generate intelligent summaries and key insights
                      </p>
                      <div className="text-xs bg-muted px-2 py-1 rounded">
                        // # Summarization Agent will be integrated here
                      </div>
                    </div>
                    
                    <div className="p-4 border border-border rounded-lg">
                      <h4 className="font-medium mb-2">📊 Flowchart Generator Agent</h4>
                      <p className="text-sm text-muted-foreground mb-2">
                        Create visual flowcharts from process descriptions
                      </p>
                      <div className="text-xs bg-muted px-2 py-1 rounded">
                        // # Flowchart Generator Agent will be integrated here
                      </div>
                    </div>
                  </div>
                </div>

                <div>
                  <h3 className="text-lg font-semibold mb-4">User Preferences</h3>
                  <div className="space-y-3">
                    <div className="flex items-center justify-between p-3 border border-border rounded-lg">
                      <span className="text-sm">Enable notifications</span>
                      <span className="text-xs text-muted-foreground">Coming soon</span>
                    </div>
                    <div className="flex items-center justify-between p-3 border border-border rounded-lg">
                      <span className="text-sm">Auto-save conversations</span>
                      <span className="text-xs text-muted-foreground">Coming soon</span>
                    </div>
                    <div className="flex items-center justify-between p-3 border border-border rounded-lg">
                      <span className="text-sm">Export format preference</span>
                      <span className="text-xs text-muted-foreground">Coming soon</span>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        );
      
      default:
        return <ChatInterface />;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-warm">
      <Navbar />
      <div className="flex h-[calc(100vh-4rem)]">
        <Sidebar activeTab={activeTab} onTabChange={setActiveTab} />
        <main className="flex-1 p-6 overflow-hidden">
          {renderContent()}
        </main>
      </div>
    </div>
  );
};

export default Dashboard;