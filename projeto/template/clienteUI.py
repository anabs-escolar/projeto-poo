import streamlit as st
import pandas as pd
from views.produtoView import ProdutoView
from views.enderecoView import EnderecoView
from views.vendaView import VendaView
from datetime import datetime
import time


class ClienteUI:
    def carrinho():
        st.header("Carrinho")
        tab1, tab2 = st.tabs(["Inserir produto", "Visualizar"])

        with tab1:
            ClienteUI.inserir_produto_carrinho()
        with tab2:
            ClienteUI.visualizar_carrinho()

    def inserir_produto_carrinho():
        st.subheader("Inserir produto no carrinho")
        carrinho = VendaView.carrinho_visualizar(
            cliente_id=st.session_state["cliente_id"]
        )

        produtos = ProdutoView.produto_listar()
        produto = st.selectbox("Produto", produtos)
        qtd = st.number_input("Quantidade", value=1)

        if st.button("Inserir"):

            if carrinho["carrinho"] != None:
                VendaView.carrinho_inserir(
                    data="",
                    carrinho=True,
                    cliente_id=st.session_state["cliente_id"],
                    produto_id=produto.getId(),
                    qtd=qtd,
                )

                st.success("Produto inserido com sucesso")
                time.sleep(2)
                st.rerun()

            else:
                data = datetime.now()
                carrinho = True

                VendaView.carrinho_inserir(
                    data=data,
                    carrinho=carrinho,
                    cliente_id=st.session_state["cliente_id"],
                    produto_id=produto.getId(),
                    qtd=qtd,
                )
                st.success("Produto inserido com sucesso")
                time.sleep(2)
                st.rerun()

    def visualizar_carrinho():
        st.subheader("Seu carrinho")

        dados = VendaView.carrinho_visualizar(cliente_id=st.session_state["cliente_id"])

        if dados["carrinho"] is not None:

            carrinho = dados["carrinho"]
            cliente = carrinho.getCliente()
            data = carrinho.getData().strftime("%d/%m/%Y")

            preco_total = 0
            prod_list_dict = []

            for item in dados["itens"]:

                subtotal = item.getQtd() * item.getPreco()
                preco_total += subtotal

                produto_nome = "Produto não encontrado"
                for prod in dados["produtos"]:
                    if prod.getId() == item.getProduto():
                        produto_nome = prod.getDescricao()
                        break

                prod_list_dict.append(
                    {
                        "produto": produto_nome,
                        "quantidade": item.getQtd(),
                        "preco_unitario": item.getPreco(),
                        "subtotal": subtotal,
                    }
                )

            st.write(f"Carrinho: Cliente: {cliente} - Criação do carrinho: {data}")

            df = pd.DataFrame(prod_list_dict)
            st.dataframe(
                df,
                hide_index=True,
                column_order=["produto", "quantidade", "preco_unitario", "subtotal"],
            )

            st.write(f"Total: R$ {preco_total:.2f}")

            enderecos = EnderecoView.endereco_listar_por_cliente(
                st.session_state["cliente_id"]
            )

            endereco_selecionado = st.selectbox(
                "Endereço de entrega",
                enderecos,
                index=None,
                placeholder="Selecione um endereço",
            )

            if st.button("Finalizar compra"):
                if endereco_selecionado is None:
                    st.warning("Selecione um endereço para entrega")
                    return

                VendaView.carrinho_comprar(
                    cliente_id=st.session_state["cliente_id"],
                    endereco_id=endereco_selecionado.getId(),
                    comprar=True,
                )

                st.success("Compra finalizada")
                time.sleep(2)
                st.rerun()

            if st.button("Esvaziar carrinho"):
                VendaView.carrinho_esvaziar(st.session_state["cliente_id"])
                st.success("Esvaziando...")
                time.sleep(2)
                st.rerun()

        else:
            st.write("Carrinho vazio")

    def listar_minhas_compras():
        st.subheader("Minhas compras")

        dados = VendaView.vendas_listar(
            is_carrinho=False, cliente_id=st.session_state["cliente_id"]
        )

        enderecos = EnderecoView.endereco_listar()

        for venda in dados["vendas"]:
            prod_list_dict = []
            preco_total = 0

            cliente = st.session_state["cliente_nome"]
            data = venda.getData().strftime("%d/%m/%Y")
            venda_id = venda.getId()

            # 🔹 Resolver endereço da venda
            endereco_str = "Endereço não informado"
            if venda.getEndereco() is not None:
                for end in enderecos:
                    if end.getId() == venda.getEndereco():
                        endereco_str = str(end)
                        break

            for item in dados["itens"]:
                if item.getVenda() == venda_id:

                    subtotal = item.getQtd() * item.getPreco()
                    preco_total += subtotal

                    produto_nome = "Produto não encontrado"
                    for prod in dados["produtos"]:
                        if prod.getId() == item.getProduto():
                            produto_nome = prod.getDescricao()
                            break

                    prod_list_dict.append(
                        {
                            "produto": produto_nome,
                            "quantidade": item.getQtd(),
                            "preco_unitario": item.getPreco(),
                            "subtotal": subtotal,
                        }
                    )

            st.write(
                f"""
                **Data:** {data}  
                **Endereço de entrega:** {endereco_str}
                """
            )

            df = pd.DataFrame(prod_list_dict)
            st.dataframe(
                df,
                hide_index=True,
                column_order=["produto", "quantidade", "preco_unitario", "subtotal"],
            )

            st.write(f"**Total:** R$ {preco_total:.2f}")
            st.divider()
