import Navbar from "../components/Navbar.JSX"
import { NumberInput, TextInput, Button, Stack, Input, Select } from "@mantine/core"
import { useForm } from "@mantine/form"
import { useParams } from "react-router-dom"
import { IconChevronDown } from '@tabler/icons-react';
import './AjusteProduto.css'



function AjusteProduto() {
    const { id } = useParams();

    fetch

    return (
        <>
            <Navbar />
            <h2 className="mt-10">Ajustes</h2>
            <form action="">

                <Stack>
                    <div className="text-start">
                        <Select
                            className="inputcolor"
                            label="Tipo do Ajuste"
                            description="Tipo do ajuste aplicado"
                            withAsterisk
                            rightSection={<IconChevronDown size={14} stroke={1.5} />}
                            mt="md"
                            data={[
                                { value: "1", label: "+" },
                                { value: "2", label: "-" },
                                { value: "3", label: "$" },
                            ]}
                        />


                    </div>
                    <div className="text-start mt-1">
                        <NumberInput
                            withAsterisk
                            label="Quantidade"
                            min={0}
                            allowDecimal={true}
                            allowNegative={false}
                            hideControls
                        />
                    </div>
                    <div className="text-start mt-1">
                        <NumberInput
                            withAsterisk
                            label="Preco"
                            min={0}
                            allowNegative={false}
                            allowDecimal={true}
                            hideControls
                        />
                    </div>

                    <Button className="mt-2" type="submit">Ajustar</Button>
                </Stack>
            </form>

        </>
    )
}
export default AjusteProduto