//
//  CheckoutView.swift
//  EasyMArket
//
//  Created by Viviane Lima Bonfim Moroni de Souza on 14/04/21.
//

import SwiftUI

struct CheckoutView: View {
    var body: some View {
        VStack {
            Text("Compra finalizada")
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
                    .foregroundColor(.green)
                    .background(Color.themeTextField)
                    .cornerRadius(20.0)
                    .shadow(radius: 10.0, x: 20, y: 10)}
            Spacer()
            Text("Seu pagamento foi aceito!")
                    .foregroundColor(.black)
            Button(action: {}) {
                Text("✔️")
                    .font(.headline)
                    .foregroundColor(.white)
                    .padding()
                    .frame(width: 80, height: 80)
                    .background(Color.green)
                    .cornerRadius(15.0)
                    .shadow(radius: 10.0, x: 0, y: 5)
            }.padding(.bottom, 50)
                
            
        
        }.background(
            LinearGradient(gradient: Gradient(colors: [.blue, .white]), startPoint: .top, endPoint: .bottom)
                .edgesIgnoringSafeArea(.all))
    }
    
}

struct CheckoutView_Previews: PreviewProvider {
    static var previews: some View {
        CheckoutView()
    }
}
