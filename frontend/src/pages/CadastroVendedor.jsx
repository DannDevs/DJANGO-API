import { Button, Stack, TextInput } from "@mantine/core"
import Navbar from "../components/Navbar"
import { Link } from "react-router-dom"
import './cadastrovendedor.css'

function CadastroVendedor() {
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
                            <TextInput className="mt-3"
                            label="Nome"
                            withAsterisk
                            rightSection
                            style={{
                                'textAlign':'start'
                            }}
                            >
                            </TextInput>
                            <TextInput className="mt-3"
                             label="Cargo"
                            withAsterisk
                            rightSection
                            style={{
                                'textAlign':'start'
                            }}
                            >
                            </TextInput>
                            <TextInput className="mt-3 mb-3"
                             label="E-mail"
                            withAsterisk
                            rightSection
                            style={{
                                'textAlign':'start'
                            }}
                            >
                            </TextInput>

                            <Button className="mt-4"
                            fullWidth
                            w={210}
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