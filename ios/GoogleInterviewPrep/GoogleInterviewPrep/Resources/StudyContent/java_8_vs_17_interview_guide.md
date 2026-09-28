# Java 8 vs Java 17 — interview guide

Use this to explain Java 8→17 language, library and runtime changes. Describe only migration work you actually did; examples below are prompts, not claims about your experience.

Code blocks are independent fragments. Add the relevant imports and enclosing class/method; repeated type names belong to separate examples. Unless explicitly labeled otherwise, Java 17 examples use **no preview features**.

**LTS releases covered here:** 8 (2014) → 11 (2018) → 17 (2021). A direct 8→17 migration is supported; reviewing the intervening releases helps find breaking changes. Deploying Java 11 first is optional, not required. This is a historical comparison, not a list of all current LTS releases.

**In a coding round:** confirm the supported Java version with the recruiter/interviewer. Use features that environment supports; Java 8-compatible syntax is a conservative fallback if it is unknown. Language-feature knowledge alone does not establish an interview level.

---

## 1. Thirty-second summary

| | Java 8 | Java 17 |
|---|---|---|
| Identity | Lambdas, streams, `java.time`, default methods | Records, sealed types, text blocks, switch expressions, pattern `instanceof` |
| Data carriers | JavaBean + Builder + `equals`/`hashCode` by hand | `record` |
| Closed hierarchies | Visitor / `instanceof` + cast / enum | `sealed` + pattern matching |
| Collections | `Arrays.asList` (fixed-size, mutable slots), `unmodifiable*` views | Unmodifiable factories/results; contained objects can still be mutable |
| JDK internals | No JPMS; many internals accessible but unsupported | Strong encapsulation; deep reflection into non-open JDK packages normally fails |
| Default GC | Parallel | G1 (since 9) |
| Modules | Classpath, no JPMS | JPMS available; classpath applications still supported |
| Bundled components | Selected Java EE/CORBA APIs and Nashorn; JavaFX depended on distribution | Selected modules and Nashorn removed; JavaFX distributed separately; CMS removed; SecurityManager deprecated for removal |

**Unchanged:** type erasure, equality contracts and the Java Memory Model still apply. HotSpot still uses JIT compilation, GC and allocation optimizations, though implementations evolve. Patterns such as DI and Singleton solve different problems; a Java upgrade does not decide between them.

---

## 2. Language features you must contrast

### 2.1 Local `var` (Java 10)

```java
// Java 8
Map<String, List<Integer>> counts8 = new HashMap<>();

// Java 10+
var counts17 = new HashMap<String, List<Integer>>();
```

**Interview:** `var` infers a static local type; it is not dynamic typing. It cannot declare fields, ordinary method parameters or return types. `var x = null` is illegal. Java 11 permits `var` for lambda parameters (all parameters must use the same declaration style). Beware `var map = new HashMap<>()`: without a target type it infers `HashMap<Object, Object>`. Use it when the inferred type is clear and appropriate; the two examples above infer different declared types (`Map` versus `HashMap`).

### 2.2 Switch: statement vs expression (14 standard)

```java
// Java 8 — fall-through, must break, cannot yield a value
String label;
switch (status) {
    case 1:
    case 2: label = "open"; break;
    case 3: label = "closed"; break;
    default: throw new IllegalArgumentException();
}

// Java 14+ expression — every input needs a result; arrows do not fall through
String label17 = switch (status) {
    case 1, 2 -> "open";
    case 3    -> "closed";
    default   -> throw new IllegalArgumentException();
};
```

Block arrows use `yield` (not `return`):

```java
int n = switch (s) {
    case "a" -> 1;
    case "b" -> {
        log(s);
        yield 2;
    }
    default -> 0;
};
```

**Pattern matching for switch is preview in 17, standard in 21.** Java 17 preview code needs `--enable-preview` when compiling and running with the matching release. Prefer non-preview syntax unless the environment explicitly permits it; later runtimes do not generally accept older preview class files.

### 2.3 Pattern matching `instanceof` (16 standard)

```java
static final class Literal {
    final int value;
    Literal(int value) { this.value = value; }
}

static int read8(Object node) {
    if (node instanceof Literal) {
        Literal lit = (Literal) node;
        return lit.value;
    }
    throw new IllegalArgumentException("not a literal");
}

static int read17(Object node) {
    if (node instanceof Literal lit) return lit.value;
    throw new IllegalArgumentException("not a literal");
}
```

Scope follows control flow: the variable is available wherever the match is known to have succeeded, including the right side of `&&` or after a negated check that exits. An `instanceof` test on null is false. It reduces casting boilerplate but does not check exhaustiveness of an if-chain.

### 2.4 Records (16 standard, you will use them on 17)

```java
// Java 8 value class (Money8 keeps the comparison in one scope)
final class Money8 {
    private final String currency;
    private final long cents;
    Money8(String currency, long cents) {
        if (currency == null || cents < 0) throw new IllegalArgumentException();
        this.currency = currency;
        this.cents = cents;
    }
    public String currency() { return currency; }
    public long cents() { return cents; }
    @Override public boolean equals(Object other) {
        if (this == other) return true;
        if (!(other instanceof Money8)) return false;
        Money8 m = (Money8) other;
        return cents == m.cents && currency.equals(m.currency);
    }
    @Override public int hashCode() { return Objects.hash(currency, cents); }
    @Override public String toString() { return currency + " " + cents; }
}

// Java 16+: this example models non-negative amounts in minor units.
record Money(String currency, long cents) {
    Money { // validate/reassign parameters; implicit field assignments happen last
        if (currency == null || cents < 0) throw new IllegalArgumentException();
    }
    Money plus(Money o) {
        Objects.requireNonNull(o, "other");
        if (!currency.equals(o.currency)) throw new IllegalArgumentException("fx");
        return new Money(currency, Math.addExact(cents, o.cents));
    }
}
```

**Facts they like:**
- Implicit `final` class, `private final` fields, accessor **`currency()` not `getCurrency()`**
- Generated canonical constructor, `equals`/`hashCode`/`toString` based on components; you may explicitly implement them
- **Shallow immutability** only: mutable components can change equality/hash codes. Array components use reference equality by default, not element-by-element equality
- Can implement interfaces; **cannot extend** a class; cannot declare extra instance fields
- Java serialization requires explicit `implements Serializable`; deserialization invokes the canonical constructor and ignores record `readObject`/`writeObject` hooks
- Useful as keys/snapshots/payloads when components have suitable stable value semantics
- **Not** a replacement for entities with identity / lifecycle / JPA without extra work

### 2.5 Sealed classes (17 standard)

```java
sealed interface Node permits Lit, Add, Neg {}
record Lit(int v) implements Node {}
record Add(Node l, Node r) implements Node {}
record Neg(Node n) implements Node {}
```

Direct permitted subtypes must be `final`, `sealed`, or `non-sealed` (records are implicitly final). They must be in the **same named module**, or the **same package when in the unnamed module**. A `non-sealed` branch permits further extension; `permits` restricts direct subtypes, not every descendant. A permits list can be inferred for direct subtypes in the same compilation unit.

Java 17 if/`instanceof` chains are **not checked for exhaustiveness**. A Java 21 pattern-switch expression can be checked for exhaustiveness; pattern switch is only preview in 17.

### 2.6 Text blocks (15 standard)

```java
// Java 8
String q8 = "SELECT id, email\n"
         + "FROM users\n"
         + "WHERE id = ?\n";

// Java 15+
String q17 = """
        SELECT id, email
        FROM users
        WHERE id = ?
        """;
```

Incidental indentation stripped. Useful for JSON/SQL in tests. Text blocks are literals, with no interpolation in Java 17; do not assume a later Java release adds it. `\` at end of line suppresses newline.

### 2.7 Collection factories

```java
// Java 8
List<String> a = Arrays.asList("a", "b"); // fixed size, set() works, nulls OK
a.set(0, "z");                            // OK
List<String> u = Collections.unmodifiableList(new ArrayList<>(a)); // view

// Java 9+
List<String> b = List.of("a", "b");       // unmodifiable; rejects nulls
// b.set(0, "z");                         // would throw UnsupportedOperationException
Map<String, Integer> m = Map.of("k", 1);  // max 10 entries; Map.ofEntries for more
Set<String> s = Set.of("a", "b");         // duplicate keys/elements throw IAE

// Java 10
List<String> snapshot = List.copyOf(a);  // shallow snapshot; rejects nulls; may reuse a suitable input

// Java 8 vs 16 streams
a.stream().collect(Collectors.toList()); // type and mutability NOT guaranteed
a.stream().collect(Collectors.toCollection(ArrayList::new)); // explicitly mutable
a.stream().collect(Collectors.toUnmodifiableList()); // Java 10, rejects nulls
Stream.of("a", (String) null).toList();   // Java 16, unmodifiable; accepts nulls
```

**Trap:** these collections are not deeply immutable. `Collectors.toList()` gives no mutability guarantee. Replacing it with `Stream.toList()` breaks subsequent mutations; merely upgrading the JDK does not rewrite the call. Use `toCollection(ArrayList::new)` when you require a mutable list. `Map.of` rejects duplicate keys and null keys/values; `Set.of` rejects duplicates/nulls. [Stream API](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/stream/Stream.html#toList()), [Collectors API](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/stream/Collectors.html#toList()).

### 2.8 Strings, files, HTTP

| Need | Java 8 | Java 11 / 17 |
|---|---|---|
| Blank check | `trim().isEmpty()` | `isBlank()` (11) — uses Unicode whitespace |
| Strip | `trim()` (removes characters ≤ U+0020) | `strip()` / `stripLeading()` (11) |
| Repeat | loop / `StringBuilder` | `repeat(n)` (11) |
| Lines | `split("\\R")` | `lines()` stream (11) |
| File as String | `new String(Files.readAllBytes(p), StandardCharsets.UTF_8)` | `Files.readString(path)` (11; UTF-8 default) |
| HTTP | `HttpURLConnection` or Apache | `java.net.http.HttpClient` (11, incubated 9) |

```java
HttpClient client = HttpClient.newBuilder().connectTimeout(Duration.ofSeconds(5)).build();
HttpRequest req = HttpRequest.newBuilder(URI.create("https://example.com"))
        .timeout(Duration.ofSeconds(10)).GET().build();
HttpResponse<String> res = client.send(req, HttpResponse.BodyHandlers.ofString());
```

`send` blocks and declares `IOException`/`InterruptedException`; propagate interruption or restore the interrupt flag if caught. `sendAsync` returns a `CompletableFuture`. `isBlank`/`strip` use `Character.isWhitespace`, which does not include every Unicode space (e.g. non-breaking space). `String.lines()` recognizes LF, CR and CRLF; it is not equivalent to splitting on every `\R` line break.

### 2.9 Optional / Stream extras

```java
Optional<String> optional = Optional.of("value");
// Java 9
optional.ifPresentOrElse(System.out::println, () -> System.out.println("missing"));
optional.or(() -> Optional.of("fallback"));
long present = optional.stream().count(); // 0 or 1 element
long absent = Stream.ofNullable(null).count(); // 0
List<Integer> prefix = Stream.of(1, 2, 0, 3).takeWhile(x -> x > 0)
        .collect(Collectors.toList()); // [1, 2]
List<Integer> suffix = Stream.of(1, 2, 0, 3).dropWhile(x -> x > 0)
        .collect(Collectors.toList()); // [0, 3]
long count = Stream.iterate(0, x -> x < 3, x -> x + 1).count(); // 3

// Java 10 / 11
String value = optional.orElseThrow(); // no-arg throws if empty (10)
boolean empty = optional.isEmpty(); // 11
Predicate<String> nonblank = Predicate.not(String::isBlank); // 11

// Java 12: teeing combines two collector results; empty average is explicit.
OptionalDouble average = Stream.of(2, 4, 6).collect(Collectors.teeing(
        Collectors.summingDouble(Integer::doubleValue), Collectors.counting(),
        (sum, n) -> n == 0 ? OptionalDouble.empty() : OptionalDouble.of(sum / n)));

// Java 16: emit zero or more outputs per input.
List<Integer> doubled = Stream.of(1, 2).<Integer>mapMulti((x, out) -> {
    out.accept(x);
    out.accept(x * 10);
}).toList(); // [1, 10, 2, 20]
```

Each terminal operation needs a fresh stream. `takeWhile`/`dropWhile` operate on prefixes of ordered streams, not every matching element. `orElse(expensive())` evaluates eagerly; `orElseGet(() -> expensive())` is lazy (both already existed in 8).

### 2.10 Interfaces

Java 8: default + static methods.  
Java 9: **private** instance and static methods on interfaces (shared helpers for defaults, not part of API).

```java
public interface Retry {
    default void run() { attempt(1); }
    private void attempt(int n) { /* Java 9+ */ }
}
```

---

## 3. What stayed the same (do not “upgrade” these in your head)

- Memory model: volatile visibility/order does not make `count++` atomic; final-field initialization guarantees require proper construction (no escaping `this`)
- Generics erasure, PECS, heap pollution
- `==` vs `equals`; `hashCode` contract
- Checked exceptions (records/lambdas did not remove them)
- `ArrayList` / `HashMap` / `ConcurrentHashMap` complexity
- `PriorityQueue` is still a min-heap; still no `decrease-key`
- `Cloneable` is still a trap
- `new Object()` identity vs value types (Valhalla is **not** 17)
- Virtual threads are **Java 21**, not 17 — don’t claim 17 has them
- Pattern-switch is a **preview** in 17 (requires opt-in for compilation and execution); it is standard in 21
- Spring / Hibernate versions are independent of “I use 17”

---

## 4. Design patterns: Java 8 vs Java 17

No GoF pattern was deleted. New syntax can reduce boilerplate; choose patterns by requirements, not Java version.

### Patterns that remain available on 17

| Pattern | 8 and 17 |
|---|---|
| Strategy | Lambdas (already 8). 17: same, maybe `record` for strategy with fields |
| Decorator / Proxy / Adapter / Facade | Unchanged. I/O streams still decorator |
| Composite | Unchanged. Sealed `FileSys` if the set of node types is closed |
| Observer | Still. Do **not** use `java.util.Observable` (obsolete since 9). `Flow` (9) if you need Reactive Streams |
| Command | `record SaveCmd(...) implements Command` is nicer; undo stack same |
| Template Method | Still. Or default methods + private interface methods (9) |
| Chain | Still. Filters unchanged |
| Singleton | Enum or initialization-on-demand holder when global identity is required; DI often controls application lifetime |
| DI | Still constructor injection. 17 didn’t change this |
| DAO / Repository | Same |
| Object pool | Same. `BlockingQueue` same |
| Flyweight | Same. Don’t intern records blindly |
| Builder | Useful for many optional fields; constructors/factories also enforce invariants |

### Changed or demoted

#### A. JavaBean DTO / “POJO with getters” → Record

**Java 8 pattern:** private fields, getters, `equals`/`hashCode`/`toString`, maybe Builder.

**Java 17:** `record` is an option for transparent value carriers. Check serializer support and persistence requirements before converting existing APIs.

Interview line: “For a value I used a bean + builder on 8; on 17 that’s a record unless it has identity or mutability.”

#### B. Visitor on a closed AST → Sealed + pattern matching

This is a useful comparison of language syntax and extensibility tradeoffs.

```java
// Java 17: use Node/Lit/Add/Neg from section 2.5.
// A classic Visitor instead declares visit overloads and accept on each node.
int eval(Node n) {
    Objects.requireNonNull(n, "node");
    if (n instanceof Lit l) return l.v();
    if (n instanceof Add a) return eval(a.l()) + eval(a.r());
    if (n instanceof Neg g) return -eval(g.n());
    throw new IllegalStateException("unhandled subtype"); // runtime fallback, NOT compile-time exhaustiveness
}
```

| | Visitor (8) | Sealed + PM (17/21) |
|---|---|---|
| Add an **operation** | New visitor implementation; nodes unchanged | Add a new function; existing functions unchanged |
| Add a **node type** | Touch every visitor | Touch every function; compiler helps if sealed/switch exhaustive |
| Best when | Element set stable, ops grow (compiler backend) | Type set stable, ops few (most business ADTs) |

**Do not say “Visitor is obsolete.”** Say “Visitor still wins when operations grow and types don’t; for a sealed domain model I use pattern matching.”

#### C. Exhaustive `switch` as a poor State/Strategy

```java
// Java 8 State via switch — easy to miss a branch
enum Status { OPEN, CLOSED, ARCHIVED }

String label(Status s) {
    switch (s) {
        case OPEN: return "open";
        case CLOSED: return "closed";
        // ARCHIVED reaches default; it does not implicitly return null
        default: throw new IllegalStateException();
    }
}

// Java 14+ enum switch expression — must be exhaustive or have default
String label17(Status s) {
    return switch (s) {
        case OPEN -> "open";
        case CLOSED -> "closed";
        case ARCHIVED -> "archived";
    };
}
```

State **pattern** (objects + transitions) still beats a giant switch when transitions have behavior. Use switch for enum mappings; switching on sealed-type patterns requires preview in 17 or standard Java 21. Java 17 ordinary enum/string switches throw NPE on a null selector.

#### D. Builder vs record

```java
// Java 8 — Builder still the answer for HttpRequest with 8 optional fields
// Java 17 — 2–3 required components: just a record
record Money(String currency, long cents) {}

// Hybrid still valid on 17
record RequestSpec(String method, String url, String body, int timeoutMs) {
    RequestSpec {
        Objects.requireNonNull(method, "method");
        Objects.requireNonNull(url, "url");
        Objects.requireNonNull(body, "body");
        if (method.isBlank() || url.isBlank() || timeoutMs <= 0)
            throw new IllegalArgumentException("invalid request settings");
    }
    static final class Builder {
        private String method = "GET", url, body = "";
        private int timeoutMs = 1000;
        Builder url(String u) { url = u; return this; }
        Builder method(String m) { method = m; return this; }
        Builder body(String b) { body = b; return this; }
        Builder timeoutMs(int t) { timeoutMs = t; return this; }
        RequestSpec build() {
            if (url == null) throw new IllegalStateException("url required");
            return new RequestSpec(method, url, body, timeoutMs);
        }
    }
}
```

**Invalid claim:** “Java 17 replaced Builder with records.” Records replaced **hand-written value classes**. Builder remains for optional/fluent construction.

#### E. Prototype / clone

Still don’t use `Cloneable`. Records: `new Money(m.currency(), m.cents())` is a shallow copy. Mutable list components still need a defensive copy — **same bug as Java 8 beans.**

```java
record Folder(String name, List<String> files) {
    Folder {
        files = List.copyOf(files); // Java 10; shallow snapshot; String elements immutable
    }
}
```

On 8 you’d `Collections.unmodifiableList(new ArrayList<>(files))`.

#### F. Abstract Factory + Factory Method

Still valid. JDK itself moved toward static factories: `List.of`, `HttpClient.newHttpClient()`, `Path.of` (11; `Paths.get` on 8).

Simple factory via enum/`switch` is **safer** on 14+ because of exhaustiveness.

```java
Notifier create(Kind k) {
    return switch (k) {
        case EMAIL -> new EmailNotifier();
        case SMS   -> new SmsNotifier();
    };
}
```

#### G. Null Object vs Optional

Both exist. Java 9–11 made Optional less painful (`or`, `ifPresentOrElse`, `isEmpty`). Null Object still right for **interfaces with behavior** (`Logger`). Optional still right for **return values**. `Optional` is primarily a return-type API; field use is a design choice with framework/serialization implications, not a language prohibition. Never return null from a method whose contract is Optional.

#### H. Memento

`record DocMemento(String text) {}` is a transparent snapshot. If Memento requires opaque state accessible only to the originator, use an encapsulated nested implementation; a public record exposes its components.

#### I. Interpreter

Sealed `Expr` + `eval()` on the interface **or** a separate function with pattern matching. Interpreter pattern didn’t die; the class explosion got sealed.

#### J. Marker interface

Still `Serializable` / `RandomAccess`. Markers participate in subtyping and generic bounds; annotations attach metadata. Sealing restricts permitted implementations. They are distinct mechanisms, not interchangeable upgrades.

#### K. Singleton + double-checked locking

**Unchanged.** Double-checked locking requires a `volatile` instance field. Enum and initialization-on-demand holder are common alternatives; the appropriate scope depends on the application. Java 17 did not add a new singleton keyword. Records have no “one instance” semantics.

#### L. Dynamic Proxy

```java
// Java 16+: InvocationHandler can invoke interface default methods via
// InvocationHandler.invokeDefault(...)
```

Rare interview detail. If you write JDK proxies around interfaces with defaults, 8 needed a workaround; 16+ has `invokeDefault`.

#### M. Observer / reactive

| 8 | 9–17 |
|---|---|
| `Observable` / `Observer` (already broken) | **Deprecated** (9). Don’t touch |
| RxJava / Reactor | Same |
| — | `java.util.concurrent.Flow` (Reactive Streams SPI), `SubmissionPublisher` |

For Google system design, talk Pub/Sub, not `Flow`. For Java API design, “Observer, or Flow if we need RS.”

#### N. Finalizer → Cleaner

```java
// Java 9+: a minimal Cleaner lifecycle demo, not a native-resource wrapper.
// The counter stands in for external cleanup; State cannot retain CleanupDemo.
final class CleanupDemo implements AutoCloseable {
    private static final Cleaner CLEANER = Cleaner.create();
    private static final class State implements Runnable {
        private final java.util.concurrent.atomic.AtomicInteger cleanups;
        State(java.util.concurrent.atomic.AtomicInteger cleanups) { this.cleanups = cleanups; }
        @Override public void run() { cleanups.incrementAndGet(); }
    }
    private final Cleaner.Cleanable cleanable;
    CleanupDemo(java.util.concurrent.atomic.AtomicInteger cleanups) {
        cleanable = CLEANER.register(this, new State(Objects.requireNonNull(cleanups)));
    }
    @Override public void close() { cleanable.clean(); } // action runs at most once
}
```

`finalize` was deprecated in 9, then deprecated **for removal in 18**, not 17. Use `AutoCloseable` + try-with-resources for prompt cleanup. Cleaner is a nondeterministic fallback: the cleanup action must not capture the referent (`this`), directly or indirectly, or it prevents phantom reachability. Typically use one shared Cleaner and a static cleanup-state class; do not depend on cleanup running before process exit.

#### O. Service Locator vs `ServiceLoader`

`ServiceLoader` is an SPI discovery mechanism (since 6); Java 9 adds module `provides` / `uses` and provider streams. It discovers implementations, whereas a general service locator resolves application dependencies. It can be used with DI, e.g. to discover plugins.

---

## 5. Patterns that look “Java 8” and will get a follow-up

Say these **only** if you also know the 17 counterpart.

| If you write… | They may ask… | Answer |
|---|---|---|
| Anonymous `new Comparator<Foo>() { ... }` | Lambda? | Yes, Java 8 already. `Comparator.comparing(...)` |
| `getX()` JavaBean for a value | Record? | Yes on 17 if it’s a value |
| Full Visitor for 3 node types | Sealed? | Yes if the set is closed |
| `Arrays.asList` as “immutable” | `List.of`? | `asList` is **not** immutable |
| `collect(toList())` then `.add` | `toList()`? | `toList()` (16) is unmodifiable; mutation was always on thin ice |
| `HttpURLConnection` | `HttpClient`? | 11+ standard library |
| `Date` / `Calendar` | `java.time`? | That was **Java 8**. Using `Date` on 17 is a smell |
| `new Integer(1)` | Deprecated? | Deprecated in 9; marked for removal in 16. Use `valueOf` / autobox |
| `setAccessible(true)` on `String.value` | Why fail on 17? | Strong encapsulation (16+) |
| CMS GC tuning story | Still exists? | **Removed in 14** |
| Nashorn | — | **Removed in 15**. Use GraalJS or don’t embed JS |
| JAXB `javax.xml.bind` on JDK | — | **Removed in 11**. Add a dependency; Jakarta namespace later |
| `SecurityManager` | — | **Deprecated for removal in 17** |
| `Thread.stop` | — | Unsafe since forever; still don’t |

---

## 6. Runtime, JDK, migration landmines (8 → 17)

These show up as “you migrated a service, what broke?”

### 6.1 Strong encapsulation (the big one)

JPMS arrived in 9. Relaxed access to many pre-9 JDK internals was the default in 9–15; strong encapsulation became the default in 16. Java 17 removes the broad `--illegal-access=permit` escape hatch. Deep reflection into a non-open package can throw `InaccessibleObjectException`; ordinary reflection on accessible public API is still supported.

**What broke in real life:** Lombok/old bytecode tools, mocking JDK classes, JSON libs poking `String`, Hadoop/Spark on old versions, `sun.misc.Unsafe` use. Some critical APIs, including `sun.misc.Unsafe`, remain accessible in 17 as an exception; prefer supported APIs such as `VarHandle` for suitable operations. Moving to **`jdk.internal.misc.Unsafe` is not a supported migration**.

**Interview:** “We needed `--add-opens` as a bridge, then removed the illegal access.” Don’t propose `--add-opens` as the destination.

### 6.2 Removed / moved out of the JDK

| Gone from JDK | When | What you do |
|---|---|---|
| Selected Java EE/CORBA modules (JAXB, JAX-WS, CORBA, common annotations, transaction subset) | 11 | Add compatible dependencies; removal alone does not require a `jakarta.*` namespace migration |
| JavaFX from Oracle JDK | 11 | OpenJFX separately; not bundled in every Java 8 distribution |
| Nashorn | 15 | Don’t embed JS in JDK |
| CMS GC | 14 | G1 / ZGC / Parallel |
| Pack200 | 14 | — |
| RMI activation | 17 | — |
| Applet API / SecurityManager | deprecated **for removal** in 17, still present | Replace affected functionality when migrating; these are not removals in 17 |

Only specific bundled modules were removed; **not every `javax.*` API**. Java SE packages such as `javax.sql`, `javax.crypto` and `javax.transaction.xa` remain.

### 6.3 GC and performance talking points

| | 8 | 17 |
|---|---|---|
| Default GC | Parallel | **G1** (default since 9) |
| CMS | Common | **Removed (14)** |
| G1 | Optional | Default, much improved |
| ZGC | Not in original JDK 8 | Production since 15; designed for low pauses, with CPU/memory tradeoffs; measure your workload |
| Shenandoah | Available in some later vendor backports | Production upstream since 15; availability depends on JDK distribution |
| Helpful NPE | Less detailed VM messages | Introduced in 14 (opt-in there), enabled by default since 15; explains many VM-generated NPEs |

Parallel→G1 describes typical server-class HotSpot defaults; ergonomics, explicit flags and distributions can differ. Do not promise a latency target merely from a collector name. For migration discussions, compare GC logs, throughput, CPU, memory and tail latency against the same workload.

### 6.4 Tooling

- `jlink` (9) — custom runtime
- `jdeps` (8 already, more useful with modules)
- `jshell` (9)
- `java Hello.java` single-file (11)
- `jpackage` (16) — native installers
- Flight Recorder was open-sourced in OpenJDK 11; Mission Control is a separate tool. Java 8 availability/licensing depends on distribution and update
- Microbenchmarks: JMH still; `VarHandle` vs `Unsafe`

### 6.5 Modules (JPMS, 9)

Know: `module-info.java`, `requires`, `exports`, `opens`, unnamed module, split packages.

Running on the classpath uses the unnamed module and does not require `module-info.java`. Split-package restrictions matter when introducing named modules; the JDK upgrade does not simply ban all classpath split packages. `exports` exposes public API; `opens` allows deep reflection into a package. Describe your actual deployment, not a memorized migration claim.

### 6.6 Serialization

Basic serialization filters predate 17 (Java 9, backported to 8u121); `jdk.serialFilter` is not new in 17. Java 17 adds context-specific filter selection through `ObjectInputFilter.Config.setSerialFilterFactory` or `jdk.serialFilterFactory`. The JVM-wide factory selects/composes a filter as streams are constructed or filters set. Prefer safer formats for untrusted input; filters do not make arbitrary object deserialization safe.

Records serialize by components, not by fields you invent.

### 6.7 NullPointerException quality (14)

```java
user.getAddress().getCity().trim();
// 17: Cannot invoke "String.trim()" because the return value of "Address.getCity()" is null
```

Small, but it is a real debugging upgrade. Mention if they ask “favorite 17 quality-of-life.”

---

### 6.8 Verify a real migration

Run the existing Java 8 artifact on the target runtime first, then rebuild with updated dependencies/plugins. Check reflection, agents, JNI, removed JVM flags, TLS/certificate changes and behavior under representative load. Test the actual target JDK; compilation alone is not a runtime compatibility test.

```bash
# Replace these illustrative paths with actual source/artifacts.
javac --release 8 -d out src/Example.java   # limits syntax AND Java SE API surface
jdeps --jdk-internals app.jar              # static analysis; cannot find every reflective use
jdeprscan --release 17 app.jar             # deprecated Java SE API usage
```

`-source 8 -target 8` alone does not prevent calls to newer library APIs. `--release 8` does; dependencies still need compatible bytecode/runtime support. After adopting records or other Java 17 features, build that code for 17 and retain rollback artifacts compatible with the previous runtime.

---

## 7. Concurrency: 8 vs 17 (and don’t confuse 21)

| Tool | Since | Notes |
|---|---|---|
| `CompletableFuture` | 8 | Still the default async API on 17 |
| `StampedLock`, `LongAdder` | 8 | Unchanged |
| `Flow` / `SubmissionPublisher` | 9 | RS SPI |
| `VarHandle` | 9 | Ordered / volatile / CAS without Unsafe |
| `Thread.onSpinWait` | 9 | |
| `CompletableFuture.orTimeout` / `completeOnTimeout` | 9 | |
| `ExecutorService` + `AutoCloseable` | 19 | **not 17** |
| Virtual threads | 21 | **not 17** |

Virtual threads were preview in 19/20 and finalized in 21; they are not in standard Java 17. `CompletableFuture.orTimeout` completes the future exceptionally but does not automatically stop its underlying task. Specify executors and resource limits deliberately; parallel streams/async stages are not inherently faster.

---

## 8. Side-by-side snippets interviewers actually use

### Immutable list

```java
// 8 — still mutable structure behind unmodifiable view if you keep the backing ref
List<String> inner = new ArrayList<>();
inner.add("a");
List<String> view = Collections.unmodifiableList(inner);
inner.add("b"); // view now has b — classic trap

// 9+
List<String> frozen = List.of("a");
List<String> copy = List.copyOf(inner); // 10+: independent structure, rejects null
```

### Equals/hashCode

```java
// Inside a Java 17 final value class with non-null currency and long cents.
@Override public boolean equals(Object o) {
    if (this == o) return true;
    if (!(o instanceof Amount m)) return false;
    return cents == m.cents && currency.equals(m.currency);
}
@Override public int hashCode() { return Objects.hash(currency, cents); }
// Java 8: use instanceof Amount followed by an explicit cast.
// A record can generate both methods instead.
```

### Multi-line JSON fixture

Text blocks (15) vs `+` concatenation. That’s it.

### Sealed hierarchy with explicit handling (Java 17; no exhaustiveness check)

```java
sealed interface Shape permits Circle, Rect {}
record Circle(double r) implements Shape {}
record Rect(double w, double h) implements Shape {}

static double area(Shape s) {
    Objects.requireNonNull(s, "shape");
    if (s instanceof Circle c) return Math.PI * c.r() * c.r();
    if (s instanceof Rect r) return r.w() * r.h();
    throw new IllegalStateException("unhandled shape"); // adding a subtype does not force this if-chain to change
}
```

Assume finite, non-negative dimensions; add constructor validation if enforcing this domain contract. On 21 a pattern-switch expression can omit default when all permitted cases are covered. A null selector still needs an explicit policy. The Java 17 version above will compile even if you later add a permitted subtype and forget its branch.

---

## 9. What to write in a Google **coding** round

1. Confirm the supported version; use Java 8-compatible syntax as a fallback when unknown.
2. `List<Integer> list = new ArrayList<>();` not `var` if it hurts readability for the interviewer.
3. Keep the provided node/API contract. Records are unsuitable for nodes you need to mutate in place.
4. `Deque`/`ArrayDeque`, `PriorityQueue`, `HashMap` — same on both.
5. If you want a record for a helper pair: ask “Java 16+ OK?” One sentence. If no, `int[]` or a static inner class.

**Concise Java 17 helpers when supported:** `record Pair(int i, int j)`, `List.of`, `switch` expressions, `instanceof Foo f`.

---

## 10. What to say in a **Googleyness / experience** round

Story shape: “Migrated X from 8 to 17.”

1. **Why:** LTS, G1/ZGC, records, security (encapsulation), drop CMS, library support.
2. **Broke:** JAXB on the JDK, illegal reflective access, `toList()` mutability, an old BCEL/Lombok, `sun.misc.BASE64Encoder`.
3. **What you did:** dependency replacements, `--add-opens` as temporary, then removed; CI matrix 8/11/17; `jdeps`.
4. **What you didn’t do:** full JPMS split of a monolith.
5. **Pattern change:** DTOs → records in new code; Visitor kept for the compiler-like module; new ADTs sealed.

These are possible discussion points, not a story to claim verbatim. Explain your ownership, rollout/rollback plan and measured results (latency, error rate, resource use, compatibility). Do not invent failures or metrics. Interview levels depend on scope and judgment, not a list of Java features.

---

## 11. Rapid-fire answers

**Q: Difference between `List.of` and `Arrays.asList`?**  
`asList` is a fixed-size list backed by an array (slots can be replaced with `set`; `add` is unsupported). `List.of` is structurally immutable, no nulls, not backed by a writable array.

**Q: `Collectors.toList()` vs `Stream.toList()`?**  
`Stream.toList()` (16) is unmodifiable and accepts null elements. `Collectors.toList()` does not promise a concrete type or mutability. For guaranteed mutability use `collect(Collectors.toCollection(ArrayList::new))`. `toUnmodifiableList()` rejects nulls.

**Q: Why records aren’t JPA entities?**  
Records are final with final component fields, which conflicts with standard JPA entity requirements and mutable lifecycle management. A record can declare a no-arg constructor that delegates to its canonical constructor, so the constructor alone is not the fundamental issue. Records work as query projections/DTOs; embeddable support is provider/version-specific.

**Q: Is Visitor dead?**  
No. Sealed+PM wins for closed models with few ops. Visitor wins for many ops on a stable tree.

**Q: Best singleton on 17?**  
Enum or holder idiom, depending on requirements. Both have class-loader scope. Prefer explicitly managed dependencies when global identity is unnecessary.

**Q: Virtual threads in 17?**  
No. 21.

**Q: Pattern switch in 17?**  
Preview only.

**Q: Default GC 8 vs 17?**  
Parallel vs G1.

**Q: What is strong encapsulation?**  
Deep reflection into non-open JDK packages is restricted; accessible public API still works. Java 16 made strong encapsulation the default; 17 removed the broad illegal-access override. Targeted `--add-opens` is a migration bridge.

**Q: `var` on a field?**  
Illegal.

**Q: Can a record extend another record?**  
No.

**Q: Sealed + new subclass in another jar?**  
A direct subtype must be permitted (explicitly, or inferred in the same compilation unit) and be in the same named module, or the same package in the unnamed module. A separate module cannot directly extend it. A non-sealed permitted subtype can be extended normally.

**Q: Text blocks vs `String.format`?**  
Blocks are literals. No interpolation in 17. Still use `formatted()` (Java 15) : `"%s".formatted(x)`.

**Q: `Optional` field in a record?**  
Legal, but Optional is primarily designed for return values and does not implement Serializable. Decide the field contract and framework compatibility explicitly; do not permit both null Optional and Optional.empty() for the same absence state.

**Q: Checked exceptions in lambdas?**  
The target functional interface determines which checked exceptions may escape. Use an interface that declares them (e.g. Callable), handle them, or wrap with a meaningful exception preserving the cause. Sneaky throws hide the contract and are not a default solution.

**Q: Modules mandatory?**  
No.

---

## 12. One-page memory

```
Java 8  : lambdas, streams, java.time, default methods, Optional, CompletableFuture
Java 9  : modules, List.of, Flow, private interface methods, JShell, G1 default
Java 10 : var, List.copyOf, orElseThrow()
Java 11 : HttpClient, String.isBlank/strip/repeat/lines, Files.readString, Predicate.not
          Selected Java EE/CORBA modules removed from JDK
Java 14 : switch expressions, helpful NPE, CMS removed
Java 15 : text blocks, Nashorn removed, ZGC production
Java 16 : records, pattern instanceof, Stream.toList, strong encapsulation
Java 17 : sealed classes, SecurityManager deprecated for removal  ★ LTS

NOT 17  : virtual threads (21), pattern switch production (21), value types (Valhalla)

Patterns demoted : JavaBean DTO, Visitor-for-every-ADT, Arrays.asList-as-immutable
Patterns alive   : Strategy, Decorator, Proxy, Adapter, Facade, DI, Builder (optional fields),
                   Singleton enum, State objects, Observer (not java.util.Observable)
```

If you remember only four sentences for the interview:

1. **Records** reduce boilerplate for transparent value carriers; Builders and ordinary classes remain useful.  
2. **Sealed + pattern matching** can simplify closed hierarchies; Java 17 if-chains are not exhaustiveness-checked. Visitor remains useful when operations grow.  
3. **`List.of` / `Stream.toList()`** are unmodifiable, not deeply immutable; only the latter accepts nulls. Use an explicit mutable collector when needed.  
4. **17 is not 21** — no virtual threads; pattern switch is preview only. Strong encapsulation affects unsupported reflective access, not all reflection.


---

## 13. Review validation and official references

All **22 Java code blocks** compiled with `javac --release 17`, without preview, after supplying imports, enclosing classes/methods and minimal domain scaffolding. Six Java 8 comparison extracts also compiled with `--release 8`. The corrected examples passed **50 behavioral checks** and **three compiler acceptance/rejection checks** for enum exhaustiveness, sealed if-chains and Java 17 pattern-switch preview requirements.

Validation used a **JDK 25.0.2 compiler/runtime** targeting Java 17/8; it was not a run on actual Java 8 or 17 VMs. HTTP code was compiled but no network request was executed. Cleaner tests verified explicit cleanup, not nondeterministic GC timing. Temporary harnesses are outside the study files.

- Collection contracts: [Stream.toList](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/stream/Stream.html#toList()) and [Collectors.toList](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/util/stream/Collectors.html#toList()).
- Language rules: [records](https://docs.oracle.com/en/java/javase/17/language/records.html), [sealed classes](https://docs.oracle.com/en/java/javase/17/language/sealed-classes-and-interfaces.html), [local type inference](https://docs.oracle.com/en/java/javase/17/language/local-variable-type-inference.html).
- Encapsulation and removals: [migration from Java 8](https://docs.oracle.com/en/java/javase/17/migrate/migrating-jdk-8-later-jdk-releases.html), [removed tools/components](https://docs.oracle.com/en/java/javase/17/migrate/removed-tools-and-components.html).
- Lifecycle and serialization details: [Cleaner API](https://docs.oracle.com/en/java/javase/17/docs/api/java.base/java/lang/ref/Cleaner.html), [serialization filtering](https://docs.oracle.com/en/java/javase/17/core/serialization-filtering1.html).
