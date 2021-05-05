//
//  FinishedPurchaseView.swift
//  EasyMArket
//
//  Created by Viviane Lima Bonfim Moroni de Souza on 04/05/21.
//

import SwiftUI

struct FinishedPurchaseView: View {
    var body: some View {
        VStack {
            Text("Compra finalizada!")
                .font(.largeTitle).foregroundColor(Color.blue)
                .padding(.top, 10)
                .padding(.bottom, 60)
            Text("Pagamento confirmado!")
                .foregroundColor(.green)
                .padding([.top, .bottom], 40)
            Text("✅")
                .font(.largeTitle)
                .padding(.bottom, 40)
                .shadow(radius: 10.0, x: 0, y: 10)
        }
    }
}

struct FinishedPurchaseView_Previews: PreviewProvider {
    static var previews: some View {
        FinishedPurchaseView()
    }
}
