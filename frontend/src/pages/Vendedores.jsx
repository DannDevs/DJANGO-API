import { useEffect, useState } from "react"
import Navbar from "../components/Navbar"
import "./vendedores.css"
import { Button, TextInput, Table, Menu } from "@mantine/core"
import SearchIcon from "../components/icons/SearchIcon"
import RefreshIcon from "../components/icons/RefreshIcon"
import ArchiveIcon from "../components/icons/ArchiveIcons"
import { IconX, IconCheck } from "@tabler/icons-react"
import { showNotification } from "@mantine/notifications"
import StatusIcon from "../components/icons/StatusIcon"
import { Link } from "react-router-dom"
function Vendedores() {

    const [vendedores, setVendedores] = useState([]);
    const [pesquisa, setPesquisa] = useState("");

    const ativar = (vendedor) => {
        if (vendedor.ativo === "I") {
            fetch(`http://127.0.0.1:8000/vendedores/ativar/${vendedor.id}`,
                { method: "POST", headers: { 'Content-Type': 'application/json' } })
                .then(res => {
                    if (res.ok) {
                        carregarVendedores()
                        showNotification({
                            title: 'Sucesso',
                            message: 'Vendedor Ativado com sucesso.',
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
                    }
                    else {
                        showNotification({
                            title: 'Erro',
                            message: 'Vendedor Já esta ativo',
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
                })
        }
        else {
            showNotification({
                title: 'Erro',
                message: 'Vendedor Já esta ativo',
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
    const inativar = (vendedor) => {
        if (vendedor.ativo === "A") {
            fetch(`http://127.0.0.1:8000/vendedores/inativar/${vendedor.id}`, {
                method: "POST",
                headers: { 'Content-Type': 'application/json' }
            }).then(res => {
                if (res.ok) {
                    carregarVendedores()
                    showNotification({
                        title: 'Sucesso',
                        message: 'Vendedor Inativado com sucesso',
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
                }
            })
        }
        else {
            showNotification({
                title: 'Erro',
                message: 'Vendedor Já esta Inativo',
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

    const filtrar = (valor) => {

        if (!valor) {
            carregarVendedores()
            return
        }
        fetch(`http://127.0.0.1:8000/vendedores/?nome=${valor}`)
            .then(res => res.json())
            .then(data => setVendedores(data) ?? data)
    }

    const carregarVendedores = () => {
        fetch("http://127.0.0.1:8000/vendedores/")
            .then(res => res.json())
            .then(data => setVendedores(data) ?? data)
    }

    useEffect(() => {
        carregarVendedores()
    }, [])

    const deletarvendedor = (id) => {
        fetch(`http://127.0.0.1:8000/vendedores/${id}`, {
            method: "DELETE",
        }
        ).then(res => {
            if (res.ok) {
                showNotification({
                    title:"Sucesso",
                    message: 'Vendedor Foi Deletado com Sucesso',
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
            carregarVendedores()
            }
        })
    }
    return (
        <>
            <Navbar />
            <div className="container">

                <div className="divcentral">
                    <div className="title"><h2 className="fw-bold ">Vendedores</h2></div>
                    <div className="pesquisador">
                        <TextInput value={pesquisa} onChange={(e) => setPesquisa(e.target.value)}></TextInput>
                        <Button onClick={() => filtrar(pesquisa)}><SearchIcon /></Button>
                    </div>
                    <div className="divfinal">
                        <Button className="me-3" onClick={carregarVendedores}><RefreshIcon color={"white"} /> </Button>
                        <Link to={"/vendedores/cadastro"}>
                            <Button>Cadastrar</Button>
                        </Link>
                    </div>
                </div>
                <div className="tabelavendedor mt-3">
                    <Table style={{ backgroundColor: '#202020cc', borderRadius: '10px', width: '90%' }} withRowBorders={false}>
                        <Table.Thead>
                            <Table.Tr>
                                <Table.Th className="text-center">Ativo</Table.Th>
                                <Table.Th className="text-center">Codigo</Table.Th>
                                <Table.Th className="text-center">Nome</Table.Th>
                                <Table.Th className="text-center">Cargo</Table.Th>
                                <Table.Th className="text-center">E-mail</Table.Th>
                                <Table.Th className="text-center">Açoes</Table.Th>
                            </Table.Tr>
                        </Table.Thead>
                        <Table.Tbody>
                            {vendedores.map(vendedor =>
                                <Table.Tr key={vendedor.id}>
                                    <Table.Td>{vendedor.ativo === 'A' ?
                                        <StatusIcon color={'green'} />
                                        :
                                        <StatusIcon color={'red'} />}</Table.Td>
                                    <Table.Td>{vendedor.id}</Table.Td>
                                    <Table.Td>{vendedor.nome}</Table.Td>
                                    <Table.Td>{vendedor.cargo === 'G' ? 'Gerente' :
                                        vendedor.cargo === 'J' ? 'Junior' :
                                            vendedor.cargo === 'S' ? 'Senior' :
                                                vendedor.cargo === 'R' ? 'Rep' :
                                                    'N/A'
                                    }</Table.Td>
                                    <Table.Td>{vendedor.email}</Table.Td>
                                    <Table.Td>
                                        <Menu>
                                            <Menu.Target>
                                                <Button>Açoes</Button>
                                            </Menu.Target>
                                            <Menu.Dropdown>
                                                <Menu.Item onClick={() => ativar(vendedor)}>Ativar</Menu.Item>
                                                <Menu.Item onClick={() => inativar(vendedor)}>Inativar</Menu.Item>
                                                <Menu.Item>Editar</Menu.Item>
                                                <Menu.Item onClick={() => deletarvendedor(vendedor.id) }>Excluir</Menu.Item>
                                            </Menu.Dropdown>
                                        </Menu>
                                    </Table.Td>
                                </Table.Tr>

                            )}
                        </Table.Tbody>
                    </Table>
                </div>
            </div>
        </>
    )
}
export default Vendedores