import { useEffect, useState } from "react";
import Navbar from "../components/Navbar"
import './vendas.css'
import { Link } from "react-router-dom";
import { Table, Checkbox, Button, Menu, MenuDropdown, MenuLabel, Textarea, TextInput,Stack} from '@mantine/core';
import  SearchIcon from "../components/icons/SearchIcon"
import RefreshIcon from "../components/icons/RefreshIcon"
function Vendas() {

    const [vendas,setVendas] = useState([]);

const carregarVendas = () => {
    fetch("http://127.0.0.1:8000/vendas/")
    .then(res => res.json())
    .then(data => {
        setVendas(data)
    })
}

useEffect(()=> {
    carregarVendas();
},[])

    return (
        <>
            <Navbar />
            <div className='buttons d-flex'>
            <div className='menu me-3'>

            </div>
          </div>
          <div className='pesquisadiv d-flex'>
            <TextInput></TextInput>
            <Button variant={'filled'}><SearchIcon /></Button>
          </div>
          <div>
            {<Button variant="filled" className='me-4' onClick={carregarVendas}><RefreshIcon color="white" /></Button>}
            <Link to="/produto/cadastro">
              <Button variant="filled">Cadastrar</Button>
            </Link>
          </div>
        

            
                <Table>
                    <Table.Thead>
                        <Table.Tr>
                            <Table.Th className="text-center">ID</Table.Th>
                            <Table.Th className="text-center">Status</Table.Th>
                            <Table.Th className="text-center">Tipo Venda</Table.Th>
                            <Table.Th className="text-center">Cliente</Table.Th>
                            <Table.Th className="text-center">Vendedor</Table.Th>
                            <Table.Th className="text-center">Valor Venda</Table.Th>
                        </Table.Tr>
                    </Table.Thead>
                    <Table.Tbody>
                        {vendas.map(venda => (
                            <Table.Tr key={venda.id}>
                            <Table.Td>{venda.id}</Table.Td>
                            <Table.Td>{venda.status}</Table.Td>
                            <Table.Td>Tipo Venda</Table.Td>
                            <Table.Td>Cliente</Table.Td>
                            <Table.Td>Vendedor</Table.Td>
                            <Table.Td>Valor Venda</Table.Td>
                            </Table.Tr>
                        ))}
                    
                    </Table.Tbody>
                </Table>
        </>
    )

}
export default Vendas