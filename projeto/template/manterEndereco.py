import streamlit as st
import pandas as pd
from views.clienteView import ClienteView
from views.enderecoView import EnderecoView
import time
from utils import sucesso_mensagem


class ManterEnderecoUI:
    def main():
        st.header("Meus enderecos")
        tab1, tab2, tab3, tab4 = st.tabs(
            ["Listar", "Cadastrar", "Atualizar", "Excluir"]
        )

        with tab1:
            ManterEnderecoUI.listar()
        with tab2:
            ManterEnderecoUI.cadastrar()
        with tab3:
            ManterEnderecoUI.atualizar()
        with tab4:
            ManterEnderecoUI.excluir()

    def listar():
        st.subheader("Endereços")
        try:
            enderecos = EnderecoView.endereco_listar()

            if len(enderecos) == 0:
                st.warning("Nenhum endereço cadastrado")
            else:
                ender_list_dict = []

                for obj in enderecos:
                    ender_list_dict.append(obj.to_json())

                df = pd.DataFrame(ender_list_dict)
                st.dataframe(
                    df,
                    hide_index=True,
                    column_order=[
                        "id",
                        "logradouro",
                        "numero",
                        "cidade",
                        "estado",
                    ],
                )
        except ValueError as e:
            st.warning(e)

    def cadastrar():
        st.subheader("Cadastrar")
        logradouro = st.text_input("Logradouro")
        num_casa = st.text_input("Número")
        complemento = st.text_input("Complemento")
        bairro = st.text_input("Bairro")
        cidade = st.text_input("Cidade")
        estado = st.text_input("Estado")
        cep = st.text_input("CEP")
        cli = st.session_state["cliente_id"]

        if st.button("Cadastrar"):
            try:
                EnderecoView.endereco_inserir(
                    logradouro,
                    num_casa,
                    complemento,
                    bairro,
                    cidade,
                    estado,
                    cep,
                    cli,
                )
                sucesso_mensagem("Endereço")

            except ValueError as e:
                st.warning(e)

    def atualizar():
        st.subheader("Atualizar")

        enderecos = EnderecoView.endereco_listar()

        if len(enderecos) == 0:
            st.write("Nenhum endereço cadastrado")

        else:
            op = st.selectbox(
                "Atualização do endereço",
                enderecos,
                index=None,
                placeholder="Selecione um endereço",
            )
            if op is not None:
                logradouro = st.text_input("Novo logradouro", op.getLogradouro())
                num_casa = st.text_input("Novo número", op.getNumero())
                complemento = st.text_input("Novo complemento", op.getComplemento())
                bairro = st.text_input("Novo bairro", op.getBairro())
                cidade = st.text_input("Nova cidade", op.getCidade())
                estado = st.text_input("Novo Estado", op.getEstado())
                cep = st.text_input("Novo CEP", op.getCep())
                cli = st.session_state["cliente_id"]

                if st.button("Atualizar"):
                    try:
                        id_endereco = op.getId()
                        EnderecoView.endereco_atualizar(
                            id_endereco,
                            logradouro,
                            num_casa,
                            complemento,
                            bairro,
                            cidade,
                            estado,
                            cep,
                            cli,
                        )
                        sucesso_mensagem("Endereço")

                    except ValueError as e:
                        st.warning(e)

    def excluir():
        st.subheader("Excluir")
        enderecos = EnderecoView.endereco_listar()
        op = st.selectbox("Excluir endereço", enderecos)

        if st.button("Excluir"):
            try:
                EnderecoView.endereco_excluir(op.getId())
                sucesso_mensagem("Endereço")
            except ValueError as e:
                st.warning(e)
