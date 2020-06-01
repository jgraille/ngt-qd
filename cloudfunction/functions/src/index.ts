import * as functions from 'firebase-functions';
import * as admin from 'firebase-admin';

// Import and initialize the Firebase Admin SDK.
const serviceAccount = require('../../../cloudfunction/serviceaccountkey.json');
admin.initializeApp({
  credential: admin.credential.cert(serviceAccount),
  databaseURL: `https://ngttest-64cd5.firebaseio.com`
})

// // Start writing Firebase Functions
// // https://firebase.google.com/docs/functions/typescript
export const helloWorld = functions.https.onRequest((request, response) => {
  response.send("Hello from Firebase!");
});

export const onMessageCreate = functions.database
.ref('/0/{0id}/checkone/{checkoneId}')
.onCreate((snapshot,context) => {
  console.log(`Just a test`)
})