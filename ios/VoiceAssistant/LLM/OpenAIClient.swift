import Foundation

class OpenAIClient {
    private let systemPrompt = """
        You are Fish, a concise and friendly voice assistant on a phone. \
        Keep every response under two short sentences. \
        Never use markdown or lists — speak in plain, natural language.
        """

    func generate(prompt: String) async throws -> String {
        guard !Config.openAIKey.isEmpty else {
            throw AssistantError.missingAPIKey
        }

        var request = URLRequest(url: URL(string: "https://api.openai.com/v1/chat/completions")!)
        request.httpMethod = "POST"
        request.setValue("Bearer \(Config.openAIKey)", forHTTPHeaderField: "Authorization")
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let body: [String: Any] = [
            "model": Config.openAIModel,
            "max_tokens": 80,
            "messages": [
                ["role": "system", "content": systemPrompt],
                ["role": "user", "content": prompt],
            ],
        ]
        request.httpBody = try JSONSerialization.data(withJSONObject: body)

        let (data, response) = try await URLSession.shared.data(for: request)

        guard let http = response as? HTTPURLResponse, http.statusCode == 200 else {
            throw AssistantError.badResponse
        }

        let json = try JSONSerialization.jsonObject(with: data) as? [String: Any]
        let choices = json?["choices"] as? [[String: Any]]
        let content = choices?.first?["message"] as? [String: Any]
        return (content?["content"] as? String)?.trimmingCharacters(in: .whitespacesAndNewlines) ?? "Okay."
    }
}

enum AssistantError: LocalizedError {
    case missingAPIKey
    case badResponse

    var errorDescription: String? {
        switch self {
        case .missingAPIKey: "OpenAI API key not set. Add it in Settings."
        case .badResponse: "Got an unexpected response from OpenAI."
        }
    }
}
