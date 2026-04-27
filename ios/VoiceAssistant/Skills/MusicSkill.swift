import Foundation

class MusicSkill: Skill {
    let name = "music"

    private let triggers = ["play", "pause", "resume", "next song", "previous song", "skip", "shuffle", "music"]

    func canHandle(_ text: String) -> Bool {
        let lowered = text.lowercased()
        return triggers.contains { lowered.contains($0) }
    }

    func handle(_ text: String) -> SkillResult {
        let lowered = text.lowercased()
        let response: String
        if lowered.contains("pause") {
            response = "Pausing music."
        } else if lowered.contains("resume") || lowered.contains("play") {
            response = "Playing music."
        } else if lowered.contains("next") || lowered.contains("skip") {
            response = "Skipping to the next song."
        } else if lowered.contains("previous") {
            response = "Going back to the previous song."
        } else if lowered.contains("shuffle") {
            response = "Shuffling your music."
        } else {
            response = "On it."
        }
        return SkillResult(text: response, action: .music(command: text))
    }
}
