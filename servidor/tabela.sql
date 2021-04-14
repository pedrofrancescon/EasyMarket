CREATE TABLE "Compra" ( "Comprador" INTEGER, "Celular" INTEGER, "Carrinho" INTEGER, FOREIGN KEY("Comprador") REFERENCES "Comprador" )
CREATE TABLE "Comprador" ( "Nome" TEXT NOT NULL, "Senha" TEXT NOT NULL )
CREATE TABLE "Item" ( "RFIDCode" INTEGER NOT NULL UNIQUE, "Nome" TEXT NOT NULL, "Peso" INTEGER NOT NULL, "Preço" INTEGER NOT NULL, PRIMARY KEY("RFIDCode") )
CREATE TABLE "ItemCompra" ( "Compra" INTEGER, "Item" INTEGER, "Quantidade" INTEGER, FOREIGN KEY("Item") REFERENCES "Item", PRIMARY KEY("Item","Compra"), FOREIGN KEY("Compra") REFERENCES "Compra" )
