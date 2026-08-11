import { useState, useEffect } from 'react';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Pie } from 'react-chartjs-2';
import jsPDF from 'jspdf';
import 'jspdf-autotable';
import './App.css';

//solo cargo de la libreria lo esencial para las graficas, sexo etc
ChartJS.register(ArcElement, Tooltip, Legend);

function App() {
  const [alumnos, setAlumnos] = useState([]);
  const [formData, setFormData] = useState({
    matricula: '',
    nombre: '',
    sexo: 'M',
    edad: '',
    email: '',
    repetidor: false
  });

  useEffect(() => {
    fetchAlumnos();
  }, []);

//sin el async se va a seguir ejecutando el codigo
  const fetchAlumnos = async () => {
    try {
      const response = await fetch('http://localhost:3001/api/alumnos/list?activo=1');
      const data = await response.json();
      setAlumnos(data);
    } catch (error) {
      console.error("Error al cargar alumnos:", error);
    }
  };
//contiene toda la informacion
  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    //si cambio nombre directamente se traba
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value
    });
  };

  const generarPDF = () => {
    const doc = new jsPDF();
    doc.text("Reporte de Alumnos - IES Lomo de la Herradura", 20, 20);
    const tableColumn = ["Matrícula", "Nombre", "Email", "Sexo"];
    const tableRows = alumnos.map(al => [al.Matricula, al.Nombre, al.Email, al.Sexo]);
    doc.autoTable(tableColumn, tableRows, { startY: 30 });
    doc.save("reporte_alumnos.pdf");
  };

  const chartData = {
    labels: ['Hombres', 'Mujeres'],
    datasets: [{
      data: [
        alumnos.filter(a => a.Sexo === 'M').length,
        alumnos.filter(a => a.Sexo === 'F').length
      ],
      backgroundColor: ['#36A2EB', '#FF6384'],
    }]
  };

  return (
    <div className="app-container">
      <header className="nav-top">
        <div className="nav-content">
          <div className="brand-group">
            <img src="/Logo IES.png" className="logo-ies" alt="Logo IES" />
            <span className="brand-text">IES <strong>Lomo de la Herradura</strong></span>
          </div>
          <img src="/LogoGOBCAN.png" className="logo-gob" alt="Logo Gobierno" />
        </div>
      </header>

      <main className="main-wrapper">
        <section className="form-card">
          <h2 className="section-title">FICHA DEL ALUMNO</h2>
          <div className="input-group">
            <input 
              type="text" name="matricula" placeholder="Matrícula" 
              value={formData.matricula} onChange={handleInputChange} 
            />
          </div>
          <div className="input-group">
            <input 
              type="text" name="nombre" placeholder="Nombre completo" 
              value={formData.nombre} onChange={handleInputChange} 
            />
          </div>
          <div className="row">
            <select name="sexo" value={formData.sexo} onChange={handleInputChange}>
              <option value="M">Masc.</option>
              <option value="F">Fem.</option>
            </select>
            <input 
              type="number" name="edad" placeholder="Edad" 
              value={formData.edad} onChange={handleInputChange} 
            />
          </div>
          <div className="input-group">
            <input 
              type="email" name="email" placeholder="Email" 
              value={formData.email} onChange={handleInputChange} 
            />
          </div>
          <label className="checkbox-container">
            <input 
              type="checkbox" name="repetidor" 
              checked={formData.repetidor} onChange={handleInputChange} 
            />
            <span>¿Es alumno repetidor?</span>
          </label>
          
          <div className="button-group">
            <button className="btn-save">GUARDAR</button>
            <button className="btn-clear" onClick={() => setFormData({matricula:'', nombre:'', sexo:'M', edad:'', email:'', repetidor:false})}>LIMPIAR</button>
          </div>
          <button className="btn-pdf-full" onClick={generarPDF}>GENERAR REPORTE PDF</button>
        </section>

        <section className="content-grid">
          <div className="table-container">
            <h2 className="section-title">Gestión Académica</h2>
            <table>
              <thead>
                <tr>
                  <th>Matrícula</th>
                  <th>Nombre</th>
                  <th>Email</th>
                  <th>Acciones</th>
                </tr>
              </thead>
              <tbody>
                {alumnos.map((alumno) => (
                  <tr key={alumno.Id}>
                    <td>{alumno.Matricula}</td>
                    <td>{alumno.Nombre}</td>
                    <td>{alumno.Email}</td>
                    <td><button className="btn-baja">BAJA</button></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="chart-container">
            <h2 className="section-title">Estadísticas por Sexo</h2>
            <div className="chart-wrapper">
              <Pie data={chartData} />
            </div>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;