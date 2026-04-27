import SwiftUI

struct ContentView: View {
    @StateObject private var orchestrator = Orchestrator()
    @State private var showSettings = false

    var body: some View {
        NavigationStack {
            VStack(spacing: 32) {
                Spacer()

                // Response area
                VStack(spacing: 8) {
                    if !orchestrator.response.isEmpty {
                        Text(orchestrator.response)
                            .font(.title3)
                            .multilineTextAlignment(.center)
                            .padding(.horizontal)
                            .transition(.opacity)
                    }

                    if !orchestrator.transcript.isEmpty {
                        Text(orchestrator.transcript)
                            .font(.callout)
                            .foregroundStyle(.secondary)
                            .italic()
                            .multilineTextAlignment(.center)
                            .padding(.horizontal)
                    }
                }
                .frame(minHeight: 80)

                Spacer()

                // Mic button
                Button(action: orchestrator.toggleListening) {
                    ZStack {
                        Circle()
                            .fill(orchestrator.isListening ? Color.red : Color.accentColor)
                            .frame(width: 96, height: 96)

                        if orchestrator.isProcessing {
                            ProgressView().tint(.white)
                        } else {
                            Image(systemName: orchestrator.isListening ? "waveform" : "mic.fill")
                                .font(.system(size: 36))
                                .foregroundStyle(.white)
                        }
                    }
                }
                .buttonStyle(.plain)
                .scaleEffect(orchestrator.isListening ? 1.1 : 1.0)
                .animation(.easeInOut(duration: 0.2), value: orchestrator.isListening)
                .disabled(orchestrator.isProcessing)

                Text(orchestrator.isListening ? "Listening…" : "Tap to speak")
                    .font(.footnote)
                    .foregroundStyle(.secondary)

                Spacer().frame(height: 32)
            }
            .navigationTitle("Fish")
            .navigationBarTitleDisplayMode(.large)
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Button { showSettings = true } label: {
                        Image(systemName: "gearshape")
                    }
                }
            }
            .sheet(isPresented: $showSettings) {
                SettingsView()
            }
            .alert("Permission Required", isPresented: $orchestrator.permissionDenied) {
                Button("Open Settings") {
                    if let url = URL(string: UIApplication.openSettingsURLString) {
                        UIApplication.shared.open(url)
                    }
                }
                Button("Cancel", role: .cancel) {}
            } message: {
                Text("Fish needs microphone and speech recognition access. Enable them in Settings.")
            }
        }
    }
}
