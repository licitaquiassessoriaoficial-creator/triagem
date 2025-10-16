import React from 'react';

export default function Dashboard() {
  return (
    <div className="container">
      <h1 className="title">Sistema de Triagem ODQ - Web</h1>
      
      <div className="main-content">
        <h2 className="success-title">✅ Conversão Concluída!</h2>
        <p>O sistema desktop foi convertido com sucesso para uma aplicação web moderna:</p>
        
        <div className="grid">
          <div className="card">
            <h3 className="card-title backend">Backend (FastAPI)</h3>
            <ul>
              <li>API REST completa</li>
              <li>PostgreSQL + Redis</li>
              <li>Autenticação JWT</li>
              <li>Deploy Railway</li>
            </ul>
          </div>
          
          <div className="card">
            <h3 className="card-title frontend">Frontend (Next.js)</h3>
            <ul>
              <li>Interface moderna</li>
              <li>TypeScript + TailwindCSS</li>
              <li>Responsive design</li>
              <li>Deploy Netlify</li>
            </ul>
          </div>
        </div>
        
        <div className="deploy-info">
          <h3 className="deploy-title">🚀 Pronto para Deploy!</h3>
          <p>Execute o setup automatizado: <code>./setup.ps1</code></p>
        </div>
      </div>
      
      <style>{`
        .container {
          padding: 20px;
          font-family: Arial, sans-serif;
        }
        .title {
          color: #333;
          text-align: center;
        }
        .main-content {
          max-width: 800px;
          margin: 0 auto;
          padding: 20px;
          background-color: #f5f5f5;
          border-radius: 8px;
          margin-top: 20px;
        }
        .success-title {
          color: #2563eb;
        }
        .grid {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 20px;
          margin-top: 20px;
        }
        .card {
          background-color: white;
          padding: 15px;
          border-radius: 6px;
          box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .card-title {
          margin: 0 0 10px 0;
        }
        .backend {
          color: #059669;
        }
        .frontend {
          color: #7c3aed;
        }
        .card ul {
          margin: 0;
          padding-left: 20px;
        }
        .deploy-info {
          background-color: #dbeafe;
          padding: 15px;
          border-radius: 6px;
          margin-top: 20px;
          text-align: center;
        }
        .deploy-title {
          margin: 0 0 10px 0;
          color: #1d4ed8;
        }
        .deploy-info p {
          margin: 0;
        }
      `}</style>
    </div>
  );
}