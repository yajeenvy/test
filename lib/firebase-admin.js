import { initializeApp, getApps, cert } from 'firebase-admin/app'  // ← Исправлено здесь
import { getFirestore } from 'firebase-admin/firestore'

const serviceAccount = JSON.parse(process.env.FIREBASE_SERVICE_ACCOUNT)

if (!getApps().length) {
  initializeApp({
    credential: cert(serviceAccount)  // ← Используем правильное имя функции
  })
}

export const db = getFirestore()
