import Navbar from "../components/Navbar"
import './vendas.css'
import { Table, Checkbox, Button, Menu, MenuDropdown, MenuLabel, Textarea, TextInput } from '@mantine/core';
import {Input} from '@mantine/form'

function Vendas() {
    
    return (
        <>
            <Navbar />
            <div className="divisaocentral">
            <div className="cabeçalho">
                <h2 className="fw-bold text-start">Vendas</h2>
                <Input></Input>
            </div>
            
                <Table>
                    <Table.Thead>
                        <Table.Tr>
                            <Table.Th>ID</Table.Th>
                            <Table.Th>Status</Table.Th>
                            <Table.Th>Cliente</Table.Th>
                            <Table.Th>Vendedor</Table.Th>
                            <Table.Th>Valor Venda</Table.Th>
                        </Table.Tr>
                    </Table.Thead>
                    <Table.Tbody>

                    </Table.Tbody>
                </Table>
            </div>
        </>
    )

}
export default Vendas