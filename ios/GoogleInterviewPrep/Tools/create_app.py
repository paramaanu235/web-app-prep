import os

app_dir = "ios/GoogleInterviewPrep/GoogleInterviewPrep/App"
features_dir = "ios/GoogleInterviewPrep/GoogleInterviewPrep/Features"
os.makedirs(app_dir, exist_ok=True)
os.makedirs(features_dir, exist_ok=True)

# 1. AppEnvironment.swift
env_code = """import Foundation
import SwiftUI

@MainActor
public final class AppEnvironment: ObservableObject {
    public let repository: ContentRepository
    public let stateStore: StudyStateStore
    public let searchService: SearchService

    public init(
        repository: ContentRepository = ContentRepository(),
        stateStore: StudyStateStore = StudyStateStore()
    ) {
        self.repository = repository
        self.stateStore = stateStore
        self.searchService = SearchService(repository: repository)
    }

    public static func preview() -> AppEnvironment {
        let repo = ContentRepository()
        let store = StudyStateStore(customDirectory: FileManager.default.temporaryDirectory)
        return AppEnvironment(repository: repo, stateStore: store)
    }
}
"""

with open(f"{app_dir}/AppEnvironment.swift", "w", encoding="utf-8") as f:
    f.write(env_code.strip())
print("Wrote AppEnvironment.swift")

# 2. GoogleInterviewPrepApp.swift
app_code = r"""import SwiftUI

public struct AppThemePalette: Equatable, @unchecked Sendable {
    public let background: Color
    public let groupedBackground: Color
    public let secondaryBackground: Color
    public let tertiaryBackground: Color
    public let separator: Color
    public let accent: Color
    public let preferredColorScheme: ColorScheme?

    public static func resolve(_ preference: String) -> AppThemePalette {
        switch preference {
        case "light":
            return systemPalette(scheme: .light, accent: Color(red: 0.00, green: 0.42, blue: 0.88))
        case "dark":
            return systemPalette(scheme: .dark, accent: Color(red: 0.20, green: 0.67, blue: 1.00))
        case "sepia":
            return AppThemePalette(
                background: Color(red: 0.953, green: 0.918, blue: 0.824),
                groupedBackground: Color(red: 0.925, green: 0.871, blue: 0.745),
                secondaryBackground: Color(red: 0.985, green: 0.949, blue: 0.855),
                tertiaryBackground: Color(red: 0.890, green: 0.820, blue: 0.663),
                separator: Color(red: 0.49, green: 0.39, blue: 0.27),
                accent: Color(red: 0.48, green: 0.29, blue: 0.13),
                preferredColorScheme: .light
            )
        default:
            return systemPalette(scheme: nil, accent: .accentColor)
        }
    }

    private static func systemPalette(scheme: ColorScheme?, accent: Color) -> AppThemePalette {
        AppThemePalette(
            background: Color(uiColor: .systemBackground),
            groupedBackground: Color(uiColor: .systemGroupedBackground),
            secondaryBackground: Color(uiColor: .secondarySystemGroupedBackground),
            tertiaryBackground: Color(uiColor: .tertiarySystemGroupedBackground),
            separator: Color(uiColor: .separator),
            accent: accent,
            preferredColorScheme: scheme
        )
    }
}

private struct AppThemeKey: EnvironmentKey {
    static let defaultValue = AppThemePalette.resolve("system")
}

public extension EnvironmentValues {
    var appTheme: AppThemePalette {
        get { self[AppThemeKey.self] }
        set { self[AppThemeKey.self] = newValue }
    }
}

public extension View {
    func themedSurface() -> some View {
        modifier(ThemedSurfaceModifier())
    }
}

private struct ThemedSurfaceModifier: ViewModifier {
    @Environment(\.appTheme) private var theme

    func body(content: Content) -> some View {
        content
            .scrollContentBackground(.hidden)
            .background(theme.background.ignoresSafeArea())
    }
}

@main
struct GoogleInterviewPrepApp: App {
    @StateObject private var environment: AppEnvironment

    init() {
        _environment = StateObject(wrappedValue: AppEnvironment())
    }

    var body: some Scene {
        WindowGroup {
            AppRootView(environment: environment)
        }
    }
}

private struct AppRootView: View {
    let environment: AppEnvironment
    @ObservedObject private var stateStore: StudyStateStore

    init(environment: AppEnvironment) {
        self.environment = environment
        self.stateStore = environment.stateStore
    }

    private var theme: AppThemePalette {
        AppThemePalette.resolve(stateStore.state.themePreference)
    }

    var body: some View {
        MainTabView()
            .themedSurface()
            .environment(\.appTheme, theme)
            .environmentObject(environment)
            .environmentObject(stateStore)
            .environmentObject(environment.searchService)
            .tint(theme.accent)
            .preferredColorScheme(theme.preferredColorScheme)
            .toolbarBackground(theme.background, for: .navigationBar)
            .toolbarBackground(theme.groupedBackground, for: .tabBar)
            .toolbarBackground(.visible, for: .navigationBar, .tabBar)
            .onAppear { syncKeepAwake() }
            .onChange(of: stateStore.state.keepScreenAwake) { _ in syncKeepAwake() }
    }

    private func syncKeepAwake() {
        UIApplication.shared.isIdleTimerDisabled = stateStore.state.keepScreenAwake
    }
}
"""

with open(f"{app_dir}/GoogleInterviewPrepApp.swift", "w", encoding="utf-8") as f:
    f.write(app_code.strip())
print("Wrote GoogleInterviewPrepApp.swift")

# 3. MainTabView.swift
tab_code = """import SwiftUI

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
"""

with open(f"{features_dir}/MainTabView.swift", "w", encoding="utf-8") as f:
    f.write(tab_code.strip())
print("Wrote MainTabView.swift")
