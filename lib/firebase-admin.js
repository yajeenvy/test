import { initializeApp, getApps } from 'firebase-admin/app'
import { getFirestore } from 'firebase-admin/firestore'

const serviceAccount = JSON.parse(process.env.FIREBASE_SERVICE_ACCOUNT)

if (!getApps().length) {
  initializeApp({
    credential: certificate(serviceAccount)
  })
}

export const db = getFirestore()