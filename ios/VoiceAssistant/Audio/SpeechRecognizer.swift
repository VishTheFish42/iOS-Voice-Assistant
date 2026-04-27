import AVFoundation
import Speech

@MainActor
class SpeechRecognizer {
    private let recognizer = SFSpeechRecognizer(locale: Locale(identifier: "en-US"))
    private var request: SFSpeechAudioBufferRecognitionRequest?
    private var task: SFSpeechRecognitionTask?
    private let engine = AVAudioEngine()
    private var silenceTimer: Timer?

    var onTranscript: ((String, Bool) -> Void)?

    func requestPermissions() async -> Bool {
        let speech = await withCheckedContinuation { cont in
            SFSpeechRecognizer.requestAuthorization { cont.resume(returning: $0) }
        }
        let mic = await AVAudioApplication.requestRecordPermission()
        return speech == .authorized && mic
    }

    func finish() {
        silenceTimer?.invalidate()
        silenceTimer = nil
        task?.finish()
    }

    func start() throws {
        stop()

        guard recognizer?.isAvailable == true else {
            throw SpeechError.unavailable
        }

        let session = AVAudioSession.sharedInstance()
        try session.setCategory(.playAndRecord, mode: .measurement, options: [.duckOthers, .defaultToSpeaker])
        try session.setActive(true, options: .notifyOthersOnDeactivation)

        request = SFSpeechAudioBufferRecognitionRequest()
        request?.shouldReportPartialResults = true

        task = recognizer?.recognitionTask(with: request!) { [weak self] result, error in
            guard let self else { return }
            Task { @MainActor in
                if let text = result?.bestTranscription.formattedString {
                    self.resetSilenceTimer()
                    self.onTranscript?(text, result?.isFinal ?? false)
                }
                if result?.isFinal == true || (error != nil && result == nil) {
                    self.stop()
                }
            }
        }

        engine.prepare()
        let format = engine.inputNode.outputFormat(forBus: 0)
        engine.inputNode.installTap(onBus: 0, bufferSize: 4096, format: format) { [weak self] buf, _ in
            self?.request?.append(buf)
        }
        try engine.start()

        resetSilenceTimer()
    }

    func stop() {
        silenceTimer?.invalidate()
        silenceTimer = nil
        engine.stop()
        engine.inputNode.removeTap(onBus: 0)
        request?.endAudio()
        request = nil
        task?.cancel()
        task = nil
    }

    private func resetSilenceTimer() {
        silenceTimer?.invalidate()
        silenceTimer = Timer.scheduledTimer(withTimeInterval: 2.0, repeats: false) { [weak self] _ in
            self?.task?.finish()
        }
    }
}

enum SpeechError: LocalizedError {
    case unavailable
    var errorDescription: String? {
        "Speech recognition is not available on this device right now."
    }
}
