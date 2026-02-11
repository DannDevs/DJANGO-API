import { Button, Stack, TextInput, Text, Select } from "@mantine/core"
import Navbar from "../components/Navbar"
import { Link } from "react-router-dom"
import './cadastrovendedor.css'
import { useEffect, useState } from "react"
import { showNotification } from "@mantine/notifications"
import { IconCheck } from "@tabler/icons-react"

function CadastroVendedor() {
    const [form, setForm] = useState({
        nome: "",
        cargo: "",
        email: ""
    })
    function handleChange(e) {
        setForm({
            ...form,
            [e.currentTarget.name]: e.currentTarget.value
        })
    }
    useEffect(() => {
        console.log(form)
    }, [form])

    const cargos = [
        { value: 'G', label: 'Gerente' },
        { value: 'S', label: 'Vendedor Senior' },
        { value: 'R', label: 'Representante Comercial' },
        { value: 'J', label: 'Vendedor Junior' }
    ]



    const handleSubmit = () => {
        console.log(form)

        fetch(`http://127.0.0.1:8000/vendedores/cadastro/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(form),
        }).then(res => {
            if (res.ok) {
                showNotification({
                    title: 'Sucesso!',
                    message: 'Produto cadastrado com sucesso.',
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

    return (
        <>
            <Navbar />
            <div className="container">
                <div className="acoes">
                    <Link to={"/vendedores/"}>
                        <Button>Retornar</Button>
                    </Link>
                </div>
                <div className="form-container mt-4">
                    <div className="formcadastro">
                        <Stack
                            h={520}
                            align="center"
                            justify="center"

                        >

                            <Text className="fw-bold" style={{ fontSize: '30px' }}>Cadastro Vendedor</Text>

                            <TextInput className="mt-3"
                                label="Nome"
                                withAsterisk
                                rightSection
                                name="nome"
                                style={{
                                    'textAlign': 'start'
                                }}
                                onChange={handleChange}
                            >
                            </TextInput>
                            <Select
                                className="mt-3"
                                label="Cargo"
                                searchable
                                nothingFoundMessage="Sem Resultados..."
                                data={cargos}
                                onChange={(value) =>
                                    setForm({
                                        ...form,
                                        cargo: value
                                    })
                                }
                                style={{
                                    'textAlign': 'start'
                                }}
                                withAsterisk
                            >

                            </Select>
                            <TextInput className="mt-3 mb-3"
                                label="E-mail"
                                withAsterisk
                                rightSection
                                onChange={handleChange}
                                name="email"
                                style={{
                                    'textAlign': 'start'
                                }}
                            >
                            </TextInput>

                            <Button className="mt-4"
                                fullWidth
                                w={210}
                                onClick={handleSubmit}
                            >
                                Cadastrar
                            </Button>

                        </Stack>
                    </div>
                </div>

            </div>

        </>
    )

}
export default CadastroVendedor