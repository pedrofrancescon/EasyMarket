//
//  PaymentMethodView.swift
//  EasyMArket
//
//  Created by Viviane Lima Bonfim Moroni de Souza on 13/04/21.
//

import SwiftUI

struct PaymentMethodView: View {
    @State private var cardNumber = ""
    @State private var cvv = ""
    var body: some View {
        VStack {
            Text("Bem vindo ao Easy Market")
                            .font(.largeTitle).foregroundColor(Color.white)
                            .padding([.top, .bottom], 40)
                            .shadow(radius: 10.0, x: 20, y: 10)
            
            Text("Agora cadatre um meio de pagamento")
                .padding()
            
            VStack(alignment: .leading, spacing: 15) {
                TextField("Número do Cartão", text: self.$cardNumber)
                    .padding()
                    .background(Color.themeTextField)
                    .cornerRadius(20.0)
                    .shadow(radius: 10.0, x: 20, y: 10)
                
                TextField("Nome do Titular", text: self.$cardNumber)
                    .padding()
                    .background(Color.themeTextField)
                    .cornerRadius(20.0)
                    .shadow(radius: 10.0, x: 20, y: 10)
                
                TextField("Validade", text: self.$cardNumber)
                    .padding()
                    .background(Color.themeTextField)
                    .cornerRadius(20.0)
                    .shadow(radius: 10.0, x: 20, y: 10)
                
                SecureField("Código de Segurança", text: self.$cvv)
                    .padding()
                    .background(Color.themeTextField)
                    .cornerRadius(20.0)
                    .shadow(radius: 10.0, x: 20, y: 10)
            }.padding([.leading, .trailing], 27.5)
            Spacer()
            Button(action: {}) {
                Text("Cadastrar")
                    .font(.headline)
                    .foregroundColor(.white)
                    .padding()
                    .frame(width: 300, height: 50)
                    .background(Color.green)
                    .cornerRadius(15.0)
                    .shadow(radius: 10.0, x: 20, y: 10)
            }.padding(.top, 50)
            
            Text("Está tendo algum problema?")
                .padding()
                
            
        }.background(
            LinearGradient(gradient: Gradient(colors: [.purple, .blue]), startPoint: .top, endPoint: .bottom)
                .edgesIgnoringSafeArea(.all))
    }
}


struct PaymentMethodView_Previews: PreviewProvider {
    static var previews: some View {
        PaymentMethodView()
    }
}
