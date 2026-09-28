import SwiftUI

public struct LocalInstallHelpView: View {
    public init() {}

    public var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
                Text("Physical iPhone Local Installation")
                    .font(.title2.bold())

                Text("This app is designed to run 100% offline on your iPhone using Xcode's free local development provisioning. No paid Apple Developer account or App Store submission is needed.")
                    .font(.subheadline)
                    .foregroundColor(.secondary)

                VStack(alignment: .leading, spacing: 12) {
                    StepRow(number: 1, title: "Open Xcode Project", description: "Open `ios/GoogleInterviewPrep/GoogleInterviewPrep.xcodeproj` in Xcode.")
                    StepRow(number: 2, title: "Select Signing Team", description: "Select the app target in Xcode → Signing & Capabilities. Enable 'Automatically manage signing' and select your Personal Team.")
                    StepRow(number: 3, title: "Unique Bundle ID", description: "If prompted, change the bundle identifier to a unique string (e.g. dev.yourname.GoogleInterviewPrep).")
                    StepRow(number: 4, title: "Connect iPhone", description: "Connect your iPhone with a USB cable. Trust the Mac when prompted on the iPhone.")
                    StepRow(number: 5, title: "Enable Developer Mode", description: "On iPhone: Settings → Privacy & Security → Developer Mode → Turn ON and reboot.")
                    StepRow(number: 6, title: "Build & Run", description: "Select your iPhone as the destination in Xcode and press Run (Cmd+R).")
                    StepRow(number: 7, title: "Trust Developer Certificate", description: "On iPhone: Settings → General → VPN & Device Management → tap your Apple ID and tap Trust.")
                    StepRow(number: 8, title: "Verify Airplane Mode", description: "Turn on Airplane Mode on your iPhone to verify all 18 documents, full-text search, and notes work with zero network connection.")
                }
            }
            .padding()
        }
        .themedSurface()
        .navigationTitle("Local Install Guide")
        .navigationBarTitleDisplayMode(.inline)
    }
}

public struct StepRow: View {
    public let number: Int
    public let title: String
    public let description: String

    public var body: some View {
        HStack(alignment: .top, spacing: 12) {
            Text("\(number)")
                .font(.headline)
                .foregroundColor(.white)
                .frame(width: 28, height: 28)
                .background(Color.accentColor)
                .clipShape(Circle())

            VStack(alignment: .leading, spacing: 4) {
                Text(title)
                    .font(.headline)
                Text(description)
                    .font(.subheadline)
                    .foregroundColor(.secondary)
            }
        }
        .padding(.vertical, 4)
    }
}
