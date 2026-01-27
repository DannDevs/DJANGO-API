import { Link } from 'react-router-dom';
import './navbar.css';

function Navbar() {
    return (
        <>
            <nav className="navbar  nav-bar navbar-expand-lg fixed-top">
                <div className="container-fluid">
                    {/* Logo */}
                    <Link className="navbar-link fw-bold ms-3" to="/">
                        Logo
                    </Link>

                    {/* Botão hamburger */}
                    <button
                        className="navbar-toggler"
                        type="button"
                        data-bs-toggle="collapse"
                        data-bs-target="#navbarNav"
                        aria-controls="navbarNav"
                        aria-expanded="false"
                        aria-label="Toggle navigation"
                    >
                        <span className="navbar-toggler-icon"></span>
                    </button>

                    {/* Links do menu */}
                    <div className="collapse navbar-collapse" id="navbarNav">
                        <ul className="navbar-nav ms-auto gap-3 me-3">
                            <li className="nav-item">
                                <Link className="nav-link fw-bold" to="/">DashBoard</Link>
                            </li>
                            <li className="nav-item">
                                <Link className="nav-link fw-bold" to="/produtos">Produtos</Link>
                            </li>
                            <li className="nav-item">
                                <Link className="nav-link fw-bold" to="/vendas">Vendas</Link>
                            </li>
                            <li className="nav-item">
                                <Link className="nav-link fw-bold" to="/">Estoque</Link>
                            </li>
                            <li className="nav-item">
                                <Link className="nav-link fw-bold" to="/">Clientes</Link>
                            </li>
                            <li className="nav-item">
                                <Link className="nav-link fw-bold" to="/vendedores">Vendedores</Link>
                            </li>
                        </ul>
                    </div>
                </div>
            </nav>
        </>
    );
}

export default Navbar;
