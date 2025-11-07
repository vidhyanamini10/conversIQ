import { PaperAirplaneIcon, StopCircleIcon } from '@heroicons/react/24/solid';

export default function MessageInput({ input, setInput, onSend, onStop, loading }) {
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      onSend();
    }
  };

  return (
    <div className="absolute bottom-0 left-0 w-full bg-[#343541] md:bg-vert-light-gradient pt-6">
      <div className="stretch mx-2 flex flex-row gap-3 last:mb-2 md:mx-4 md:last:mb-6 lg:mx-auto lg:max-w-3xl">
        <div className="relative flex h-full flex-1 flex-col">
          <div className="relative flex w-full flex-grow flex-col rounded-xl border border-gray-900/50 bg-[#40414F] shadow-[0_0_15px_rgba(0,0,0,0.10)] py-2">
            <textarea
              tabIndex="0"
              rows={1}
              placeholder="Send a message..."
              className="m-0 w-full resize-none border-0 bg-transparent py-[10px] pr-10 pl-3 text-white outline-none placeholder:text-gray-400"
              style={{
                maxHeight: '200px',
                height: '24px',
                overflowY: 'hidden',
              }}
              value={input}
              onChange={(e) => {
                setInput(e.target.value);
                // Auto-adjust height
                e.target.style.height = 'auto';
                e.target.style.height = e.target.scrollHeight + 'px';
              }}
              onKeyDown={handleKeyDown}
              disabled={loading}
            />
            <button
              onClick={loading ? onStop : onSend}
              disabled={loading ? false : !input.trim()}
              className="absolute right-2 top-2 rounded-lg p-1 text-gray-400 hover:bg-gray-900 hover:text-gray-200 disabled:hover:bg-transparent disabled:hover:text-gray-400"
            >
              {loading ? (
                <StopCircleIcon className="h-6 w-6 text-red-500" />
              ) : (
                <PaperAirplaneIcon className="h-6 w-6" />
              )}
            </button>
          </div>
        </div>
      </div>
      <div className="px-3 pb-3 pt-2 text-center text-xs text-gray-500">
        Free Research Preview. ConversIQ may produce inaccurate information.
      </div>
    </div>
  );
}
