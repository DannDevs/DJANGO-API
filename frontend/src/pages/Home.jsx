import './Home.css'
import Navbar from '../components/Navbar'
import { Card, Group, Text, useMantineTheme,Stack } from '@mantine/core';
import { useEffect, useState } from 'react';

function Home(){

    const [total,SetTotal] = useState([]);

    const totalvendas = () => {
        fetch(`http://127.0.0.1:8000/vendas/totalvendas/`)
        .then(res => res.json())
        .then(data =>
            SetTotal(data)
        )
    }

    useEffect(() =>{
    totalvendas()
    },[]);

    


    return(
        <>
        <Navbar />
        <div>
            <Stack>
                <Text fw={500} style={{fontSize:'40px'}} className='fw-bold mt-2' >Seja Bem Vindo User!</Text>
                <Text className='md-4' style={{fontSize:'20px'}}>Seus Resultados</Text>
                <div className='cards'>
                    <Card w={250} style={{ backgroundColor:'#2d2c2c'}} shadow='sw'>
                    <div className='inputs-home'>
                        <Text style={{color:'white'}}>a</Text>
                        <Text fw={500} style={{color:'white'}}>Vendas de Hoje</Text>
                    </div>
                    <Text fw={500} className='fw-bold' style={{color:'white'}}>{total.total_vendas}</Text>
                    </Card>
                    <Card w={250} style={{ backgroundColor:'#2d2c2c'}} shadow='sw'>
                    <div className='inputs-home'>
                        <Text style={{color:'white'}}>a</Text>
                        <Text fw={500} style={{color:'white'}}>Vendas de Hoje</Text>
                    </div>
                    <Text fw={500} className='fw-bold' style={{color:'white'}}>0</Text>
                    </Card>
                    <Card w={250} style={{ backgroundColor:'#2d2c2c'}} shadow='sw'>
                    <div className='inputs-home'>
                        <Text style={{color:'white'}}>a</Text>
                        <Text fw={500} style={{color:'white'}}>Vendas de Hoje</Text>
                    </div>
                    <Text fw={500} className='fw-bold' style={{color:'white'}}>0</Text>
                    </Card>
                    <Card w={250} style={{ backgroundColor:'#2d2c2c'}} shadow='sw'>
                    <div className='inputs-home'>
                        <Text style={{color:'white'}}>a</Text>
                        <Text fw={500} style={{color:'white'}}>Vendas de Hoje</Text>
                    </div>
                    <Text fw={500} className='fw-bold' style={{color:'white'}}>0</Text>
                    </Card>
                </div>                    
            </Stack>
        </div>
        </>
    )
}
export default Home