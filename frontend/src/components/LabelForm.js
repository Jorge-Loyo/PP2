// src/components/LabelForm.js
import React, { useState, useEffect } from 'react';
import axios from 'axios'; // Asegúrate de tener axios instalado

function LabelForm() {
  const [monodroga, setMonodroga] = useState('');
  const [marca, setMarca] = useState('');
  const [presentacion, setPresentacion] = useState('');
  const [lote, setLote] = useState('');
  const [vencimiento, setVencimiento] = useState('');
  const [cantidad, setCantidad] = useState('');

  const [sugerenciasMonodroga, setSugerenciasMonodroga] = useState([]);
  const [mostrarSugerenciasMonodroga, setMostrarSugerenciasMonodroga] = useState(false);

  // Simulación de datos de monodrogas (reemplazar con llamada a la API)
  const [listaMonodrogas, setListaMonodrogas] = useState([]);

  useEffect(() => {
    // Aquí harías la llamada a tu API para obtener la lista de monodrogas
    // Ejemplo con axios:
    axios.get('http://localhost:3001/api/monodrogas') // Reemplaza con tu endpoint
      .then(response => {
        setListaMonodrogas(response.data);
      })
      .catch(error => {
        console.error('Error al obtener monodrogas:', error);
        setListaMonodrogas(['Paracetamol', 'Ibuprofeno', 'Aspirina']); // Datos de respaldo
      });
  }, []);

  const handleInputChangeMonodroga = (event) => {
    const value = event.target.value;
    setMonodroga(value);

    // Filtrar las sugerencias
    const nuevasSugerencias = listaMonodrogas.filter(
      (item) => item.toLowerCase().includes(value.toLowerCase()) && value.length > 0
    );
    setSugerenciasMonodroga(nuevasSugerencias);
    setMostrarSugerenciasMonodroga(true);
  };

  const handleSugerenciaClickMonodroga = (sugerencia) => {
    setMonodroga(sugerencia);
    setSugerenciasMonodroga([]);
    setMostrarSugerenciasMonodroga(false);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    console.log({ monodroga, marca, presentacion, lote, vencimiento, cantidad });
    // Aquí iría la lógica para enviar los datos al backend
  };

  return (
    <div>
      <h2>Generar Etiqueta</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="monodroga">Monodroga:</label>
          <input
            type="text"
            id="monodroga"
            value={monodroga}
            onChange={handleInputChangeMonodroga}
            onBlur={() => setTimeout(() => setMostrarSugerenciasMonodroga(false), 100)} // Ocultar al perder foco
          />
          {mostrarSugerenciasMonodroga && sugerenciasMonodroga.length > 0 && (
            <ul>
              {sugerenciasMonodroga.map((sugerencia) => (
                <li key={sugerencia} onClick={() => handleSugerenciaClickMonodroga(sugerencia)}>
                  {sugerencia}
                </li>
              ))}
            </ul>
          )}
        </div>
        {/* Campos para Marca y Presentación (implementar lógica similar al autocompletado de Monodroga) */}
        <div>
          <label htmlFor="marca">Marca:</label>
          <input
            type="text"
            id="marca"
            value={marca}
            onChange={(e) => setMarca(e.target.value)}
          />
          {/* Implementar autocompletado para Marca aquí */}
        </div>
        <div>
          <label htmlFor="presentacion">Presentación:</label>
          <input
            type="text"
            id="presentacion"
            value={presentacion}
            onChange={(e) => setPresentacion(e.target.value)}
          />
          {/* Implementar autocompletado para Presentación aquí */}
        </div>
        <div>
          <label htmlFor="lote">Lote:</label>
          <input
            type="text"
            id="lote"
            value={lote}
            onChange={(e) => setLote(e.target.value)}
          />
        </div>
        <div>
          <label htmlFor="vencimiento">Vencimiento:</label>
          <input
            type="date"
            id="vencimiento"
            value={vencimiento}
            onChange={(e) => setVencimiento(e.target.value)}
          />
        </div>
        <div>
          <label htmlFor="cantidad">Cantidad:</label>
          <input
            type="number"
            id="cantidad"
            value={cantidad}
            onChange={(e) => setCantidad(e.target.value)}
          />
        </div>
        <button type="submit">Generar Etiqueta</button>
      </form>
    </div>
  );
}

export default LabelForm;