import { db } from '../../lib/firebase-admin';

export default async function handler(req, res) {
  // Убедитесь, что возвращается JSON
  res.setHeader('Content-Type', 'application/json');

  try {
    if (req.method !== 'POST') {
      return res.status(405).json({ error: 'Method not allowed' });
    }

    const { hwid } = req.body;
    if (!hwid) {
      return res.status(400).json({ error: 'HWID is required' });
    }

    const doc = await db.collection('authorized_hwids').doc(hwid).get();
    res.status(200).json({ 
      access_granted: doc.exists,
      hwid: hwid
    });
  } catch (error) {
    console.error('Error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
}
