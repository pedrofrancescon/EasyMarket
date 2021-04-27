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
}
