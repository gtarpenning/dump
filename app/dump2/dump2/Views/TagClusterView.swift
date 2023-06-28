//
//  TagClusterView.swift
//  dump2
//
//  Created by Griffin Tarpenning on 5/29/23.
//

import SwiftUI

struct TagClusterView: View {
  var text: String = ""
  @State var tags: [Tag]

  var body: some View {
    VStack(alignment: .center) {
      Spacer()
      if !text.isEmpty {
        Text(text)
          .font(.system(size: 30))
          .foregroundColor(.gray)
      }
      Spacer()
      Text("Tags:")
        .font(.system(size: 30, weight: .bold))

      ScrollView(.vertical) {
        VStack(spacing: 15) {
          ForEach(tags.indices, id: \.self) { index in
            TagView(tag: $tags[index])
          }
        }
        .padding(.vertical)
      }
      Spacer()
    }
  }
}

struct TagClusterView_Previews: PreviewProvider {
  static var previews: some View {
    let tags = [
      Tag(value: "tag1", clicked: true, dates: [Date()]),
      Tag(value: "tag2", clicked: false, dates: [Date()]),
      Tag(value: "very long tag 1", clicked: true, dates: []),
    ]
    return TagClusterView(tags: tags)
  }
}
