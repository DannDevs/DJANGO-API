import { useState,useEffect } from 'react'
import { Link } from "react-router-dom"

import Navbar from '../components/navbar';
import './App.css'

function App() {
  const [produtos, setProdutos] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/produtos/")
    .then(res =>{
    if(!res.ok){
      throw new Error("Erro HTTP" + res.status);
    }
      return res.json();
    })
    .then(data => setProdutos(data.produtos ?? data))
    .catch(err => console.log(err));
  }, []);
  return (
    <>
    <Navbar />
    <div className='tabela'>
      <div className='d-flex justify-content-between'>
        <h2 className='fw-bold text-start'>Produtos</h2>
         <Link to="/cadastro">
        <button className='btn'>Cadastro</button>
      </Link>        
      </div>
      
     
      <div className='rounded shadow'>
        <table className='table table-striped table-dark'>
          <thead>
            <tr>
              <th className='fw-bold' scope='col'>ID</th>
              <th className='fw-bold' scope='col'>Referencia</th>
              <th className='fw-bold' scope='col'>Descrição</th>
              <th className='fw-bold' scope='col'>Preco</th>
            </tr>
            </thead>  
            <tbody>
                {produtos.map(produto => (
                  <tr className='bg-dark' key={produto.id}>
                    <td>{produto.id}</td>
                    <td>{produto.referencia}</td>
                    <td>{produto.descricao}</td>
                    <td>R$ {produto.preco}</td>
                  </tr>
                ))}
            </tbody>
             
        </table>  
        </div>
    </div>
    </>
  )
}

export default App
