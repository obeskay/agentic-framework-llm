import { useState, useEffect } from 'react';
import axios from 'axios';

export default function Home() {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post('http://localhost:5000/api/send_message', { message });
      setResponse(res.data.content);
    } catch (error) {
      setResponse('Error: Failed to get response from the assistant.');
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen py-2">
      <h1 className="text-4xl font-bold mb-4">AI Assistant</h1>
      <form onSubmit={handleSubmit} className="flex flex-col items-center">
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          className="border border-gray-300 p-2 mb-4 w-80 h-32"
          placeholder="Type your message here..."
        />
        <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">
          Send Message
        </button>
      </form>
      {response && <p className="mt-4">Response: {response}</p>}
    </div>
  );
import axios from 'axios';

export default function Home() {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setResponse('');

    try {
      const res = await axios.post('/api/assistant', { message });
      setResponse(res.data.message);
    } catch (error) {
      setResponse('Error: Failed to get response from the assistant.');
      console.error('Error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 py-6 flex flex-col justify-center sm:py-12">
      <div className="relative py-3 sm:max-w-xl sm:mx-auto">
        <div className="absolute inset-0 bg-gradient-to-r from-cyan-400 to-light-blue-500 shadow-lg transform -skew-y-6 sm:skew-y-0 sm:-rotate-6 sm:rounded-3xl"></div>
        <div className="relative px-4 py-10 bg-white shadow-lg sm:rounded-3xl sm:p-20">
          <div className="max-w-md mx-auto">
            <div>
              <h1 className="text-2xl font-semibold text-center">AI Assistant</h1>
            </div>
            <div className="divide-y divide-gray-200">
              <form onSubmit={handleSubmit} className="py-8 text-base leading-6 space-y-4 text-gray-700 sm:text-lg sm:leading-7">
                <div className="relative">
                  <textarea
                    id="message"
                    name="message"
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    className="peer h-32 w-full border-b-2 border-gray-300 text-gray-900 focus:outline-none focus:border-rose-600 resize-none"
                    placeholder="Enter your message here"
                  ></textarea>
                </div>
                <div className="relative">
                  <button type="submit" className="bg-blue-500 text-white rounded-md px-4 py-2 hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-600 focus:ring-opacity-50 w-full">
                    {isLoading ? 'Sending...' : 'Send'}
                  </button>
                </div>
              </form>
              {response && (
                <div className="py-8 text-base leading-6 space-y-4 text-gray-700 sm:text-lg sm:leading-7">
                  <p className="font-bold">Response:</p>
                  <p className="text-gray-600">{response}</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
