import { useState, useEffect } from 'react'
import { Link } from "react-router-dom"
import { Table, Checkbox, Button, Menu, MenuDropdown, MenuLabel, Textarea, TextInput } from '@mantine/core';
import { IconCheck, IconX } from '@tabler/icons-react';
import { showNotification } from "@mantine/notifications";
import Navbar from '../components/Navbar';
import './produto.css'
import RefreshIcon from '../components/icons/RefreshIcon';
import ArchiveIcon from '../components/icons/ArchiveIcons';
import SearchIcon from '../components/icons/SearchIcon';
function Produto() {
  const [produtos, setProdutos] = useState([]);
  const [pesquisa,setPesquisa] = useState("");




  useEffect(() => {
    fetch("http://127.0.0.1:8000/produtos/")
      .then(res => {
        if (!res.ok) {
          throw new Error("Erro HTTP" + res.status);
        }
        return res.json();
      })
      .then(data => setProdutos(data.produtos ?? data))
      .catch(err => console.log(err));
  }, []);

const ativar = (produto) => {
    if (produto.ativo === 'I') {
      fetch(`http://127.0.0.1:8000/produtos/${produto.id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ativo: 'A' }),
      }).then(res => {
        if (res.ok) {
          carregarProdutos();
        }
      })
        .then(() => {
          showNotification({
            title: 'Sucesso',
            message: 'Produto Ativado com sucesso.',
            color: 'green',
            styles: (theme) => ({
              closeButton: {
                backgroundColor: '#202020',
              },
              root: {
                backgroundColor: '#202020',
                color: '#ffffffe5',
              },
              title: {
                color: '#fff',
              },
            }),
            radius: 'md',
            autoClose: 3000,
            icon: <IconCheck />,
          })
        })
    }
else {
      showNotification({
        title: 'Erro',
        message: 'Produto Já esta Ativo.',
        color: 'red',
        styles: (theme) => ({
          closeButton: {
            backgroundColor: '#202020',
          },
          root: {
            backgroundColor: '#202020',
            color: '#ffffffe5',
          },
          title: {
            color: '#fff',
          },
        }),
        radius: 'md',
        autoClose: 3000,
        icon: <IconX />,
      })
    }
  }

const inativar = (produto) => {
    if (produto.ativo == "A") {
      fetch(`http://127.0.0.1:8000/produtos/${produto.id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ativo: 'I' }),
      })
        .then(res => {
          if (res.ok) {
            carregarProdutos();
          }
        })
        .then(() => {
          showNotification({
            title: 'Sucesso',
            message: 'Produto Inativo com sucesso.',
            color: 'green',
            styles: (theme) => ({
              closeButton: {
                backgroundColor: '#202020',
              },
              root: {
                backgroundColor: '#202020',
                color: '#ffffffe5',
              },
              title: {
                color: '#fff',
              },
            }),
            radius: 'md',
            autoClose: 3000,
            icon: <IconCheck />,

          })
        })
    }
else {
      showNotification({
        title: 'Erro',
        message: 'Produto ja inativo',
        color: 'red',
        styles: (theme) => ({
          closeButton: {
            backgroundColor: '#202020',
          },
          root: {
            backgroundColor: '#202020',
            color: '#ffffffe5',
          },
          title: {
            color: '#fff',
          },
        }),
        radius: 'md',
        autoClose: 3000,
        icon: <IconX />,
      })
    }
  };

  const deleteProduto = (id) => {
      fetch(`http://127.0.0.1:8000/produtos/${id}`, { method: 'DELETE' })
      .then(() => {
        setProdutos(produtos.filter(p => p.id !== id))
        showNotification({
          title: 'Sucesso!',
          message: 'Produto Excluido com sucesso.',
          color: 'green',
          styles: (theme) => ({
            closeButton: {
              backgroundColor: '#202020',
            },
            root: {
              backgroundColor: '#202020',
              color: '#ffffffe5',
            },
            title: {
              color: '#fff',
            },
          }),
          radius: 'md',
          autoClose: 3000,
          icon: <IconCheck />,
        })
      })

  }

  function carregarProdutos() {
      fetch(`http://127.0.0.1:8000/produtos/`)
      .then(res => {
        if (!res.ok) {
          throw new Error("Erro HTTP" + res.status);
        }
        return res.json();
      })
      .then(data => setProdutos(data.produtos ?? data))
  }

  function filtrar(valor){
    if(!valor){
      carregarProdutos();
      return
    }
    console.log(valor)
    fetch(`http://127.0.0.1:8000/produtos/${valor}`)
    .then(res => res.json())
    .then(data=> setProdutos(data.produto ?? data))
  }

  return (
    <>
      <Navbar />
      <div className='tabela'>
        <div className='d-flex justify-content-between mb-2'>
          <h2 className='fw-bold text-start texto-prin'>Produtos</h2>

          <div className='buttons d-flex'>
            <div className='menu me-3'>

            </div>
          </div>
          <div className='pesquisadiv d-flex'>
            <TextInput value={pesquisa} onChange={(e) => setPesquisa(e.target.value)}></TextInput>
            <Button variant='filled' className='ms-4' onClick={() => filtrar(pesquisa)}><SearchIcon /></Button>
          </div>
          <div>
            {<Button variant="filled" className='me-4' onClick={carregarProdutos}><RefreshIcon color="white" /></Button>}
            <Link to="/produto/cadastro">
              <Button variant="filled">Cadastrar</Button>
            </Link>
          </div>
        </div>

        <Table style={{ backgroundColor: '#202020cc', borderRadius: '10px' }} withRowBorders={false}>
          <Table.Thead style={{ borderRadius: '10px' }}>
            <Table.Tr style={{ backgroundColor: '#202020', borderRadius: '10px' }}>
              <Table.Th className='text-center'>Ativo</Table.Th>
              <Table.Th className='text-center'>ID</Table.Th>
              <Table.Th className='text-center' >Referencia</Table.Th>
              <Table.Th className='text-center'>Descrição</Table.Th>
              <Table.Th className='text-center'>Preço</Table.Th>
              <Table.Th className='text-center'>Estoque</Table.Th>
              <Table.Th className='text-center'>Açoes</Table.Th>
            </Table.Tr>
          </Table.Thead>
          <Table.Tbody>
            {produtos.map(produto => (
              <Table.Tr key={produto.id}>
                <Table.Td>
                  {produto.ativo === 'A' ? (
                    <ArchiveIcon color="#1f521fff" size={18} />
                  ) : (
                    <ArchiveIcon color="#ca1313ff" size={18} />
                  )}
                </Table.Td>
                <Table.Td >{produto.id}</Table.Td>
                <Table.Td>{produto.referencia}</Table.Td>
                <Table.Td>{produto.descricao}</Table.Td>
                <Table.Td>{produto.preco}</Table.Td>
                <Table.Td>{produto.saldo}</Table.Td>
                <Table.Td>
                  <Menu shadow='md'>
                    <Menu.Target>
                      <Button size='xs'>Açoes</Button>
                    </Menu.Target>
                    <MenuDropdown>
                      <Menu.Item onClick={() => deleteProduto(produto.id)}>Excluir</Menu.Item>
                      <Menu.Item onClick={() => ativar(produto)}>Ativar</Menu.Item>
                      <Menu.Item onClick={() => inativar(produto)}>Inativar</Menu.Item>
                      <Menu.Item>
                      <Link className='links' to={`/produtos/ajuste/${produto.id}`}>Ajuste</Link></Menu.Item>
                    </MenuDropdown>
                  </Menu>
                </Table.Td>
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
