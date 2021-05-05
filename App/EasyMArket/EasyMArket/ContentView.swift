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
    @State private var taped: Int? = 0
    @State var products: [Product] = []
    
    var body: some View {
        NavigationView {
            VStack {
            Text("Easy Market")
                            .font(.largeTitle).foregroundColor(Color.blue)
                            .padding([.top, .bottom], 40)
                            .shadow(radius: 10.0, x: 0, y: 10)
                        
                        Image("cart")
                            .resizable()
                            .frame(width: 250, height: 250)
                            .clipShape(Circle())
                            .overlay(Circle().stroke(Color.white, lineWidth: 4))
                            .shadow(radius: 10.0, x: 0, y: 10)
                            .padding(.bottom, 50)
                        
                        VStack(alignment: .leading, spacing: 15) {
                            TextField("Email", text: self.$email)
                                .padding()
                                .background(Color.themeTextField)
                                .cornerRadius(10.0)
                                .shadow(radius: 10.0, x: 0, y: 10)
                            
                            SecureField("Senha", text: self.$password)
                                .padding()
                                .background(Color.themeTextField)
                                .cornerRadius(10.0)
                                .shadow(radius: 10.0, x: 0, y: 10)
                        }.padding([.leading, .trailing], 27.5)
                        
            
                NavigationLink(destination: StartPurchaseView(), tag: 1, selection: $taped) {
            }
                    Text("Entrar")
                        .buttonStyle(PlainButtonStyle())
                        .font(.headline)
                        .foregroundColor(.white)
                        .padding()
                        .frame(width: 300, height: 50)
                        .background(Color.green)
                        .cornerRadius(10.0)
                        .shadow(radius: 10.0, x: 0, y: 10)
                        .padding()
                        .onTapGesture {
                            //let username = "pfcittolin@gmail.com"
                            //let password = "123456"
                            let loginString = String(format: "%@:%@", email, password)
                            let loginData = loginString.data(using: String.Encoding.utf8)!
                            let base64LoginString = loginData.base64EncodedString()
                            LoginSettings.loginBase64 = base64LoginString
                            
                            apiCall().getProducts { (products) in
                                self.products = products
                                self.taped = 1
                            }
                        }
                        
                        Spacer()
                        HStack(spacing: 0) {
                            Text("Don't have an account? ")
                            Button(action: {
                            }) {
                                Text("Sign Up")
                                    .foregroundColor(.black)
                            }
                        }
                    }
                    .background(Color.white)
            
        }
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

