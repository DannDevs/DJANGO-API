import { Routes,Route } from "react-router-dom";
import Cadastro from "./pages/Cadastro.JSX";
import Produtos from './pages/Produto'
import Home from './pages/Home'


export default function RoutesApp(){
    return(
        <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/produtos" element={<Produtos />} />
            <Route path="/cadastro" element={<Cadastro />} />
        </Routes>
    )
}