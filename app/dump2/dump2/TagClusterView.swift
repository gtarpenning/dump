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
    let date: Date?
}

struct TagClusterView: View {
    
    var text: String = ""  // Defaults to None
    var tags: [Tag]
    
    var body: some View {
        VStack(alignment : .center) {
            Spacer()
            if text != "" {
                Text(text)
                    .font(.system(size:30))
                    .foregroundColor(.gray)
            }
            Spacer()
            Text("Tags:")
                .font(.system(size:30, weight: .bold))
            
            ForEach(tags, id: \.self) { tag in
                TagRowView(tag: tag.value, clicked: tag.clicked)
            }
            Spacer()
        }
    }
}

let text = "This is some basic text"
let tags = [
    Tag(value: "tag1", clicked: true, date: Date()),
    Tag(value: "tag2", clicked: false, date: Date()),
    Tag(value: "long tag 1", clicked: true, date: nil),
]

struct TagClusterView_Previews: PreviewProvider {
    
    static var previews: some View {
        TagClusterView(text: text, tags: tags)
    }
}
