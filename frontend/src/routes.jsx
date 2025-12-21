import { Routes,Route } from "react-router-dom";
import Produtos from './pages/App'
import Cadastro from './pages/Cadastro'


export default function RoutesApp(){
    return(
        <Routes>
            <Route path="/" element={<Produtos />} />
            <Route path="/cadastro" element={<Cadastro />} />
        </Routes>
    )
}