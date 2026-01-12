import { Routes,Route } from "react-router-dom";
import Cadastro from "./pages/Cadastro";
import Produtos from './pages/Produto'
import Home from './pages/Home'
import AjusteProduto from "./pages/AjusteProduto";
import Vendas from "./pages/Vendas"


export default function RoutesApp(){
    return(
        <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/produtos" element={<Produtos />} />
            <Route path="/produto/cadastro" element={<Cadastro />} />
            <Route path="/produtos/ajuste/:id" element={<AjusteProduto />}/>
            <Route path="/vendas" element={<Vendas/>}/>
        </Routes>
    )
}