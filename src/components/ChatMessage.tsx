import { cn } from '@/lib/utils';
import { Bot, User } from 'lucide-react';

export interface Message {
  id: string;
  content: string;
  sender: 'user' | 'bot';
  timestamp: Date;
}

interface ChatMessageProps {
  message: Message;
}

const ChatMessage = ({ message }: ChatMessageProps) => {
  const isUser = message.sender === 'user';

  return (
    <div className={cn("flex gap-3 mb-4", isUser ? "justify-end" : "justify-start")}>
      {!isUser && (
        <div className="flex-shrink-0 w-8 h-8 bg-primary rounded-full flex items-center justify-center shadow-soft">
          <Bot className="w-4 h-4 text-primary-foreground" />
        </div>
      )}
      
      <div className={cn(
        "max-w-[80%] sm:max-w-[70%] rounded-2xl px-4 py-3 shadow-soft transition-smooth",
        isUser 
          ? "bg-chat-user text-chat-user-foreground ml-12" 
          : "bg-chat-bot text-chat-bot-foreground mr-12"
      )}>
        <p className="text-sm leading-relaxed whitespace-pre-wrap">
          {message.content}
        </p>
        <div className="mt-2 text-xs opacity-70">
          {message.timestamp.toLocaleTimeString([], { 
            hour: '2-digit', 
            minute: '2-digit' 
          })}
        </div>
      </div>

      {isUser && (
        <div className="flex-shrink-0 w-8 h-8 bg-gradient-primary rounded-full flex items-center justify-center shadow-soft">
          <User className="w-4 h-4 text-primary-foreground" />
        </div>
      )}
    </div>
  );
};

export default ChatMessage;