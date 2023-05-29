//
//  TagClusterView.swift
//  dump2
//
//  Created by Griffin Tarpenning on 5/29/23.
//

import SwiftUI

struct Tag: Hashable {
    let value: String
    let clicked: Bool
}

struct TagClusterView: View {
    
    var text: String = ""  // Defaults to None
    var tags: [Tag]
    
    var body: some View {
        VStack(alignment : .center) {
            if text != "" {
                Text(text)
                    .font(.system(size:30))
                    .foregroundColor(.gray)
            }
            Text("Tags:")
                .font(.system(size:30, weight: .bold))
            
            ForEach(tags, id: \.self) { tag in
                TagRowView(tag: tag.value, clicked: tag.clicked)
            }
        }
    }
}

let text = "This is some basic text"
let tags = [
    Tag(value: "tag1", clicked: true),
    Tag(value: "tag2", clicked: false),
    Tag(value: "long tag 1", clicked: true),
]

struct TagClusterView_Previews: PreviewProvider {
    
    static var previews: some View {
        TagClusterView(text: text, tags: tags)
    }
}
