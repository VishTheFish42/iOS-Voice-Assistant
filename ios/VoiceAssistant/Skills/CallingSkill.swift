import Foundation

class CallingSkill: Skill {
    let name = "calling"

    private let triggers = ["call", "dial", "ring", "phone"]

    func canHandle(_ text: String) -> Bool {
        let lowered = text.lowercased()
        return triggers.contains { lowered.contains($0) }
    }

    func handle(_ text: String) -> SkillResult {
        let contact = extractContact(from: text)
        return SkillResult(text: "Calling \(contact).", action: .calling(contact: contact))
    }

    private func extractContact(from text: String) -> String {
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
