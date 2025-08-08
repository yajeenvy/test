import { db } from '../../lib/firebase-admin'
import Cors from 'cors'

// Инициализация CORS
const cors = Cors({
  methods: ['POST'],
  origin: '*' // Для продакшена укажите ваш домен
})

function runMiddleware(req, res, fn) {
  return new Promise((resolve, reject) => {
    fn(req, res, (result) => {
      if (result instanceof Error) return reject(result)
      return resolve(result)
    })
  })
}

export default async function handler(req, res) {
  // Применяем CORS
  await runMiddleware(req, res, cors)

  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' })
  }

  try {
    const { hwid } = req.body
    
    if (!hwid) {
      return res.status(400).json({ error: 'HWID is required' })
    }

    const doc = await db.collection('authorized_hwids').doc(hwid).get()
    
    return res.status(200).json({
      access_granted: doc.exists,
      hwid: hwid
    })

  } catch (error) {
    console.error('Error checking HWID:', error)
    return res.status(500).json({ error: 'Internal server error' })
  }
}