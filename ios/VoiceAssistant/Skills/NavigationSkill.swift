import Foundation

class NavigationSkill: Skill {
    let name = "navigation"

    private let triggers = [
        "navigate to", "directions to", "take me to", "drive to",
        "get me to", "route to", "how do i get to", "map to",
        "go to", "open maps", "navigate me to", "find directions",
        "i need to go to", "i want to go to", "can you take me",
    ]

    func canHandle(_ text: String) -> Bool {
        let lowered = text.lowercased()
        return triggers.contains { lowered.contains($0) }
    }

    func handle(_ text: String) -> SkillResult {
        let dest = extractDestination(from: text)
        return SkillResult(text: "Starting navigation to \(dest).", action: .navigation(query: dest))
    }

    private func extractDestination(from text: String) -> String {
        let lowered = text.lowercased()
        for trigger in triggers {
            if let range = lowered.range(of: trigger) {
                let after = text[range.upperBound...].trimmingCharacters(in: .whitespaces)
                if !after.isEmpty { return after }
            }
        }
        return text
    }
}
