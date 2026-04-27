import UIKit

enum AppLauncher {
    // Ordered by popularity; first installed one wins.
    private static let musicApps: [(scheme: String, openURL: String)] = [
        ("spotify", "spotify://"),
        ("youtubemusic", "youtubemusic://"),
        ("amznmusic", "amznmusic://"),
        ("tidal", "tidal://"),
        ("deezer", "deezer://"),
        ("music", "music://"),  // Apple Music (last — always present, use as fallback)
    ]

    static func openNavigation(query: String) {
        let encoded = query.addingPercentEncoding(withAllowedCharacters: .urlQueryAllowed) ?? query

        // Try Google Maps first if installed
        if let url = URL(string: "comgooglemaps://?daddr=\(encoded)&directionsmode=driving"),
           UIApplication.shared.canOpenURL(url) {
            UIApplication.shared.open(url)
            return
        }

        // Apple Maps universal link — always works, no canOpenURL needed
        if let url = URL(string: "https://maps.apple.com/?daddr=\(encoded)&dirflg=d") {
            UIApplication.shared.open(url)
        }
    }

    static func openMusic() {
        for app in musicApps {
            guard let testURL = URL(string: "\(app.scheme)://"),
                  UIApplication.shared.canOpenURL(testURL),
                  let openURL = URL(string: app.openURL)
            else { continue }
            UIApplication.shared.open(openURL)
            return
        }
    }

    static func call(_ contact: String) {
        let digits = contact.filter { $0.isNumber || $0 == "+" }
        let target = digits.isEmpty ? contact : digits
        if let url = URL(string: "tel://\(target)") {
            UIApplication.shared.open(url)
        }
    }

    private static func openFirst(of urlStrings: [String]) {
        for string in urlStrings {
            guard let url = URL(string: string) else { continue }
            if UIApplication.shared.canOpenURL(url) {
                UIApplication.shared.open(url)
                return
            }
        }
    }
}
