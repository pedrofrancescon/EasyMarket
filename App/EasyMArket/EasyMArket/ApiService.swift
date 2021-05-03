//
//  ApiService.swift
//  EasyMArket
//
//  Created by Viviane Lima Bonfim Moroni de Souza on 25/04/21.
//

import Foundation

struct User: Codable, Identifiable {
    let id = UUID()
    let username: String
    let name: String
}


class apiCall {
    func getUsers(completion:@escaping ([User]) -> ()) {
        guard let url = URL(string: "https://jsonplaceholder.typicode.com/users") else { return }
        URLSession.shared.dataTask(with: url) { (data, _, _) in
            let users = try! JSONDecoder().decode([User].self, from: data!)
            print(users)
            
            DispatchQueue.main.async {
                completion(users)
            }
        }
        .resume()
    }
    
    func getProducts(completion:@escaping ([Product]) -> ()) {
        guard let url = URL(string: "http://localhost:8080/purchase") else { return }
        
        var request = URLRequest(url: url)
        
        let username = "pfcittolin@gmail.com"
        let password = "123456"
        let loginString = String(format: "%@:%@", username, password)
        let loginData = loginString.data(using: String.Encoding.utf8)!
        let base64LoginString = loginData.base64EncodedString()
        //if (base64LoginString != "cGZjaXR0b2xpbkBnbWFpbC5jb206MTIzNDU2"){print (base64LoginString)}
        request.setValue("application/json", forHTTPHeaderField: "accept")
        request.setValue("Basic \(base64LoginString)", forHTTPHeaderField: "Authorization")
        request.httpMethod = "GET"

        URLSession.shared.dataTask(with: request) { (data, _, _) in
            if (data != nil){
                let products = try! JSONDecoder().decode([Product].self, from: data!)
                print (products)
                DispatchQueue.main.async {
                    completion(products)
                }
            } else {
                return
            }
        }
        .resume()
    }
}
