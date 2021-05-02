//
//  UserView.swift
//  EasyMArket
//
//  Created by Viviane Lima Bonfim Moroni de Souza on 25/04/21.
//

import SwiftUI

struct UserView: View {
    @State var users: [User] = []
    var body: some View {
        List(users) { user in
            Text(user.username)
               .font(.headline)
            Text(user.name)
               .font(.subheadline)
        }.onAppear {
            apiCall().getUsers { (users) in
                self.users = users
                }
        }
    }
}

struct UserView_Previews: PreviewProvider {
    static var previews: some View {
        UserView()
    }
}
