import { ChatBubbleLeftIcon } from '@heroicons/react/24/outline';
import { PlusIcon } from '@heroicons/react/24/solid';

export default function ChatList({ conversations, activeId, onSelect, onNewChat }) {
  return (
    <div className="w-[260px] bg-[#202123] flex flex-col h-screen overflow-hidden border-r border-gray-800">
      {/* New Chat Button */}
      <div className="p-2">
        <button
          onClick={onNewChat}
          className="w-full flex items-center gap-3 rounded-md border border-gray-700 text-white px-3 py-3 hover:bg-gray-700/50 transition-colors text-sm"
        >
          <PlusIcon className="h-4 w-4" />
          New chat
        </button>
      </div>

      {/* Chat List */}
      <div className="flex-1 overflow-y-auto">
        <div className="px-2 py-2 space-y-1">
          {conversations.map((chat) => (
            <button
              key={chat.id}
              onClick={() => onSelect(chat)}
              className={`w-full flex items-center gap-3 rounded-md px-3 py-3 text-sm transition-colors ${
                activeId === chat.id 
                ? 'bg-gray-800 text-white'
                : 'text-gray-300 hover:bg-gray-700/50'
              }`}
            >
              <ChatBubbleLeftIcon className="h-4 w-4 flex-shrink-0" />
              <span className="truncate text-left">
                {chat.title || 'New Chat'}
              </span>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}