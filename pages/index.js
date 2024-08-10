import { useState } from 'react';

export default function Home() {
  const [message, setMessage] = useState('');
  const [response, setResponse] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setResponse('');

    try {
      const res = await fetch('/api/send_message', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message }),
      });

      if (!res.ok) {
        throw new Error('Failed to send message');
      }

      const data = await res.json();
      setResponse(data.content[0].text);
    } catch (err) {
      setError('Error sending message: ' + err.message);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">AI Assistant</h1>
      <form onSubmit={handleSubmit} className="mb-4">
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          className="w-full p-2 border rounded"
          rows="4"
          placeholder="Enter your message here"
        ></textarea>
        <button type="submit" className="mt-2 px-4 py-2 bg-blue-500 text-white rounded">
          Send
        </button>
      </form>
      {error && <p className="text-red-500">{error}</p>}
      {response && (
        <div className="mt-4">
          <h2 className="text-xl font-semibold">Response:</h2>
          <p>{response}</p>
        </div>
      )}
    </div>
  );
}
