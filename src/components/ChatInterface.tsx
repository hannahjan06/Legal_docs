import { useState, useRef, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { useToast } from '@/hooks/use-toast';
import ChatMessage, { Message } from './ChatMessage';
import { Send, Upload, FileText, Loader2 } from 'lucide-react';

const ChatInterface = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      content: 'Hello! I\'m your AI assistant. Upload a PDF document and I\'ll help you analyze, summarize, or create flowcharts from it. What would you like to do today?',
      sender: 'bot',
      timestamp: new Date(),
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { toast } = useToast();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputMessage.trim() && !uploadedFile) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      content: inputMessage || `Uploaded file: ${uploadedFile?.name}`,
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    // Simulate AI response delay
    setTimeout(() => {
      let botResponse = '';
      
      if (uploadedFile) {
        botResponse = `I've received your PDF file "${uploadedFile.name}". Here's what I can help you with:

• 📄 **PDF Reader Agent**: Extract and analyze text content
• 📝 **Summarization Agent**: Create concise summaries  
• 📊 **Flowchart Generator**: Create visual flowcharts from processes

// # PDF Reader Agent will be integrated here
// # Summarization Agent will be integrated here  
// # Flowchart Generator Agent will be integrated here

What would you like me to do with this document?`;
      } else {
        // Simple echo response for text messages
        botResponse = `I understand you said: "${inputMessage}"

To get started, please upload a PDF document using the upload button, and I'll help you analyze it with my specialized agents:

• **PDF Reader** - Extract content
• **Summarizer** - Key insights  
• **Flowchart Maker** - Visual diagrams

// # Agent integration points ready for development`;
      }

      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        content: botResponse,
        sender: 'bot',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, botMessage]);
      setIsLoading(false);
      setUploadedFile(null);
    }, 1500);
  };

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      if (file.type === 'application/pdf') {
        setUploadedFile(file);
        toast({
          title: "File uploaded successfully!",
          description: `${file.name} is ready for analysis.`,
        });
      } else {
        toast({
          variant: "destructive",
          title: "Invalid file type",
          description: "Please upload a PDF file only.",
        });
      }
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="flex flex-col h-full">
      {/* File Upload Area */}
      <Card className="mb-4 shadow-soft">
        <CardHeader className="pb-3">
          <CardTitle className="text-lg flex items-center gap-2">
            <FileText className="w-5 h-5" />
            Document Upload
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex items-center gap-3">
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf"
              onChange={handleFileUpload}
              className="hidden"
            />
            <Button
              variant="outline"
              onClick={() => fileInputRef.current?.click()}
              className="hover:shadow-soft transition-all duration-200"
            >
              <Upload className="w-4 h-4 mr-2" />
              Upload PDF
            </Button>
            {uploadedFile && (
              <div className="flex items-center gap-2 text-sm text-muted-foreground bg-muted px-3 py-1 rounded-full">
                <FileText className="w-4 h-4" />
                {uploadedFile.name}
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Chat Messages */}
      <Card className="flex-1 flex flex-col shadow-soft">
        <CardContent className="flex-1 flex flex-col p-4">
          <div className="flex-1 overflow-y-auto space-y-4 pr-2 max-h-[60vh]">
            {messages.map((message) => (
              <ChatMessage key={message.id} message={message} />
            ))}
            {isLoading && (
              <div className="flex items-center gap-3 mb-4">
                <div className="flex-shrink-0 w-8 h-8 bg-primary rounded-full flex items-center justify-center shadow-soft">
                  <Loader2 className="w-4 h-4 text-primary-foreground animate-spin" />
                </div>
                <div className="bg-chat-bot text-chat-bot-foreground rounded-2xl px-4 py-3 shadow-soft">
                  <p className="text-sm">AI is thinking...</p>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Message Input */}
          <div className="mt-4 flex gap-2">
            <Input
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask me about your document or upload a PDF to get started..."
              className="flex-1 transition-all duration-200 focus:shadow-soft"
              disabled={isLoading}
            />
            <Button
              onClick={handleSendMessage}
              disabled={isLoading || (!inputMessage.trim() && !uploadedFile)}
              className="bg-gradient-primary hover:opacity-90 transition-all duration-200 shadow-soft"
            >
              <Send className="w-4 h-4" />
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default ChatInterface;