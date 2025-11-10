/**
 * server.js
 * Servidor simples para rodar a interface web do detector.
 *
 * Como usar:
 *   npm install express
 *   node server.js
 *   -> depois acesse http://localhost:8080
 */

const express = require('express');
const app = express();
const PORT = 8080;

app.use(express.static('public'));

app.listen(PORT, () => {
  console.log(`🚀 Servindo interface em http://localhost:${PORT}`);
});
