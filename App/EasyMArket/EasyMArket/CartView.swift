//
//  CartView.swift
//  EasyMArket
//
//  Created by Viviane Lima Bonfim Moroni de Souza on 13/04/21.
//

import SwiftUI

struct CartView: View {
    @State var products: [Product] = []
    @State var subtotal: Int = 0
    var body: some View {
        VStack {
            Text("Acompanhe seu carrinho")
                .font(.title3).foregroundColor(Color.blue)
                .padding()
                .shadow(radius: 10.0, x: 0, y: 10)
            VStack {
                HStack(spacing: 0) {
                    Text("Descrição")
                        .frame(minWidth: 0, maxWidth: 200, minHeight: 0, maxHeight: 20)
                        .padding()
                        .padding(.trailing, 100)
                        .cornerRadius(5.0)
                        .shadow(radius: 10.0, x: 0, y: 10)
                    Text("Qtd")
                        .frame(minWidth: 0, maxWidth: 30, minHeight: 0, maxHeight: 20)

                    Text("Preço")
                        .frame(minWidth: 0, maxWidth: 80, minHeight: 0, maxHeight: 20)
                        .padding()
                        .padding([.leading, .trailing], 10)
                        .cornerRadius(5.0)
                        .shadow(radius: 10.0, x: 0, y: 10)
                }
                List(products) { product in
                    HStack(spacing: 0) {
                        Text(product.name)
                            .frame(minWidth: 0, maxWidth: 200, minHeight: 0, maxHeight: 200)
                            .padding()
                            .padding(.trailing, 100)
                            .shadow(radius: 10.0, x: 0, y: 10)
                        Text(String(product.amount))
                            .frame(minWidth: 0, maxWidth: 30, minHeight: 0, maxHeight: 20)
                        Text("R$ "+String(format: "%.2f", Float(product.amount*product.price/100)))
                            .frame(minWidth: 0, maxWidth: 80, minHeight: 0, maxHeight: 200)
                            .padding()
                            .shadow(radius: 10.0, x: 0, y: 10)
                        
                    }.onAppear{
                        subtotal = subtotal+(product.amount*product.price)
                    }
                    //subtotal = subtotal+(product.amount*product.price)
                }
                .onAppear
                    {
                    
                        apiCall().getProducts { (products) in
                            self.products = products
                        }
                    }
                    
            
                Spacer()
                HStack(spacing: 0) {
                    Text("Total")
                        .frame(minWidth: 0, maxWidth: 200, minHeight: 0, maxHeight: 20)
                        .padding()
                        .padding(.trailing, 180)
                    Text("R$ "+String(format: "%.2f", Float(subtotal/100)))
                        .frame(minWidth: 0, maxWidth: 80, minHeight: 0, maxHeight: 20)
                        .padding()

                }
                Text("Está tendo algum problema?")
                    .padding()


           
            }}
        }
    
}

struct CartView_Previews: PreviewProvider {
    static var previews: some View {
        CartView()
    }
}

