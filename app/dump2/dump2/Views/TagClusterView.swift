//
//  TagClusterView.swift
//  dump2
//
//  Created by Griffin Tarpenning on 5/29/23.
//

import SwiftUI

public struct Tag: Hashable {
    let value: String
    var clicked: Bool
    var dates: [Date]
}

struct TagClusterView: View {
    
    var text: String = ""  // Defaults to None
    @State var tags: [Tag]
    
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
            
            ForEach(self.$tags, id: \.self) { tag in
                TagRowView(tag: tag)
            }
            Spacer()
        }
    }
}

let text = "This is some basic text"
let tags = [
    Tag(value: "tag1", clicked: true, dates: [Date()]),
    Tag(value: "tag2", clicked: false, dates: [Date()]),
    Tag(value: "long tag 1", clicked: true, dates: []),
]

struct TagClusterView_Previews: PreviewProvider {
    
    static var previews: some View {
        TagClusterView(text: text, tags: tags)
    }
}
