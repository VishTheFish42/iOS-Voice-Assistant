import Foundation

class SkillRouter {
    private let skills: [any Skill] = [
        NavigationSkill(),
        MusicSkill(),
        CallingSkill(),
    ]

    func route(_ text: String) -> SkillResult? {
        skills.first { $0.canHandle(text) }.map { $0.handle(text) }
    }
}
