import { Button, Stack, Text, TextInput,PasswordInput } from "@mantine/core"
import "./login.css"

function Login() {
    return (
        <>
            <div className="login-container">
                <Stack
                    align="center">
                    <Text className="fw-bold mb-4">Login</Text>
                    <TextInput
                        placeholder="Seuemail@gmail.com"
                        label="Usuario"
                        w={300}
                        style={{
                            'textAlign':'start'
                        }}
                    ></TextInput>
                    <PasswordInput
                        label="Senha"
                        w={300}
                        style={{
                            'textAlign': 'start'
                        }}
                    ></PasswordInput>
                    <Button className="mt-4 mb-5"
                        fullWidth
                        w={300}
                    >Acessar</Button>
                </Stack>
            </div>
        </>
    )
}
export default Login