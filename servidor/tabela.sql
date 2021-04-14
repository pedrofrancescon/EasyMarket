/*
IDComprador - Unique ID por comprador, criado quando uma conta de usuario é criada
NomeComprador - autoexplanatorio
IDCompra - Unique ID de uma visita ao supermercado, criada quando o app se conecta a um carrinho e emseguida ao servidor e inicia a compra
IDCarrinho - Um identificador unico por carrinho. Uma QR code colada no carrinho talvez? a tinha planejado isso ja?
IDCelular - Algum identificador unico por celular. To meio incerto quanto a esse item ainda.
Quantidade - Numero de items nesse carrinho/compra
RFIDCode - Unique ID por tipo de item vendido, a tag RFID do item
NomeItem, PreçoItem, PesoItem - nome, peso e preço de cada tipo de item vendido.
*/

CREATE TABLE "Compra" ( "Comprador" INTEGER, "Celular" INTEGER, "Carrinho" INTEGER, FOREIGN KEY("Comprador") REFERENCES "Comprador" )
CREATE TABLE "Comprador" ( "Nome" TEXT NOT NULL, "Senha" TEXT NOT NULL )
CREATE TABLE "Item" ( "RFIDCode" INTEGER NOT NULL UNIQUE, "Nome" TEXT NOT NULL, "Peso" INTEGER NOT NULL, "Preço" INTEGER NOT NULL, PRIMARY KEY("RFIDCode") )
CREATE TABLE "ItemCompra" ( "Compra" INTEGER, "Item" INTEGER, "Quantidade" INTEGER, FOREIGN KEY("Item") REFERENCES "Item", PRIMARY KEY("Item","Compra"), FOREIGN KEY("Compra") REFERENCES "Compra" )
