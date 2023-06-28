//
//  CalendarInsightView.swift
//  dump2
//
//  Created by Griffin Tarpenning on 6/17/23.
//

import SwiftUI

struct CalendarInsightView: View {
  @State var selectedTags: [Tag] = []

  var body: some View {
    VStack {
      CalendarContentView(
        calendar: Calendar(identifier: .gregorian),
        tags: $selectedTags
      )
      Spacer()
        if !selectedTags.isEmpty {
            TagClusterView(tags: selectedTags)
        }
      Spacer()
    }
  }
}

struct CalendarInsightView_Previews: PreviewProvider {
  static var calendar = Calendar(identifier: .gregorian)
  static var formatter = DateFormatter(dateFormat: "yyyy/MM/dd", calendar: calendar)

  static var testTags = [
    Tag(value: "tag1", clicked: false, dates: [
        formatter.date(from: "2023/06/12")!,
        formatter.date(from: "2023/06/13")!,
        formatter.date(from: "2023/06/14")!,
        formatter.date(from: "2023/06/16")!,
    ]),
    Tag(value: "tag 1234", clicked: false, dates: [
        formatter.date(from: "2023/06/01")!,
        formatter.date(from: "2023/06/02")!,
        formatter.date(from: "2023/06/04")!,
        formatter.date(from: "2023/06/06")!,
        formatter.date(from: "2023/06/09")!,
        formatter.date(from: "2023/06/012")!,
        formatter.date(from: "2023/06/014")!,
    ]),
    Tag(value: "long tag 1", clicked: false, dates: [
        formatter.date(from: "2023/06/16")!,
        formatter.date(from: "2023/06/14")!,
    ])
]

  static var previews: some View {
      CalendarInsightView(selectedTags: testTags)
  }
}
