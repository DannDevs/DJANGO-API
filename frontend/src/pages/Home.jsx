import './Home.css'
import Navbar from '../components/Navbar'
import { Card, Group, Text, useMantineTheme } from '@mantine/core';

function Home(){
    return(
        <>
        <Navbar />
        <div>
            <h2>Olá Usuario</h2>
        </div>
        </>
    )
}
export default Home