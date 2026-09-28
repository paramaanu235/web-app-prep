import SwiftUI

public struct ChecklistView: View {
    @EnvironmentObject private var stateStore: StudyStateStore
    @Environment(\.appTheme) private var theme
    @State private var newTitle: String = ""
    @State private var newCategory: String = "Daily DSA"

    public init() {}

    public var body: some View {
        List {
            Group {
            Section("Today's Active Checklist") {
                ForEach(stateStore.state.dailyChecklist) { item in
                    HStack {
                        Button(action: { stateStore.toggleChecklist(id: item.id) }) {
                            Image(systemName: item.isDone ? "checkmark.circle.fill" : "circle")
                                .foregroundColor(item.isDone ? .green : .secondary)
                                .font(.title3)
                        }
                        .buttonStyle(.plain)

                        VStack(alignment: .leading, spacing: 2) {
                            Text(item.title)
                                .font(.subheadline)
                                .strikethrough(item.isDone)
                                .foregroundColor(item.isDone ? .secondary : .primary)
                            Text(item.category)
                                .font(.caption2)
                                .foregroundColor(.secondary)
                        }
                    }
                    .padding(.vertical, 4)
                }
            }

            Section("Add Drill Item") {
                TextField("Drill description...", text: $newTitle)
                Picker("Category", selection: $newCategory) {
                    Text("Daily DSA").tag("Daily DSA")
                    Text("System Design").tag("System Design")
                    Text("Behavioral").tag("Behavioral")
                    Text("Error Log").tag("Error Log")
                }
                Button("Add to Checklist") {
                    if !newTitle.isEmpty {
                        stateStore.addChecklistItem(title: newTitle, category: newCategory)
                        newTitle = ""
                    }
                }
                .disabled(newTitle.isEmpty)
            }
            }
            .listRowBackground(theme.secondaryBackground)
        }
        .themedSurface()
        .navigationTitle("Daily Drill Checklist")
    }
}
