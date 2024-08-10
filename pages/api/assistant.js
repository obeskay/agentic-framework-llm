import axios from 'axios';

export default async function handler(req, res) {
  if (req.method === 'POST') {
    try {
      const { message } = req.body;
      
      // Make an API call to the Python backend
      const response = await axios.post('http://localhost:5000/api/send_message', { message });
      
      if (response.data && response.data.content) {
        res.status(200).json({ message: response.data.content[0].text });
      } else {
        res.status(500).json({ error: 'Failed to get response from assistant' });
      }
    } catch (error) {
      console.error('Error:', error);
      res.status(500).json({ error: 'An unexpected error occurred' });
    }
  } else {
    res.setHeader('Allow', ['POST']);
    res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}