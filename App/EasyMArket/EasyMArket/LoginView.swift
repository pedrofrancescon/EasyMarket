//
//  ContentView.swift
//  EasyMArket
//
//  Created by Viviane Lima Bonfim Moroni de Souza on 13/04/21.
//

import SwiftUI


struct ContentView: View {
    @State private var email = ""
    @State private var password = ""
    var body: some View {
        VStack {
            Text("Easy Market")
                            .font(.largeTitle).foregroundColor(Color.white)
                            .padding([.top, .bottom], 40)
                            .shadow(radius: 10.0, x: 20, y: 10)
                        
                        Image("cart")
                            .resizable()
                            .frame(width: 250, height: 250)
                            .clipShape(Circle())
                            .overlay(Circle().stroke(Color.white, lineWidth: 4))
                            .shadow(radius: 10.0, x: 20, y: 10)
                            .padding(.bottom, 50)
                        
                        VStack(alignment: .leading, spacing: 15) {
                            TextField("Email", text: self.$email)
                                .padding()
                                .background(Color.themeTextField)
                                .cornerRadius(20.0)
                                .shadow(radius: 10.0, x: 20, y: 10)
                            
                            SecureField("Senha", text: self.$password)
                                .padding()
                                .background(Color.themeTextField)
                                .cornerRadius(20.0)
                                .shadow(radius: 10.0, x: 20, y: 10)
                        }.padding([.leading, .trailing], 27.5)
                        
                        Button(action: {}) {
                            Text("Entrar")
                                .font(.headline)
                                .foregroundColor(.white)
                                .padding()
                                .frame(width: 300, height: 50)
                                .background(Color.green)
                                .cornerRadius(15.0)
                                .shadow(radius: 10.0, x: 20, y: 10)
                        }.padding(.top, 50)
                        
                        Spacer()
                        HStack(spacing: 0) {
                            Text("Don't have an account? ")
                            Button(action: {}) {
                                Text("Sign Up")
                                    .foregroundColor(.black)
                            }
                        }
                    }
                    .background(
                        LinearGradient(gradient: Gradient(colors: [.blue, .white]), startPoint: .top, endPoint: .bottom)
                            .edgesIgnoringSafeArea(.all))
                    
            
        }
    }


struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}

extension Color {
    static var themeTextField: Color {
        return Color(red: 220.0/255.0, green: 230.0/255.0, blue: 230.0/255.0, opacity: 1.0)
    }
}

