//
//  TagModel.swift
//  dump2
//
//  Created by Jonathan Morales on 6/28/23.
//

import Foundation

struct Tag: Hashable {
    let value: String
    var clicked: Bool
    var dates: [Date]
}

