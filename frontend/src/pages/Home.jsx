import './Home.css'
import Navbar from '../components/Navbar'
import { Card, Group, Text, useMantineTheme,Stack } from '@mantine/core';

function Home(){
    return(
        <>
        <Navbar />
        <div>
            <Stack>
                <h2>Olá Usuario</h2>
                <div className='cards'>
                    <Card style={{ backgroundColor:'#2d2c2c'}} shadow='sw'>
                    <Text fw={500} style={{color:'white'}}>Vendas de Hoje</Text>
                    </Card>
                    <Card style={{ backgroundColor:'#2d2c2c'}} shadow='sw'>
                    <Text fw={500} style={{color:'white'}}>Vendas de Hoje</Text>
                    </Card>
                    <Card style={{ backgroundColor:'#2d2c2c'}} shadow='sw'>
                    <Text fw={500} style={{color:'white'}}>Vendas de Hoje</Text>
                    </Card>
                    <Card style={{ backgroundColor:'#2d2c2c'}} shadow='sw'>
                    <Text fw={500} style={{color:'white'}}>Vendas de Hoje</Text>
                    </Card>
                </div>                    
            </Stack>
        </div>
        </>
    )
}
export default Home