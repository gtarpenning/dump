//
//  Date.swift
//  dump
//
//  Created by Griffin Tarpenning on 5/28/23.
//

import Foundation

extension Date {
  func toString(dateFormat format: String) -> String {
    let dateFormatter = DateFormatter()
    dateFormatter.dateFormat = format
    return dateFormatter.string(from: self)
  }
}

extension VoiceViewModel {
  func covertSecToMinAndHour(seconds: Int) -> String {
    let (_, m, s) = (seconds / 3600, (seconds % 3600) / 60, (seconds % 3600) % 60)
    let sec: String = s < 10 ? "0\(s)" : "\(s)"
    return "\(m):\(sec)"
  }
}
