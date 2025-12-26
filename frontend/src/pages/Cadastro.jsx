import Navbar from "../components/navbar";
import { Link, useNavigate } from "react-router-dom";
import { useState } from "react"; 
import { showNotification } from "@mantine/notifications";
import { IconCheck, IconX } from '@tabler/icons-react';
import { Button } from "@mantine/core";


function Cadastro() {
  const [disabled, setDisable] = useState(false);
  const navigate = useNavigate();
  const [form, setForm] = useState({
    referencia: "",
    descricao: "",
    preco: "",
  });

  function handleChange(e) {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  }

  function handleSubmit(e) {
    e.preventDefault();
    setDisable(true);

    fetch("http://127.0.0.1:8000/produtos/cadastro/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form),
    })
      .then(res => {
        if (res.ok) {
          showNotification({
            title: 'Sucesso!',
            message: 'Produto cadastrado com sucesso.',
            color: 'green',
           styles: (theme) =>({
                closeButton:{
                    backgroundColor:'#202020',
                },
                root:{
                    backgroundColor:'#202020',
                    color:'#ffffffe5',
                },
                title:{
                    color:'#fff',
                },
            }),
            radius: 'md',
            autoClose: 3000,
            icon: <IconCheck />, 
          });
          navigate("/produtos");
        } else {
          showNotification({
            title: 'Erro',
            message: 'Erro ao cadastrar o produto.',
            color: 'red',
            radius: 'md',
            autoClose: 4000,
            styles: (theme) =>({
                closeButton:{
                    backgroundColor:'#202020',
                },
                root:{
                    backgroundColor:'#202020',
                    color:'#ffffffe5',
                },
                title:{
                    color:'#fff',
                },
            }),
            icon: <IconX size={20} />, 
          })
          setDisable(false);
        }
      })
      .catch(() => {
        showNotification({
          title: 'Erro!',
          message: 'Falha na conexão com o servidor.',
          color: 'red',
          icon: <IconX size={20} />,
          radius: 'md',
          autoClose: 4000,
                 styles: (theme) =>({
                closeButton:{
                    backgroundColor:'#202020',
                },
                root:{
                    backgroundColor:'#202020',
                    color:'#ffffffe5',
                },
                title:{
                    color:'#fff',
                },
            }),
        });
        setDisable(false);
      });
  }

  return (
    <>
      <div>
        <Navbar />
        <div className="acoes text-end mb-2 mt-3">
          <Link to="/produtos">
            <Button filled>Retornar</Button>
          </Link>
        </div>
        <div className="telacadastro">
          <div className="divisao-title">
            <h2 className="title">Cadastro Produto</h2>
          </div>
          <form className="form" onSubmit={handleSubmit}>
            <div className="inputs">
              <div className="divisaoinputs">
                <label className="fw-bold form-label-custom">Referencia</label>
                <input
                  className="input form-control-custom"
                  name="referencia"
                  onChange={handleChange}
                  type="text"
                />
              </div>
              <div className="divisaoinputs">
                <label className="fw-bold form-label-custom">Descrição</label>
                <input
                  onChange={handleChange}
                  name="descricao"
                  className="input form-control-custom"
                  type="text"
                  
                />
              </div>
              <div className="divisaoinputs">
                <label className="fw-bold form-label-custom">Preço</label>
                <input
                  onChange={handleChange}
                  name="preco"
                  className="input form-control-custom"
                  type="text"
                  
                />
              </div>
            </div>
            <div className="buttons">
              <button type="submit" disabled={disabled} className="button btn-sucess">
                {disabled ? 'Enviando...' : 'Cadastrar'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </>
  );
}

export default Cadastro;
