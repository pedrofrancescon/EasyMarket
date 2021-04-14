//
//  CartView.swift
//  EasyMArket
//
//  Created by Viviane Lima Bonfim Moroni de Souza on 13/04/21.
//

import SwiftUI

struct CartView: View {
    var body: some View {
        VStack {
            Text("Seu carrinho")
                .font(.largeTitle).foregroundColor(Color.white)
                .padding()
                .shadow(radius: 10.0, x: 20, y: 10)
            VStack {
                HStack(spacing: 0) {
                    Text("Item 01   ")
                        .padding()
                        .padding(.leading, 10)
                        .padding(.trailing, 180)
                        .background(Color.themeTextField)
                        .cornerRadius(10.0)
                        .shadow(radius: 10.0, x: 20, y: 10)
                    Text("15,00")
                        .padding()
                        .padding([.leading, .trailing], 10)
                        .background(Color.themeTextField)
                        .cornerRadius(10.0)
                        .shadow(radius: 10.0, x: 20, y: 10)
                }
                HStack(spacing: 0) {
                    Text("Item 02   ")
                        .padding()
                        .padding(.leading, 10)
                        .padding(.trailing, 180)
                        .background(Color.themeTextField)
                        .cornerRadius(10.0)
                        .shadow(radius: 10.0, x: 20, y: 10)
                    Text("10,00")
                        .padding()
                        .padding([.leading, .trailing], 10)
                        .background(Color.themeTextField)
                        .cornerRadius(10.0)
                        .shadow(radius: 10.0, x: 20, y: 10)
                }
                HStack(spacing: 0) {
                    Text("Item 03   ")
                        .padding()
                        .padding(.leading, 10)
                        .padding(.trailing, 180)
                        .background(Color.themeTextField)
                        .cornerRadius(10.0)
                        .shadow(radius: 10.0, x: 20, y: 10)
                    Text("07,50")
                        .padding()
                        .padding([.leading, .trailing], 10)
                        .background(Color.themeTextField)
                        .cornerRadius(10.0)
                        .shadow(radius: 10.0, x: 20, y: 10)
                }
            }.padding()
            Spacer()
            HStack(spacing: 0) {
                Text("Total   ")
                .padding()
                .padding(.leading, 10)
                .padding(.trailing, 180)
                .background(Color.themeTextField)
                .cornerRadius(20.0)
                .shadow(radius: 10.0, x: 20, y: 10)
                Text("32,50")
                    .padding()
                    .padding([.leading, .trailing], 10)
                    .background(Color.themeTextField)
                    .cornerRadius(20.0)
                    .shadow(radius: 10.0, x: 20, y: 10)}
            Text("Está tendo algum problema?")
                .padding()
                
            
        
        }.background(
            LinearGradient(gradient: Gradient(colors: [.blue, .white]), startPoint: .top, endPoint: .bottom)
                .edgesIgnoringSafeArea(.all))
    }
}



struct CartView_Previews: PreviewProvider {
    static var previews: some View {
        CartView()
    }
}
