

const carregarclientes = () => {
    fetch("http://127.0.0.1:8000/clientes/")
        .then(res => {
            if (!res.ok) {
                console.log("Nao foi possivel conectar")
                return
            }
            return res.json()
        })
        .then(data => {
            console.log(data)
        })
        .catch(error => {
            console.log("Nao foi possivel conectar" + " " + error)
        })
}

carregarclientes()