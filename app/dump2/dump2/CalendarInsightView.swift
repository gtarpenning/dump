//
//  CalendarInsightView.swift
//  dump2
//
//  Created by Griffin Tarpenning on 6/17/23.
//

import SwiftUI

struct CalendarInsightView: View {
    
    var selectedTags: [Tag] = []
    
    var body: some View {
        VStack {
            CalendarContentView(
                calendar: Calendar(identifier: .gregorian),
                dates: selectedDates()
            )
//            TagSelectorView(selectedTags)
//            TagClusterView(tags: self.selectedTags)
            Spacer()
            ForEach(tags, id: \.self) { tag in
                TagRowView(tag: tag.value, clicked: tag.clicked)
            }
            Spacer()
        }
    }
    
    func selectedDates() -> [Date] {
        return self.selectedTags.filter({ $0.date != nil }).map({ $0.date! })
    }
}

let testTags = [
    Tag(value: "tag1", clicked: true, date: Date()),
    Tag(value: "tag2", clicked: false, date: Date()),
    Tag(value: "long tag 1", clicked: true, date: nil),
]


struct CalendarInsightView_Previews: PreviewProvider {
    static var previews: some View {
        CalendarInsightView(selectedTags: testTags)
    }
}
