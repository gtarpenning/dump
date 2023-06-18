//
//  TagRowView.swift
//  dump2
//
//  Created by Griffin Tarpenning on 5/29/23.
//

import SwiftUI

struct TagRowView: View {
    @Binding var tag: Tag
    
    var body: some View {
        ZStack {
            if tag.clicked {
                RoundedRectangle(cornerRadius: 25, style: .continuous)
                    .fill(.green)
                    .frame(width: self.getLen(text: tag.value), height: 25)
            } else {
                RoundedRectangle(cornerRadius: 25, style: .continuous)
                    .fill(.orange)
                    .frame(width: self.getLen(text: tag.value), height: 25)
            }
            Button(action: {tag.clicked = !tag.clicked}) {
                Text(tag.value)
                    .font(.system(size:18))
                    .foregroundColor(.white)
            }
        }
    }
    
    func getLen(text: String) -> CGFloat {
        var l = text.count
        
        // length adjustments
        if l < 6 {
            l += 1
        } else if l > 30 {
            l -= 5
        } else if l > 20 {
            l -= 3
        } else if l > 12 {
            l -= 1
        }
        
        return CGFloat(l * 11)
    }
}

struct TagRowView_Previews: PreviewProvider {
    
    @State static var testTag = Tag(value: "running", clicked: true, dates: [Date()])
    
    static var previews: some View {
        TagRowView(tag: $testTag)
    }
}
