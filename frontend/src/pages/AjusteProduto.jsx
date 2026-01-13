import Navbar from "../components/Navbar"
import { Table, Checkbox, NumberInput, Button, Stack, Input, Select, Menu, MenuDropdown, MenuLabel, Textarea, TextInput } from "@mantine/core"
import { Link } from 'react-router-dom';
import { useParams } from "react-router-dom"
import { IconChevronDown } from '@tabler/icons-react';
import { showNotification } from "@mantine/notifications";
import './AjusteProduto.css'
import { useEffect, useState } from "react";
import { IconCheck, IconX } from '@tabler/icons-react';






function AjusteProduto() {
    const { id } = useParams();
    const [tipomov, SetTipomov] = useState("");
    const [quantidade, SetQuantidade] = useState(0);
    const [valor, SetValor] = useState(0);
    const [produtos, SetProdutos] = useState([])

    useEffect(() => {
        movimentos(id);
    }, [id]);



    const ajustarproduto = (id) => {

        fetch(`http://127.0.0.1:8000/produtos/ajuste/${id}`,
            {
                method: "PATCH",
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    quantidade: quantidade,
                    valor: valor,
                    tipo_mov: tipomov
                }),
            }
        )
            .then(res => {
                if (res.ok) {
                    showNotification({
                        title: 'Sucesso',
                        message: 'Produto Ajustado com sucesso.',
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
                    }

                    )
                }
                else {
                    showNotification({
                        title: 'Erro',
                        message: 'Erro ao Ajustar',
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
                movimentos(id)
            }
            )
    }
    const movimentos = (id) => {
        fetch(`http://127.0.0.1:8000/movimentos/${id}`)
            .then(res => res.json())
            .then(date => {
                SetProdutos(date);
            })
            .catch(err => console.log(err))
    }
    return (
        <>
            <Navbar />
            <div className="btnretornar d-flex">
                <Link to="/produtos/">
                    <Button>Retornar</Button>
                </Link>
            </div>
            <h2 className="">Ajustes</h2>
            <form className="gridmovimentos">
                <Stack>
                    <div className="text-start">
                        <Select
                            className="inputq"
                            label="Tipo do Ajuste"
                            description="Tipo do ajuste aplicado"
                            withAsterisk
                            rightSection={<IconChevronDown size={14} stroke={1.5} />}
                            mt="md"
                            data={[
                                { value: "E", label: "+" },
                                { value: "S", label: "-" },
                                { value: "C", label: "$" },
                            ]}
                            value={tipomov}
                            onChange={SetTipomov}
                        />
                    </div>
                    <div className="text-start mt-1">
                        <NumberInput
                            disabled={tipomov === "C"}
                            className="inputq"
                            withAsterisk
                            label="Quantidade"
                            min={0}
                            allowDecimal={true}
                            allowNegative={false}
                            hideControls
                            value={quantidade}
                            onChange={SetQuantidade}
                        />
                    </div>
                    <div className="text-start mt-1">
                        <NumberInput
                            disabled={tipomov === "E" || tipomov == "S"}
                            className="inputq"
                            withAsterisk
                            label="Preco"
                            min={0}
                            allowNegative={false}
                            allowDecimal={true}
                            hideControls
                            value={valor}
                            onChange={SetValor}
                        />
                    </div>
                    <Button className="mt-2 btnmov" onClick={() => ajustarproduto(id)}>
                        Ajustar
                    </Button>
                </Stack>
                <div className="gridmovimentos mt-5 ms-5">
                    <Table style={{ backgroundColor: '#202020cc', borderRadius: '10px' }} withRowBorders={false}>
                        <Table.Thead>
                            <Table.Tr>
                                <Table.Th className="text-center">ID</Table.Th>
                                <Table.Th className="text-center">Produto</Table.Th>
                                <Table.Th className="text-center">Tipo_mov</Table.Th>
                                <Table.Th className="text-center">Quantidade</Table.Th>
                                <Table.Th className="text-center">Valor</Table.Th>
                            </Table.Tr>
                        </Table.Thead>
                        <Table.Tbody>
                            {produtos.map((p) => (
                                <Table.Tr key={p.id}>
                                    <Table.Td>{p.id}</Table.Td>
                                    <Table.Td>{p.produto_nome}</Table.Td>
                                    <Table.Td>{p.tipo_mov}</Table.Td>
                                    <Table.Td>{p.quantidade_mov}</Table.Td>
                                    <Table.Td>{p.valor_mov}</Table.Td>
                                </Table.Tr>
                            ))}
                        </Table.Tbody>
                    </Table>
                </div>
            </form>

        </>
    )
}
export default AjusteProduto