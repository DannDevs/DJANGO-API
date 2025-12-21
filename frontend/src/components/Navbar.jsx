

import './navbar.css'

function Navbar(){
    return (
        <>
        <nav className='navbar navbar-expand-lg navbar-dark bg-dark fixed-top'>
            <div className='me-4'>
                <h2 className='fw-bold gap-2 ms-3'>Logo</h2>
            </div>
            <div>
                <ul className='navbar-nav ms-auto gap-3'>
                    <li className='nav=item'><a className='nav-link active fw-bold' href="/">Home</a></li>
                    <li className='nav=item'><a className='nav-link active fw-bold' href="/">Produtos</a></li>
                    <li className='nav=item'><a className='nav-link active fw-bold' href="/">Link</a></li>
                </ul>
            </div>
        </nav>
        </>
    )

}

export default Navbar
