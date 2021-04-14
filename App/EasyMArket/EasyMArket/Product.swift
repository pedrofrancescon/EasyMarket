//
//  Product.swift
//  EasyMArket
//
//  Created by Viviane Lima Bonfim Moroni de Souza on 13/04/21.
//

import Foundation


struct Product: Hashable, Codable, Identifiable {
    var id: Int
    var name: String
    var price: String
    var quantity: String
    var description: String

}
