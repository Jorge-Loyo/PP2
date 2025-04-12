// Importar el módulo de Express
const express = require('express');
const bodyParser = require('body-parser');

// Crear una instancia de la aplicación Express
const app = express();

// Definir el puerto en el que el servidor escuchará las peticiones
const port = process.env.PORT || 3001; // Usa la variable de entorno PORT si está definida, sino usa el puerto 3001
const authRoutes = require('./routes/auth');
const authenticateToken = require('./middleware/authenticateToken');
app.use(bodyParser.json());
app.use('/api/auth', authRoutes);
// Middleware básico para registrar las peticiones (opcional, pero útil para depuración)
app.use((req, res, next) => {
  console.log(`[${new Date().toLocaleString()}] ${req.method} ${req.url}`);
  next(); // Llama al siguiente middleware o ruta
});

// Middleware para habilitar el manejo de datos JSON en las peticiones (si planeas enviar y recibir JSON)
app.use(express.json());

// Middleware para habilitar el manejo de datos de formularios codificados en la URL (si planeas usar formularios HTML tradicionales)
app.use(express.urlencoded({ extended: true }));

// --- Configuración de Rutas ---

// Ruta básica GET en la raíz ('/')
app.get('/', (req, res) => {
  res.send('¡Hola desde el servidor Express!');
});

// Otra ruta GET en '/api/saludo'
app.get('/api/saludo', (req, res) => {
  res.json({ mensaje: '¡Saludos desde la API!' });
});

// Ruta POST en '/api/datos' (ejemplo para recibir datos)
app.post('/api/datos', (req, res) => {
  const datosRecibidos = req.body; // Los datos enviados en el cuerpo de la petición estarán aquí
  console.log('Datos recibidos:', datosRecibidos);
  res.json({ mensaje: 'Datos recibidos correctamente', data: datosRecibidos });
});

// --- Middleware para manejar errores 404 (si ninguna ruta coincide) ---
app.use((req, res, next) => {
  res.status(404).send('¡Ups! No se encontró lo que buscabas.');
});

// --- Middleware para manejar errores generales del servidor (500) ---
app.use((err, req, res, next) => {
  console.error('Error en el servidor:', err.stack);
  res.status(500).send('¡Oh no! Algo salió mal en el servidor.');
});

// Iniciar el servidor y hacerlo escuchar en el puerto definido
app.listen(port, () => {
  console.log(`Servidor Express escuchando en el puerto ${port}`);
});