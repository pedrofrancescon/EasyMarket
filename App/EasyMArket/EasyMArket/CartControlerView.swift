//
//  ChartControlerView.swift
//  EasyMArket
//
//  Created by Viviane Lima Bonfim Moroni de Souza on 14/04/21.
//

import SwiftUI

struct ChartControlerView: View {
    var body: some View {
        VStack {
            VStack {
                VStack {
                    Text("Seu carrinho")
                        .font(.largeTitle).foregroundColor(Color.white)
                        .padding()
                        .shadow(radius: 10.0, x: 20, y: 10)
                    Button(action: {}) {
                        Text("ˆ")
                            .font(.headline)
                            .foregroundColor(.white)
                            .padding()
                            .frame(width: 80, height: 80)
                            .background(Color.gray)
                            .cornerRadius(15.0)
                            .shadow(radius: 10.0, x: 0, y: 5)
                    }.padding(.top, 50)
                    HStack(spacing: 0) {
                        Button(action: {}) {
                            Text("<")
                                .font(.headline)
                                .foregroundColor(.white)
                                .padding()
                                .frame(width: 80, height: 80)
                                .background(Color.gray)
                                .cornerRadius(15.0)
                                .shadow(radius: 10.0, x: -5, y: 5)
                        }.padding(.top, 50)
                        Button(action: {}) {
                            Text("")
                                .font(.headline)
                                .foregroundColor(.white)
                                .padding()
                                .frame(width: 50, height: 50)
                                .background(Color.clear)
                                .cornerRadius(15.0)
                                .shadow(radius: 10.0, x: 20, y: 10)
                        }.padding(.horizontal, 50)
                        Button(action: {}) {
                            Text(">")
                                .font(.headline)
                                .foregroundColor(.white)
                                .padding()
                                .frame(width: 80, height: 80)
                                .background(Color.gray)
                                .cornerRadius(15.0)
                                .shadow(radius: 10.0, x: 5, y: 5)
                        }.padding(.top, 50)
                    }
                    Spacer()
                    Button(action: {}) {
                        Text("Voltar a compra")
                            .font(.headline)
                            .foregroundColor(.white)
                            .padding()
                            .frame(width: 380, height: 50)
                            .background(Color.gray)
                            .cornerRadius(15.0)
                            .shadow(radius: 10.0, x: 20, y: 10)
                    }.padding(50)
                }.background(
                    LinearGradient(gradient: Gradient(colors: [.blue, .white]), startPoint: .top, endPoint: .bottom)
                    .edgesIgnoringSafeArea(.all))
                
            }
            
        }
    }
}

struct ChartControlerView_Previews: PreviewProvider {
    static var previews: some View {
        ChartControlerView()
    }
}
