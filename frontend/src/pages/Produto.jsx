import { useState,useEffect } from 'react'
import { Link } from "react-router-dom"
import { Table,Checkbox,Button,Menu, MenuDropdown, MenuLabel } from '@mantine/core';
import { IconCheck } from '@tabler/icons-react';
import { showNotification } from "@mantine/notifications";
import Navbar from '../components/navbar';
import './Produto.css'
function Produto() {
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

  const deleteProduto = (id) => {
    fetch(`http://127.0.0.1:8000/produtos/${id}`,{method:'DELETE'})
    .then(() =>{
      setProdutos(produtos.filter(p => p.id !== id))
      showNotification({
            title: 'Sucesso!',
            message: 'Produto Excluido com sucesso.',
            color: 'green',
           styles: (theme) =>({
                closeButton:{
                    backgroundColor:'#202020',
                },
                root:{
                    backgroundColor:'#202020',
                    color:'#ffffffe5',
                },
                title:{
                    color:'#fff',
                },
            }),
            radius: 'md',
            autoClose: 3000,
            icon: <IconCheck />, 
      })
    })
    
  }

  return (
    <>
    <Navbar />
    <div className='tabela'>
      <div className='d-flex justify-content-between mb-2'>
        <h2 className='fw-bold text-start texto-prin'>Produtos</h2>
         
         <div className='buttons d-flex'>
          <div className='menu me-3'>
          <Menu shadow='md'>
            <Menu.Target>
              <Button>Açoes</Button>
              </Menu.Target>
              <MenuDropdown>
                <Menu.Item>Excluir</Menu.Item>
                <Menu.Item>Ativar</Menu.Item>
                <Menu.Item>Inativar</Menu.Item>
              </MenuDropdown>
          </Menu>
          </div>
          <div>
          </div>
          <Link to="/cadastro">
            <Button variant="filled">Cadastrar</Button>
          </Link>
         </div>    
      </div>

       <Table style={{backgroundColor:'#202020cc'}} withRowBorders={false}>
        <Table.Thead>
          <Table.Tr style={{backgroundColor:'#202020'}}>
            <Table.Th className='text-center'>Ativo</Table.Th>
            <Table.Th className='text-center'>ID</Table.Th>
            <Table.Th className='text-center' >Referencia</Table.Th>
            <Table.Th className='text-center'>Descrição</Table.Th>
            <Table.Th className='text-center'>Preço</Table.Th>
            <Table.Th className='text-center'>Açoes</Table.Th>
          </Table.Tr>
        </Table.Thead>
        <Table.Tbody>
          {produtos.map(produto => (
            <Table.Tr key={produto.id}>
              <Table.Td>{produto.ativo}</Table.Td>
              <Table.Td >{produto.id}</Table.Td>
              <Table.Td>{produto.referencia}</Table.Td>
              <Table.Td>{produto.descricao}</Table.Td>
              <Table.Td>{produto.preco}</Table.Td>
              <Table.Td><Button size="xs" onClick={() => deleteProduto(produto.id)}>Excluir</Button></Table.Td>
            </Table.Tr>
          )
          )}
        </Table.Tbody>
      </Table> 
    </div>
    </>
  )
}

export default Produto
