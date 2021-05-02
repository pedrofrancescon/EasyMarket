//
//  Product.swift
//  EasyMArket
//
//  Created by Viviane Lima Bonfim Moroni de Souza on 13/04/21.
//

import Foundation


struct Product: Codable, Identifiable {
    let id = UUID()
    let amount: Int
    let name: String
    let price: Int

}
