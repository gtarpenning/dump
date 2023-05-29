//
//  TagRowView.swift
//  dump2
//
//  Created by Griffin Tarpenning on 5/29/23.
//

import SwiftUI

struct TagRowView: View {
    var tag: String
    @State var clicked: Bool
    
    var body: some View {
        ZStack {
            if clicked {
                RoundedRectangle(cornerRadius: 25, style: .continuous)
                    .fill(.green)
                    .frame(width: self.getLen(tag: tag), height: 25)
            } else {
                RoundedRectangle(cornerRadius: 25, style: .continuous)
                    .fill(.orange)
                    .frame(width: self.getLen(tag: tag), height: 25)
            }
            Button(action: {clicked = !clicked}) {
                Text(tag)
                    .font(.system(size:18))
                    .foregroundColor(.white)
            }
        }
    }
    
    func getLen(tag: String) -> CGFloat {
        var l = tag.count
        
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
    static var previews: some View {
        TagRowView(tag: "running", clicked: true)
    }
}
