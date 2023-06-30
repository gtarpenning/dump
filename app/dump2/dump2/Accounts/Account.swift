import Foundation
import Observation
import SwiftData

@Model
public class Account {

  @Attribute(.unique) public var id: String
  public var joinDate: Date
  public var displayName: String
  public var emailAddress: String

  public init(joinData: Date, displayName: String, emailAddress: String) {
    self.id = UUID().uuidString
    self.joinDate = joinDate
    self.displayName = displayName
    self.emailAddress = emailAddress
  }
}
