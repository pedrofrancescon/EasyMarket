//
//  StartPurchaseView.swift
//  EasyMArket
//
//  Created by Viviane Lima Bonfim Moroni de Souza on 27/04/21.
//

import SwiftUI

struct StartPurchaseView: View {
    @State private var qrcode = ""
    var body: some View {
        VStack {
            Text("Bem vindo Pedro!")
                            .font(.largeTitle).foregroundColor(Color.blue)
                            .padding([.top, .bottom], 40)
                            .shadow(radius: 10.0, x: 20, y: 10)
            Text("Para iniciar uma compra escaneie o Código QR de um de nossos carrinhos")
                .padding()

            Spacer()
            
            NavigationLink(destination: CodeScannerView(codeTypes: [.qr]){result in }) {
                    Text("Escanear QR")
                        .buttonStyle(PlainButtonStyle())
                        .font(.headline)
                        .foregroundColor(.white)
                        .padding()
                        .frame(width: 300, height: 50)
                        .background(Color.green)
                        .cornerRadius(15.0)
                        .shadow(radius: 10.0, x: 20, y: 10)
            }.padding()
                
        
        }
    }
}

struct StartPurchaseView_Previews: PreviewProvider {
    static var previews: some View {
        StartPurchaseView()
    }
}
