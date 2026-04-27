import Foundation

struct SkillResult {
    let text: String
    let action: SkillAction?
}

enum SkillAction {
    case navigation(query: String)
    case music(command: String)
    case calling(contact: String)
}

protocol Skill {
    var name: String { get }
    func canHandle(_ text: String) -> Bool
    func handle(_ text: String) -> SkillResult
}
