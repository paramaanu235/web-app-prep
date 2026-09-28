import Foundation
import SwiftUI

@MainActor
public final class AppEnvironment: ObservableObject {
    public let repository: ContentRepository
    public let stateStore: StudyStateStore
    public let searchService: SearchService

    public init(
        repository: ContentRepository = ContentRepository(),
        stateStore: StudyStateStore? = nil
    ) {
        self.repository = repository
        let store = stateStore ?? StudyStateStore()
        self.stateStore = store
        self.searchService = SearchService(repository: repository)
    }

    public static func preview() -> AppEnvironment {
        let repo = ContentRepository()
        let store = StudyStateStore(customDirectory: FileManager.default.temporaryDirectory)
        return AppEnvironment(repository: repo, stateStore: store)
    }
}
