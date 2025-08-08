import { db } from '../../lib/firebase-admin'
import Cors from 'cors'

const cors = Cors({
  methods: ['POST'],
  origin: true
})

export default async function handler(req, res) {
  // CORS middleware
  await new Promise((resolve, reject) => {
    cors(req, res, (result) => {
      if (result instanceof Error) return reject(result)
      return resolve(result)
    })
  })

  if (req.method !== 'POST') {
    res.setHeader('Allow', ['POST'])
    return res.status(405).json({ error: 'Method not allowed' })
  }

  try {
    const { hwid } = req.body
    if (!hwid) {
      return res.status(400).json({ error: 'HWID is required' })
    }

    const doc = await db.collection('authorized_hwids').doc(hwid).get()
    res.status(200).json({ 
      access_granted: doc.exists,
      hwid: hwid
    })
  } catch (error) {
    console.error('Firebase Error:', error)
    res.status(500).json({ 
      error: 'Internal server error',
      details: error.message 
    })
  }
}
