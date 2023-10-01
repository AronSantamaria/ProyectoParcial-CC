const express = require('express');
const pgp = require('pg-promise')();
const app = express();
const port = 3000;
var cors = require('cors')


const dbConfig = {
  user: 'postgres',
  password: 'BUYBKZ7G5c1Mmh1Gg9xX',
  host: 'database-1.chduhfhuptun.us-east-1.rds.amazonaws.com',
  port: 5432,
  database: 'masterPro'
};

const db = pgp(dbConfig);
app.use(cors())
app.use(express.json());

// Obtener comentarios por película
app.get('/comments/:peliculaId', async (req, res) => {
  const peliculaId = req.params.peliculaId;

  try {
    const comments = await db.any('SELECT * FROM Puntuacion WHERE id_pelicula = $1', [peliculaId]);
    res.json(comments);
  } catch (error) {
    console.error('Error fetching comments:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});


app.post('/comments', async (req, res) => {
  const { peliculaId, usuarioId, comentario } = req.body;

  try {
    await db.none('INSERT INTO Puntuacion (id_pelicula, id_usuario, comentario) VALUES ($1, $2, $3)', [peliculaId, usuarioId, comentario]);
    res.status(201).json({ message: 'Comentario agregado correctamente.' });
  } catch (error) {
    console.error('Error al agregar comentario:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

app.delete('/comments/:peliculaId/:usuarioId', async (req, res) => {
  const peliculaId = req.params.peliculaId;
  const usuarioId = req.params.usuarioId;

  try {
    await db.none('DELETE FROM Puntuacion WHERE id_pelicula = $1 AND id_usuario = $2', [peliculaId, usuarioId]);
    res.json({ message: 'Comentario eliminado correctamente.' });
  } catch (error) {
    console.error('Error al eliminar comentario:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});


app.put('/comments/:peliculaId/:usuarioId', async (req, res) => {
  const peliculaId = req.params.peliculaId;
  const usuarioId = req.params.usuarioId;
  const { nuevoComentario } = req.body;

  try {
    await db.none('UPDATE Puntuacion SET comentario = $1 WHERE id_pelicula = $2 AND id_usuario = $3', [nuevoComentario, peliculaId, usuarioId]);
    res.json({ message: 'Comentario actualizado correctamente.' });
  } catch (error) {
    console.error('Error al actualizar comentario:', error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});

app.listen(port, () => {
  console.log(`Microservicios escuchando en el puerto ${port}`);
});
