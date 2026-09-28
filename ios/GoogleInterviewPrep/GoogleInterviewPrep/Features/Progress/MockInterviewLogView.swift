import SwiftUI

public struct MockInterviewLogView: View {
    public let onSave: (MockResult) -> Void
    @Environment(\.dismiss) private var dismiss
    @Environment(\.appTheme) private var theme

    @State private var type: String = "Coding"
    @State private var score: Int = 3
    @State private var strengths: String = ""
    @State private var misses: String = ""
    @State private var nextDrill: String = ""

    public init(onSave: @escaping (MockResult) -> Void) {
        self.onSave = onSave
    }

    public var body: some View {
        NavigationStack {
            Form {
                Group {
                Section("Format & Calibration") {
                    Picker("Type", selection: $type) {
                        Text("Coding (45m)").tag("Coding")
                        Text("System Design (45m)").tag("System Design")
                        Text("Behavioral / Leadership").tag("Behavioral")
                    }

                    Picker("Score", selection: $score) {
                        Text("1 - No Hire / Major Gaps").tag(1)
                        Text("2 - Lean No Hire / Needs Scaffolding").tag(2)
                        Text("3 - Lean Hire / Meets Bar").tag(3)
                        Text("4 - Strong Hire / Exceeds Bar").tag(4)
                    }
                }

                Section("Debrief Notes") {
                    TextField("What went well (strengths)", text: $strengths)
                    TextField("Misses / Hesitations", text: $misses)
                    TextField("Next targeted drill", text: $nextDrill)
                }
                }
                .listRowBackground(theme.secondaryBackground)
            }
            .themedSurface()
            .navigationTitle("Log Mock")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Cancel") { dismiss() }
                }
                ToolbarItem(placement: .confirmationAction) {
                    Button("Save") {
                        let result = MockResult(
                            date: Date(),
                            type: type,
                            score: score,
                            strengths: strengths,
                            misses: misses,
                            nextDrill: nextDrill
                        )
                        onSave(result)
                        dismiss()
                    }
                }
            }
        }
    }
}
