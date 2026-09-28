import SwiftUI

public struct MainTabView: View {
    @EnvironmentObject private var stateStore: StudyStateStore
    @State private var selectedTab: Int = 0

    public init() {}

    public var body: some View {
        TabView(selection: $selectedTab) {
            NavigationStack {
                HomeView()
            }
            .tabItem {
                Label("Home", systemImage: "house.fill")
            }
            .tag(0)

            NavigationStack {
                LibraryView()
            }
            .tabItem {
                Label("Library", systemImage: "books.vertical.fill")
            }
            .tag(1)

            NavigationStack {
                SearchView()
            }
            .tabItem {
                Label("Search", systemImage: "magnifyingglass")
            }
            .tag(2)

            NavigationStack {
                ProgressDashboardView()
            }
            .tabItem {
                Label("Progress", systemImage: "chart.bar.fill")
            }
            .tag(3)

            NavigationStack {
                SavedView()
            }
            .tabItem {
                Label("Saved", systemImage: "bookmark.fill")
            }
            .tag(4)
        }
    }
}