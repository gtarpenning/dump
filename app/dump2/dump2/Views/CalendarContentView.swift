//
//  CalendarView.swift
//  dump2
//
//  Created by Griffin Tarpenning on 6/17/23.
//

import SwiftUI

extension Calendar {
  func generateDates(
    inside interval: DateInterval,
    matching components: DateComponents
  ) -> [Date] {
    var dates: [Date] = []
    dates.append(interval.start)

    enumerateDates(
      startingAfter: interval.start,
      matching: components,
      matchingPolicy: .nextTime
    ) { date, _, stop in
      if let date = date {
        if date < interval.end {
          dates.append(date)
        } else {
          stop = true
        }
      }
    }
    return dates
  }
}

extension DateFormatter {
  static let monthAndYear: DateFormatter = {
    let formatter = DateFormatter()
    formatter.setLocalizedDateFormatFromTemplate("MMMM yyyy")
    return formatter
  }()
}

struct CalendarContentView: View {
  @Binding private var selectedTags: [Tag]

  @State var selectedDate = Self.now

  private let calendar: Calendar
  private let monthFormatter: DateFormatter
  private let dayFormatter: DateFormatter
  private let weekDayFormatter: DateFormatter
  private let fullFormatter: DateFormatter

  private static var now = Date()  // Cache now

  init(calendar: Calendar, tags: Binding<[Tag]>) {
    self.calendar = calendar
    self.monthFormatter = DateFormatter(dateFormat: "MMMM", calendar: calendar)
    self.dayFormatter = DateFormatter(dateFormat: "d", calendar: calendar)
    self.weekDayFormatter = DateFormatter(dateFormat: "EEEEE", calendar: calendar)
    self.fullFormatter = DateFormatter(dateFormat: "MMMM dd, yyyy", calendar: calendar)
    self._selectedTags = tags
  }

  var body: some View {
    VStack {
      Text("Selected date: \(fullFormatter.string(from: selectedDate))")
        .bold()
        .foregroundColor(.red)
      CalendarView(
        calendar: calendar,
        date: $selectedDate,
        content: { date in
          Button(action: { selectedDate = date }) {
            Text("00")
              .padding(8)
              .foregroundColor(.clear)
              .background(
                getCalCellBackgroundColor(
                  date: date, selectedDate: selectedDate)
              )
              .cornerRadius(8)
              .accessibilityHidden(true)
              .overlay(
                Text(dayFormatter.string(from: date))
                  .foregroundColor(.white)
              )
          }
        },
        trailing: { date in
          Text(dayFormatter.string(from: date))
            .foregroundColor(.secondary)
        },
        header: { date in
          Text(weekDayFormatter.string(from: date))
        },
        title: { date in
          HStack {
            Text(monthFormatter.string(from: date))
              .font(.headline)
              .padding()
            Spacer()
            Button {
              withAnimation {
                guard
                  let newDate = calendar.date(
                    byAdding: .month,
                    value: -1,
                    to: selectedDate
                  )
                else {
                  return
                }
                selectedDate = newDate
              }
            } label: {
              Label(
                title: { Text("Previous") },
                icon: { Image(systemName: "chevron.left") }
              )
              .labelStyle(IconOnlyLabelStyle())
              .padding(.horizontal)
              .frame(maxHeight: .infinity)
            }
            Button {
              withAnimation {
                guard
                  let newDate = calendar.date(
                    byAdding: .month,
                    value: 1,
                    to: selectedDate
                  )
                else {
                  return
                }
                selectedDate = newDate
              }
            } label: {
              Label(
                title: { Text("Next") },
                icon: { Image(systemName: "chevron.right") }
              )
              .labelStyle(IconOnlyLabelStyle())
              .padding(.horizontal)
              .frame(maxHeight: .infinity)
            }
          }
          .padding(.bottom, 6)
        }
      )
    }
    .padding()
  }
}

// MARK: - Component
public struct CalendarView<Day: View, Header: View, Title: View, Trailing: View>: View {
  @Binding private var date: Date

  private var calendar: Calendar
  private let content: (Date) -> Day
  private let trailing: (Date) -> Trailing
  private let header: (Date) -> Header
  private let title: (Date) -> Title

  private let daysInWeek = 7

  public init(
    calendar: Calendar,
    date: Binding<Date>,
    @ViewBuilder content: @escaping (Date) -> Day,
    @ViewBuilder trailing: @escaping (Date) -> Trailing,
    @ViewBuilder header: @escaping (Date) -> Header,
    @ViewBuilder title: @escaping (Date) -> Title
  ) {
    self.calendar = calendar
    self._date = date
    self.content = content
    self.trailing = trailing
    self.header = header
    self.title = title
  }

  public var body: some View {
    let month = date.startOfMonth(using: calendar)
    let days = makeDays()

    return LazyVGrid(columns: Array(repeating: GridItem(), count: daysInWeek)) {
      Section(header: title(month)) {
        ForEach(days.prefix(daysInWeek), id: \.self, content: header)
        ForEach(days, id: \.self) { date in
          if calendar.isDate(date, equalTo: month, toGranularity: .month) {
            content(date)
          } else {
            trailing(date)
          }
        }
      }
    }
  }
}

// MARK: - Conformances
extension CalendarView: Equatable {
  public static func == (
    lhs: CalendarView<Day, Header, Title, Trailing>,
    rhs: CalendarView<Day, Header, Title, Trailing>
  ) -> Bool {
    lhs.calendar == rhs.calendar && lhs.date == rhs.date
  }
}

// MARK: - Helpers
extension CalendarContentView {
  fileprivate func getCalCellBackgroundColor(date: Date, selectedDate: Date) -> Color {
    let selectedDates = self.selectedTags.filter { tag in
      return tag.clicked
    }.flatMap({ $0.dates })

    print("selectedDates \(selectedDates)")

    if calendar.isDate(selectedDate, inSameDayAs: date) {
      return Color.red
    }
    if selectedDates.contains(date) {
      return Color.orange
    }
    if date > Date() {
      return Color.blue.opacity(0.5)
    }
    return Color.blue
  }
}

extension CalendarView {
  fileprivate func makeDays() -> [Date] {
    guard let monthInterval = calendar.dateInterval(of: .month, for: date),
      let monthFirstWeek = calendar.dateInterval(of: .weekOfMonth, for: monthInterval.start),
      let monthLastWeek = calendar.dateInterval(of: .weekOfMonth, for: monthInterval.end - 1)
    else {
      return []
    }
    let dateInterval = DateInterval(start: monthFirstWeek.start, end: monthLastWeek.end)
    return calendar.generateDays(for: dateInterval)
  }
}

extension Calendar {
  fileprivate func generateDates(
    for dateInterval: DateInterval,
    matching components: DateComponents
  ) -> [Date] {
    var dates = [dateInterval.start]

    enumerateDates(
      startingAfter: dateInterval.start,
      matching: components,
      matchingPolicy: .nextTime
    ) { date, _, stop in
      guard let date = date else { return }
      guard date < dateInterval.end else {
        stop = true
        return
      }
      dates.append(date)
    }
    return dates
  }

  fileprivate func generateDays(for dateInterval: DateInterval) -> [Date] {
    generateDates(
      for: dateInterval,
      matching: dateComponents([.hour, .minute, .second], from: dateInterval.start)
    )
  }
}

extension Date {
  fileprivate func startOfMonth(using calendar: Calendar) -> Date {
    calendar.date(
      from: calendar.dateComponents([.year, .month], from: self)
    ) ?? self
  }
}

extension DateFormatter {
  public convenience init(dateFormat: String, calendar: Calendar) {
    self.init()
    self.dateFormat = dateFormat
    self.calendar = calendar
  }
}

struct CalendarView_Previews: PreviewProvider {
  static var calendar = Calendar(identifier: .gregorian)
  static var formatter = DateFormatter(dateFormat: "yyyy/MM/dd", calendar: calendar)

  @State static var testTags = [
    Tag(
      value: "tag1", clicked: false,
      dates: [
        formatter.date(from: "2023/06/12")!,
        formatter.date(from: "2023/06/13")!,
        formatter.date(from: "2023/06/14")!,
        formatter.date(from: "2023/06/16")!,
      ]),
    Tag(
      value: "tag 1234", clicked: false,
      dates: [
        formatter.date(from: "2023/06/01")!,
        formatter.date(from: "2023/06/02")!,
        formatter.date(from: "2023/06/04")!,
        formatter.date(from: "2023/06/06")!,
        formatter.date(from: "2023/06/09")!,
        formatter.date(from: "2023/06/012")!,
        formatter.date(from: "2023/06/014")!,
      ]),
    Tag(
      value: "long tag 1", clicked: false,
      dates: [
        formatter.date(from: "2023/06/16")!,
        formatter.date(from: "2023/06/14")!,
      ]),
  ]

  static var previews: some View {
    CalendarContentView(calendar: calendar, tags: $testTags)
  }
}
