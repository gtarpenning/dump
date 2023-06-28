//
//  TagView.swift
//  dump2
//
//  Created by Jonathan Morales on 6/28/23.
//

import SwiftUI

struct TagView: View {
  @Binding var tag: Tag

  var body: some View {
    Button(action: {
      tag.clicked.toggle()
    }) {
      Text(tag.value)
        .font(.system(size: 20))
        .padding(.horizontal, 12)
        .padding(.vertical, 6)
        .background(tag.clicked ? Color.green : Color.orange)
        .foregroundColor(.white)
        .cornerRadius(20)
    }
  }
}

struct TagView_Previews: PreviewProvider {
  static var previews: some View {
    let tag = Tag(value: "tag1", clicked: false, dates: [])
    return TagView(tag: .constant(tag))
  }
}
