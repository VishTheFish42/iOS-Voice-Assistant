import Foundation

@MainActor
class Orchestrator: ObservableObject {
    @Published var transcript: String = ""
    @Published var response: String = ""
    @Published var isListening = false
    @Published var isProcessing = false
    @Published var permissionDenied = false

    private let speech = SpeechRecognizer()
    private let skills = SkillRouter()
    private let llm = OpenAIClient()
    private let tts = TTSEngine()

    init() {
        speech.onTranscript = { [weak self] text, isFinal in
            guard let self else { return }
            Task { @MainActor in
                self.transcript = text
                if isFinal {
                    self.isListening = false
                    await self.handle(text)
                }
            }
        }
    }

    func toggleListening() {
        if isListening {
            isListening = false
            speech.finish()
        } else {
            startListening()
        }
    }

    private func startListening() {
        Task {
            let granted = await speech.requestPermissions()
            guard granted else {
                permissionDenied = true
                return
            }
            do {
                transcript = ""
                response = ""
                tts.stop()
                try speech.start()
                isListening = true
            } catch {
                response = "Couldn't start the microphone: \(error.localizedDescription)"
            }
        }
    }

    private func handle(_ text: String) async {
        guard !text.trimmingCharacters(in: .whitespaces).isEmpty else { return }
        isProcessing = true

        if let result = skills.route(text) {
            respond(result.text)
            executeAction(result.action)
            isProcessing = false
            return
        }

        do {
            let text = try await llm.generate(prompt: text)
            respond(text)
        } catch {
            respond(error.localizedDescription)
        }
        isProcessing = false
    }

    private func respond(_ text: String) {
        response = text
        tts.speak(text)
    }

    private func executeAction(_ action: SkillAction?) {
        switch action {
        case .navigation(let query): AppLauncher.openNavigation(query: query)
        case .music: AppLauncher.openMusic()
        case .calling(let contact): AppLauncher.call(contact)
        case nil: break
        }
    }
}
