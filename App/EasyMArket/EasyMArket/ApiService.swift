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
    func getUser(completion:@escaping (User) -> ()) {
        guard let url = URL(string: "http://localhost:8080/user") else { return }
        URLSession.shared.dataTask(with: url) { (data, _, _) in
            let user = try! JSONDecoder().decode(User.self, from: data!)
            print(user)
            
            DispatchQueue.main.async {
                completion(user)
            }
        }
        .resume()
    }
    
    func getProducts(completion:@escaping ([Product]) -> ()) {
        guard let url = URL(string: "http://localhost:8080/purchase/") else { return }
        var request = URLRequest(url: url)
        request.setValue(<#T##value: String?##String?#>, forHTTPHeaderField: <#T##String#>)
        //let requestbody = ["login":"pfcitollin@gmail.com", "senha":"123456"]
        //let bodyData = try? JSONSerialization.data(withJSONObject: requestbody, options: [])
        request.httpMethod = "GET"
        URLSession.shared.dataTask(with: request) { (data, _, _) in
            let products = try! JSONDecoder().decode([Product].self, from: data!)
            print(products)
            
            DispatchQueue.main.async {
                completion(products)
            }
        }
        .resume()
    }
}
